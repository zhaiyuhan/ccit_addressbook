from flet import (
    UserControl,
    TextField,
    TextButton,
    Row
)

from Control import ContactList

from Foundation import DBService


class ContactSearch(UserControl):
    def __init__(self, contactlist: ContactList.ContactList):
        super().__init__()
        self._contact_list = contactlist
        self._searchTextField = TextField(hint_text='请输入查找内容')
        self._searchTextButton = TextButton('搜索')

    def build(self):
        def search_event(e) -> None:
            data = self._searchTextField.value
            # 在此处进行单个用户的查询
            with DBService.DBService("DB1") as dbService_query_by_name:
                temp_data = dbService_query_by_name.query_db_by_name_fuzzy('contactlist', data)
                print('通过姓名查询到的信息为', temp_data)
                self._contact_list.lv.controls.clear()
                self._contact_list.lv.update()
                self._contact_list.update_by_search_result(temp_data)
                self._contact_list.lv.update()
                # self._panel.contact_info = list(temp_data)

        self._searchTextButton.on_click = search_event
        return Row([
            self._searchTextField,
            self._searchTextButton
        ])
