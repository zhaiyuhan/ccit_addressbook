from flet import (
    Text,
    FilePicker,
    Row,
    Column,
    Page,
    ElevatedButton,
    Image,
    Container,
    Switch,
    Markdown
)
from flet_core import (
    FilePickerResultEvent,
    icons,
    ImageFit,
    alignment,
    ThemeMode, MarkdownExtensionSet, TextStyle, ScrollMode, MainAxisAlignment, colors
)

md_content = """
# 这是Python课程设计-通讯录
> 应用技术学院-网络工程1班-翟宇涵
- [x] flet
- [x] sqlite3
- [x] pypinyin

```python
def main(page: ft.Page):
    page.theme_mode = ThemeMode.LIGHT
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
            contactList = clList.ContactList(contactPanel, page)  # 联系人列表
            contactSearch = clSearch.ContactSearch(contactList)  # 联系人搜索框
            contactPanel.BindContactList(contactList)
            page.views.append(
                View(
                    "/",
                    [Row(
                        [
                            MyAppBar(open_dlg, 0),
                            Container(expand=5, content=ft.Column([contactSearch,
                                                                   Row([contactList],
                                                                       expand=True,
                                                                       scroll=ft.ScrollMode.AUTO)])),
                            contactPanel,
                        ],
                        expand=True
                    )])
            )
            add_dlg.BindContactList(contactList)

        if page.route == "/group":
            page.views.append(
                View(
                    "/group",
                    [Row(
                        [
                            MyAppBar(open_dlg, 1),
                            Container(expand=10,
                                      content=Pages.GroupPage.GroupPage(page))
                        ],
                        expand=True
                    )])
            )
        if page.route == "/setting":
            page.views.append(
                View(
                    "/setting",
                    [Row(
                        [
                            MyAppBar(open_dlg, 2),
                            Pages.SettingPage.SettingPage(page)
                        ],
                        expand=True
                    )])
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
    page.update()
```
"""


class SettingPage(Column):
    def pick_file_event(self, e: FilePickerResultEvent):
        # map -> tuple -> list
        db_name = str()
        db_path = str()
        try:
            file_info = list(map(lambda f: (f.name, f.path), e.files))
            db_name = file_info[0][0]
            db_path = file_info[0][1]
        except Exception as e:
            print(e)

        if db_name:
            self.page.client_storage.set("DB_NAME", db_name)
            self.page.client_storage.set("DB_PATH", db_path)
            self.selected_files.value = db_name

        self.selected_files.update()

    def __init__(self, _page: Page):
        self.pick_files_dialog = FilePicker(on_result=self.pick_file_event)
        self.selected_files = Text()
        self.page = _page
        if _page.client_storage.contains_key("DB_NAME"):
            self.selected_files.value = _page.client_storage.get("DB_NAME")
            print("这里是设置界面")
        _page.overlay.append(self.pick_files_dialog)
        img = Image(
            src=f"/images/nuist.PNG",
            width=250,
            height=250,
            fit=ImageFit.CONTAIN,
        )

        def theme_changed(e):
            self.page.theme_mode = (
                ThemeMode.DARK
                if self.page.theme_mode == ThemeMode.LIGHT
                else ThemeMode.LIGHT
            )
            changThemeSwitch.label = (
                "浅色模式" if self.page.theme_mode == ThemeMode.LIGHT else "深色模式"
            )
            self.page.update()

        changThemeSwitch = Switch(label="浅色模式", on_change=theme_changed)
        super().__init__(
            expand=True,
            controls=[
                Container(
                    expand=4,
                    content=img,
                    alignment=alignment.top_center
                ),
                Container(
                    expand=5,
                    content=Column(
                        scroll=ScrollMode.ALWAYS,
                        controls=[Markdown(
                            md_content,
                            extension_set=MarkdownExtensionSet.GITHUB_FLAVORED,
                            code_theme="atom-one-dark",
                            code_style=TextStyle(font_family="Roboto Mono"),
                            selectable=True,
                        )]),
                ),
                Row(
                    alignment=MainAxisAlignment.END,
                    controls=[ElevatedButton(
                        "选择通讯录数据库文件",
                        icon=icons.FILE_OPEN,
                        on_click=lambda _: self.pick_files_dialog.pick_files(
                            allow_multiple=False,
                        ),
                    ),
                        self.selected_files,
                        changThemeSwitch

                    ]
                ),
            ])
