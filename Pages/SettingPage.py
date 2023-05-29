from flet import (
    Text,
    FilePicker,
    Row,
    Page,
    ElevatedButton
)
from flet_core import (
    FilePickerResultEvent,
    icons
)


class SettingPage(Row):
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
        if _page.client_storage.contains_key("DB_NAME"):
            self.selected_files.value = _page.client_storage.get("DB_NAME")
            print("这里是设置界面")
        _page.overlay.append(self.pick_files_dialog)

        super().__init__(controls=[
            ElevatedButton(
                "选择通讯录数据库文件",
                icon=icons.FILE_OPEN,
                on_click=lambda _: self.pick_files_dialog.pick_files(
                    allow_multiple=False,
                    # allowed_extensions=["db"]
                ),
            ),
            self.selected_files,
        ])
