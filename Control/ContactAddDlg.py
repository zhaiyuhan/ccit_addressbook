from flet import (
    Page,
    AlertDialog,
    Text,
    Card,
    Container,
    Column,
    TextButton,
    TextField,
    MainAxisAlignment,
    TextStyle,
    colors
)

import Foundation.MyUtility
from Foundation import DBService
import Control.ContactList as clList


# 这是一个用来弹出错误或者警告的通用模板
class AlarmDlg(AlertDialog):
    def __init__(self, title: str, message: str):
        super().__init__(
            title=Text(f'{title}'),
            content=Text(f'{message}')
        )


class ContactAddDlg(AlertDialog):
    _name_TextFild = TextField(label='姓名', hint_text='填入联系人姓名', border_color='transparent')
    _tel_TextFild = TextField(label='手机号', hint_text='填入联系人手机号', border_color='transparent')
    _address_TextFile = TextField(label='通讯地址', hint_text='填入联系人通讯地址', border_color='transparent')
    _contact_list = clList.ContactList

    def BindContactList(self, contact_list: clList.ContactList):
        self._contact_list = contact_list

    def __init__(self, page: Page):
        self._name_TextFild.value = ''
        self._tel_TextFild.value = ''
        self._address_TextFile.value = ''

        def close_event(e):
            self.open = False
            page.update()

        def add_contact_event(e):
            error_code = 100
            if (re1 := Foundation.MyUtility.CheckInput().check_name(self._name_TextFild.value)) is not None:
                self._name_TextFild.value = ''
                self._name_TextFild.hint_text = re1
                self._name_TextFild.hint_style = TextStyle(color=colors.BLUE)  # 修改提示字的颜色
                self._name_TextFild.focus()
                self._name_TextFild.update()
                error_code += 1
            if (re2 := Foundation.MyUtility.CheckInput().check_tel(self._tel_TextFild.value)) is not None:
                self._tel_TextFild.value = ''
                self._tel_TextFild.hint_text = re2
                self._tel_TextFild.focus()
                self._tel_TextFild.update()
                error_code += 1

            if error_code == 100:
                with DBService.DBService("DB1") as dbService:
                    dbService.insert_db('contactlist', {'name': f'{self._name_TextFild.value}',
                                                        'tel': f'{self._tel_TextFild.value}',
                                                        'address': f'{self._address_TextFile.value}'})
                    self.open = False
                    page.update()
                self._contact_list.lv.controls.clear()
                self._contact_list.lv.update()
                self._contact_list.update_data_all()
                self._contact_list.lv.update()

        super().__init__(
            modal=True,
            title=Text('添加新联系人'),
            content=Card(
                content=Container(
                    content=Column(
                        [
                            self._name_TextFild,
                            self._tel_TextFild,
                            self._address_TextFile
                        ]
                    )
                )
            ),
            actions=[
                TextButton("确认添加", on_click=add_contact_event),
                TextButton("取消", on_click=close_event)
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print('Modal dialog dismissed!')
        )
