import configparser
from typing import Optional, List, Any
from phone import Phone
from pypinyin import pinyin, Style, load_single_dict


class CheckInput:

    def __init__(self):
        pass

    @classmethod
    def check_name(cls, check_str: str) -> Optional[str]:
        if len(check_str) != 0:
            return None
        elif len(check_str) == 0:
            return '用户名为空'

    @classmethod
    def check_tel(cls, check_str: str) -> Optional[str]:
        if len(check_str) < 7:
            return '非法手机号长度'
        info = Phone().find(check_str)
        if info['phone_type'] != '':
            return None


class SortContact:
    def __init__(self):
        pass

    @classmethod
    def sort(cls, contact_list: list):
        load_single_dict({ord('翟'): 'zhai'})
        temp_list = []
        for i in range(0, 30):
            temp_list.append([])  # 初始化列表
        for i in contact_list:
            temp_list[ord(pinyin(i[1], style=Style.FIRST_LETTER)[0][0])-97].append(i[1])

        return temp_list


class ConfigManager:
    def __enter__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        if "DB" not in self.config.sections():
            self.config.add_section("DB")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open("config.ini", "w+") as f:
            self.config.write(f)

    def getDBName(self) -> str:
        try:
            return self.config.get("DB", "name")
        except Exception as e:
            self.config.set("DB", "name", "DB1")

    def setDBName(self, db_name) -> None:
        self.config.set("DB", "name", db_name)
