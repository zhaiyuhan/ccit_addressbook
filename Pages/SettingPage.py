from flet import (
    FilePicker,
    Row,
    Page,
)
import flet as ft
from flet_core import (
    FilePickerResultEvent,
    icons
)


class SettingPage(Row):
    def pick_file_event(self, e: FilePickerResultEvent):
        print(e.files)
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.selected_files.update()

    def __init__(self, _page: Page):
        self.pick_files_dialog = FilePicker(on_result=self.pick_file_event)
        self.selected_files = ft.Text()
        print(type(_page))
        if _page.client_storage.contains_key("DB_NAME"):
            self.selected_files.value = _page.client_storage.get("DB_NAME")
            print("这里是设置界面 查询到了数据库文件")
        _page.overlay.append(self.pick_files_dialog)

        super().__init__(controls=[
            ft.ElevatedButton(
                "选择通讯录数据库文件",
                icon=icons.FILE_OPEN,
                on_click=lambda _: self.pick_files_dialog.pick_files(
                    allow_multiple=False,
                    # allowed_extensions=["db"]
                ),
            ),
            self.selected_files,
        ])
