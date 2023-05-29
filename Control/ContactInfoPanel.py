import flet as ft
from flet import (
    UserControl,
    Card,
    TextField,
    ElevatedButton,
    Column
)

from Foundation import DBService
# import Control.ContactList as clList


class ContactInfoPanel(UserControl):
    _contact_info = list()  # 联系人信息

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value):
        if not isinstance(value, list):
            raise ValueError('非列表')
        self._contact_info = value
        self._nameTextField.value = self._contact_info[1]
        self._telTextField.value = self._contact_info[2]
        self._addressTextField.value = self._contact_info[3]
        print(self._contact_info)
        self.update()

    def __init__(self):
        super().__init__()
        self._contact_list = None
        self._nameTextField = TextField(label='姓名', value='', read_only=True)
        self._telTextField = TextField(label='手机号', value='', read_only=True)
        self._addressTextField = TextField(label='通讯地址', value='', read_only=True)
        self._editElevatedButton = ElevatedButton()

    def BindContactList(self, contact_list):
        self._contact_list = contact_list

    def active_edit(self):
        self._editElevatedButton.text = '保存'
        self._nameTextField.read_only = False
        self._telTextField.read_only = False
        self._addressTextField.read_only = False
        self.update()

    def disable_edit(self):
        self._editElevatedButton.text = '修改'
        self._nameTextField.read_only = True
        self._telTextField.read_only = True
        self._addressTextField.read_only = True
        self.update()

    def build(self):
        def edit_event(e):
            if self._editElevatedButton.text == '修改':
                self.active_edit()
            else:
                with DBService.DBService("DB1") as dbService:
                    dbService.update_db_by_id('contactlist', self._contact_info[0],
                                              [f'{self._nameTextField.value}',
                                               f'{self._telTextField.value}',
                                               f'{self._addressTextField.value}'])
                self.disable_edit()
                self._contact_list.lv.controls.clear()
                self._contact_list.lv.update()
                self._contact_list.update_data_all()
                self._contact_list.lv.update()
        self._editElevatedButton = ElevatedButton('修改', on_click=edit_event)

        main_col = Column(
            [
                self._nameTextField,
                self._telTextField,
                self._addressTextField,
                self._editElevatedButton
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return Card(
            content=main_col,
            margin=ft.margin.all(20),
        )
