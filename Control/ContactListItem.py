import flet as ft
from flet import (
    UserControl,
    Banner,
    Text,
    TextButton
)
from flet_core import TextAlign, ButtonStyle, colors

from Foundation import DBService


class DeleteBanner(Banner):
    def __init__(self, contact_name: str, contact_list):
        self._contact_list = contact_list

        def close_event(e):
            self.page.banner.open = False
            self.page.update()

        def delete_event(e):
            if not self.page.client_storage.get("DB_PATH"):
                self.db_name = self.page.client_storage.get("DB_NAME")
            else:
                self.db_name = self.page.client_storage.get("DB_PATH")
            with DBService.DBService(db_name=self.db_name) as dbService:
                dbService.delete_by_name('contactlist', contact_name)
                self.page.banner.open = False
                print(type(self._contact_list))
                self._contact_list.lv.controls.clear()
                self._contact_list.lv.update()
                self._contact_list.update_data_all()
                self._contact_list.lv.update()
                self.page.update()
        super().__init__(
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=colors.AMBER, size=40),
            content=Text(f'确认删除{contact_name}'),
            actions=[
                TextButton("删除", style=ButtonStyle(color=colors.RED), on_click=delete_event),
                TextButton("取消", on_click=close_event)
            ]
        )


class ContactListItem(UserControl):
    def __init__(self, contact_name, button_event, contact_list):
        super().__init__()
        self._contact_name = contact_name
        self._self_event = button_event
        self._textButton = TextButton
        self._contact_list = contact_list

    @property
    def contact_name(self):
        return self._contact_name

    def build(self):
        def get_contact_info_event(e) -> None:
            self._self_event(self)

        def delete_contact_event(e) -> None:
            banner = DeleteBanner(self._contact_name, self._contact_list)
            self.page.banner = banner
            self.page.banner.open = True
            self.page.update()

        self._textButton = ft.TextButton(
            content=ft.Text(
                value=self._contact_name,
                text_align=TextAlign.LEFT,
            ),
            on_click=get_contact_info_event,
            on_long_press=delete_contact_event
        )
        return self._textButton
