import flet as ft
from flet import (
    TextButton,
    NavigationRail,
    Row,
    UserControl,
)

import Pages.SettingPage

import Control.ContactInfoPanel as clPanel
import Control.ContactList as clList
import Control.ContactAddDlg as clDlg
import Control.ContactSearch as clSearch

from Foundation.MyUtility import ConfigManager


class MyAppBar(UserControl):
    def __init__(self, dlg_event, select_index):
        super().__init__()
        self._dlg_event = dlg_event
        self.rail = NavigationRail
        self._selectIndex = select_index

    def build(self):
        def change_event(e):
            match e.control.selected_index:
                case 0:
                    self.page.go("/")
                case 1:
                    self.page.go("/group")
                case 2:
                    self.page.go("/setting")

        # 右边侧栏
        rail = NavigationRail(
            selected_index=self._selectIndex,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.FloatingActionButton(icon=ft.icons.ADD, text="添加", on_click=self._dlg_event),
            group_alignment=-0.5,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.PERSON,
                    selected_icon=ft.icons.PERSON,
                    label="联系人",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="分组",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("设置"),
                )],
            on_change=change_event,
        )
        return Row([
            rail,
            ft.VerticalDivider(width=1),
        ])


def main(page: ft.Page):
    if page.client_storage.contains_key("DB_NAME"):
        print(page.client_storage.get("DB_NAME"))
    else:
        page.client_storage.set("DB_NAME", "DB1")

    # 如果第一次没有设置路径就设置为空
    # 如果路径为空就直接在运行工程目录下查找
    if page.client_storage.contains_key("DB_PATH"):
        print(page.client_storage.get("DB_PATH"))
    else:
        page.client_storage.set("DB_PATH", "EMPTY")

    page.window_width = 880
    page.title = 'SB319通讯录'
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    add_dlg = clDlg.ContactAddDlg(page)  # 联系人添加对话框

    def open_dlg(e):
        page.dialog = add_dlg
        add_dlg.open = True
        page.update()

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            contactPanel = clPanel.ContactInfoPanel()  # 联系人信息展示面板
            contactList = clList.ContactList(contactPanel)  # 联系人列表
            contactSearch = clSearch.ContactSearch(contactList)  # 联系人搜索框
            contactPanel.BindContactList(contactList)
            page.views.append(
                ft.View(
                    "/",
                    [ft.Row(
                        [
                            MyAppBar(open_dlg, 0),
                            ft.Column([contactSearch,
                                       ft.Row([contactList],
                                              expand=True,
                                              scroll=ft.ScrollMode.AUTO)]),
                            contactPanel,
                        ],
                        expand=True
                    )])
            )
            add_dlg.BindContactList(contactList)

            def page_resize(e):
                contactList.width = page.window_width - 600
                page.update()
                print("New page size:", page.window_width, page.window_height)

            page.on_resize = page_resize
        if page.route == "/group":
            page.views.append(
                ft.View(
                    "/group",
                    [ft.Row(
                        [
                            MyAppBar(open_dlg, 1),
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Check power"),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),
                                                ft.Text("Item with a custom content"),
                                            ]
                                        ),
                                        on_click=lambda _: print("Button with a custom content clicked!"),
                                    ),
                                    ft.PopupMenuItem(),  # divider
                                    ft.PopupMenuItem(
                                        text="Checked item", checked=False,
                                    ),
                                ]
                            ),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("First name")),
                                    ft.DataColumn(ft.Text("Last name")),
                                    ft.DataColumn(ft.Text("Age"), numeric=True),
                                ],
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("John")),
                                            ft.DataCell(ft.Text("Smith")),
                                            ft.DataCell(ft.Text("43")),
                                        ],
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Jack")),
                                            ft.DataCell(ft.Text("Brown")),
                                            ft.DataCell(ft.Text("19")),
                                        ],
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Alice")),
                                            ft.DataCell(ft.Text("Wong")),
                                            ft.DataCell(ft.Text("25")),
                                        ],
                                    ),
                                ],
                            ),

                        ],
                        expand=True
                    )])
            )
        if page.route == "/setting":
            page.views.append(
                ft.View(
                    "/setting",
                    [ft.Row(
                        [
                            MyAppBar(open_dlg, 2),
                            Pages.SettingPage.SettingPage(page),
                        ],
                        expand=True
                    )])
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
    page.update()


if __name__ == "__main__":
    # with ConfigManager() as cm:
    # cm.setDBName("DEMO")
    # print(cm.getDBName())
    ft.app(target=main)
