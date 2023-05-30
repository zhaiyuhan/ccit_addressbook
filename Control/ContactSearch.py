from flet import (
    UserControl,
    TextField,
    TextButton,
    Row,
    Page
)

from Control import ContactList

from Foundation import DBService


class ContactSearch(UserControl):
    def __init__(self, contactlist: ContactList.ContactList, _page: Page):
        super().__init__()
        self.page = _page
        self._contact_list = contactlist
        self._searchTextField = TextField(hint_text='请输入查找内容')
        self._searchTextButton = TextButton('搜索')
        self.db_name = str()
        # 如果地址为空 就把db_name赋值为数据库的名字
        if not self.page.client_storage.get("DB_PATH"):
            self.db_name = self.page.client_storage.get("DB_NAME")
        else:
            self.db_name = self.page.client_storage.get("DB_PATH")
        print('搜索框获取到的数据库', self.db_name)

    def build(self):
        def search_event(e) -> None:
            data = self._searchTextField.value
            # 在此处进行单个用户的查询
            with DBService.DBService(self.db_name) as dbService_query_by_name:
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
