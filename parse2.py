import enum
import json
import logging

import requests
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


class ParsePage(object):
    def __init__(self, url) -> None:
        super().__init__()
        self.url = url
        self.strs = []
        self.a_links = {}
        self.need_esacep_chars = {
            "[": "\\[",
            "]": "\\]",
            "*": "\\*",
        }

    def parse_p(self, p: Tag, deep=1) -> None:
        # 解析p标签

        strs = []

        for child in p.children:
            if isinstance(child, NavigableString):
                strs.append(child.text.replace("\n", ""))
                continue
            
            tag_name = child.name

            if tag_name == "a" and child.text.strip() != 'Â¶':
                strs.append(f" **[{child.text}]** ")
                self.a_links[child.text] = child.attrs.get("href")

            elif tag_name == "code":
                strs.append(f" `{child.text}` ")
            
            elif tag_name == "strong":
                strs.append(f" **[{child.text}]** ")

            else:
                logging.info(f'未知节点: {tag_name}')

        sentence = " ".join(strs)

        self.strs.append(sentence)
        self.strs.append("\n")

    def parse_header(self, hx: Tag, number: int) -> None:
        # 解析 标题标签， 如 h1、h2、h3

        text = hx.text
        text = text.replace("Â¶", "")

        prefix = "#" * number

        self.strs.append(f"{prefix} {text}")
        self.strs.append("\n")

    def parse_dl(self, dl: Tag) -> None:
        # 解析 dl dt dd 标签

        for child in dl.children:
            tag_name = child.name

            if tag_name == "dt":
                self.parse_dt(child)

            elif tag_name == "dd":
                self.parse_dd(child)

    def parse_dt(self, dt: Tag) -> None:
        # 解析 dt 类定义、函数定义、异常定义、

        strs = []

        for child in dt.children:
            text = child.text

            if isinstance(child, NavigableString):  # 常规文本
                strs.append(text)
                continue

            class_values = child.attrs.get("class")
            class_str = " ".join(class_values)

            if class_str == "property":  # class 、classmethod 关键字
                text = self.parse_dt_property(child)
                strs.append(f" *{text.strip()}* ")  # 斜体

            elif class_str == "sig-prename descclassname":  # 包的前缀路径
                strs.append(text)

            if class_str == "sig-name descname":  # 类名、方法名、属性名
                strs.append(f" **{text}** ")

            elif class_str == "sig-paren":  # 定义的左边括号、右边括号
                strs.append(text)

            elif class_str == "sig-param":  # 参数定义
                strs.append(self.parse_dt_param(child))

            elif class_str == "sig-return":  # 返回值定义
                strs.append(self.parse_dt_return(child))

        sentence = "".join(strs)

        self.strs.append(sentence)
        self.strs.append("\n")

    def parse_dd(self, dd: Tag) -> None:
        # 解析 dd 文本说明、类的函数集合

        for child in dd.children:
            tag_name = child.name

            if tag_name == "p":
                self.parse_p(child)

            elif tag_name == "dl":
                self.parse_dl(child)
            
            elif tag_name == "ul":

                self.parse_ul(child)  # 参数列表

            else:
                logging.info(f'未知节点: {tag_name}')
    

    def parse_ul(self, ul: Tag) -> None:
        
        for child in ul.children:
            tag_name = child.name

            if tag_name == "li":
                self.parse_li(child)
            else:
                logging.info(f'未知节点: {tag_name}')
    

    def parse_li(self, li: Tag) -> None:

        for child in li.children:
            tag_name = child.name

            if tag_name == "p":
                self.parse_p(child)
            else:
                logging.info(f'未知节点: {tag_name}')


    def parse_dt_property(self, tag: Tag) -> str:
        # 解析函数的返回值定义

        text = tag.text

        sub_links = {}

        for a in tag.select("a"):
            sub_links[a.text] = a.attrs.get("href")

        # 转义字符
        for raw, escaped in self.need_esacep_chars.items():
            text = text.replace(raw, escaped)

        for key in sub_links.keys():
            text = text.replace(key, f"**[{key}]**")

        self.a_links.update(sub_links)

        return text

    def parse_dt_return(self, tag: Tag) -> str:
        # 解析函数的返回值定义

        text = tag.text

        sub_links = {}

        for a in tag.select("a"):
            sub_links[a.text] = a.attrs.get("href")

        # 转义字符
        for raw, escaped in self.need_esacep_chars.items():
            text = text.replace(raw, escaped)

        for key in sub_links.keys():
            text = text.replace(key, f"**[{key}]**")

        self.a_links.update(sub_links)

        return text

    def parse_dt_param(self, tag: Tag) -> str:
        # 解析 类、函数 的参数定义
        # <em class="sig-param"><span class="n"><span class="pre">dir</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>

        text = tag.text
        sub_links = {}

        for a in tag.select("a"):
            sub_links[a.text] = a.attrs.get("href")

        # 转义字符
        for raw, escaped in self.need_esacep_chars.items():
            text = text.replace(raw, escaped)

        if ":" in text:
            param, _type = text.split(":")

            for key in sub_links:
                _type = _type.replace(key, f"**[{key}]**")

            text = f"*{param}:* *{_type.strip()}*"

        self.a_links.update(sub_links)

        return text

    def parse_section(self, section: Tag, deep=1) -> list:
        result = []

        for child in section.children:
            text = child.text
            tag_name = child.name

            if tag_name == "h1":
                self.parse_header(child, 1)

            elif tag_name == "h2":
                self.parse_header(child, 2)

            elif tag_name == "h3":
                self.parse_header(child, 3)

            elif tag_name == "h4":
                self.parse_header(child, 4)

            elif tag_name == "h5":
                self.parse_header(child, 5)

            elif tag_name == "h6":
                self.parse_header(child, 6)

            elif tag_name == "p":
                self.parse_p(child)

            elif tag_name == "dl":
                self.parse_dl(child)

            elif tag_name == "section":
                self.parse_section(child)

        return result

    def parse(self):

        if not url:
            return

        html_doc = requests.get(self.url).text
        soup = BeautifulSoup(html_doc, "html.parser")

        first_section = soup.select_one("div.body>section")

        self.parse_section(first_section)

        for k, v in self.a_links.items():
            print(f"[{k}]: {v}")

        print("\n")
        print("\n".join(self.strs))


if __name__ == "__main__":

    url = "http://localhost:3001/en/api/script.html"

    parse_page = ParsePage(url)
    parse_page.parse()
