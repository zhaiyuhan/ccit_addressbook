from flet import (
    UserControl,
    Text,
    ListView
)

import Control.ContactListItem as clItem
import Control.ContactInfoPanel as clPanel

from Foundation import DBService
from Foundation import MyUtility


class ContactList(UserControl):
    def __init__(self, panel: clPanel.ContactInfoPanel):
        super().__init__()
        self.lv = ListView(
            spacing=10, padding=20, auto_scroll=False, width=300
        )
        self._panel = panel
        self.query_result = list()

    def update_by_search_result(self, search_result):
        def button_event(button_self):
            # 先禁用联系人面板的编辑状态
            # self._panel.disable_edit()
            # 在此处进行单个用户的查询
            with DBService.DBService("DB1") as dbService_query_by_name:
                temp_data = dbService_query_by_name.query_db_by_name('contactlist', button_self.contact_name)[0]
                print('通过姓名查询到的信息为', temp_data)
                self._panel.contact_info = list(temp_data)
        # 根据姓的拼音进行排序
        temp_result = MyUtility.SortContact.sort(search_result)
        index_label = 65
        for FirstLetter in temp_result:
            if len(FirstLetter) != 0:
                self.lv.controls.append(Text(value=f'{chr(index_label)}'))
            index_label += 1
            for words in FirstLetter:
                self.lv.controls.append(clItem.ContactListItem(words, button_event, self))
        del temp_result

    def update_data_all(self):

        def button_event(button_self):
            # 先禁用联系人面板的编辑状态
            self._panel.disable_edit()
            # 在此处进行单个用户的查询
            with DBService.DBService("DB1") as dbService_query_by_name:
                temp_data = dbService_query_by_name.query_db_by_name('contactlist', button_self.contact_name)[0]
                print('通过姓名查询到的信息为', temp_data)
                self._panel.contact_info = list(temp_data)

        # 打开数据库 如果不存在先进行表的创建
        with DBService.DBService("DB1") as dbService:
            dbService.create_table("""CREATE TABLE IF NOT EXISTS contactlist(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        name CHAR(50) NOT NULL, 
                                        tel CHAR(50) NOT NULL,
                                        address CHAR(100));
                                        """)
            self.query_result = dbService.query_db_all('contactlist')
        # 根据姓的拼音进行排序
        temp_result = MyUtility.SortContact.sort(self.query_result)
        index_label = 65
        for FirstLetter in temp_result:
            if len(FirstLetter) != 0:
                self.lv.controls.append(Text(value=f'{chr(index_label)}'))
            index_label += 1
            for words in FirstLetter:
                self.lv.controls.append(clItem.ContactListItem(words, button_event, self))
        del temp_result

    def build(self):
        self.update_data_all()
        return self.lv
