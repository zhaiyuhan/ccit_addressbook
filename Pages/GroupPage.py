from flet import (
    Text,
    PopupMenuButton,
    PopupMenuItem,
    Page,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    Column,
)
from flet_core import (
    icons, MainAxisAlignment, ScrollMode
)

from Foundation import DBService


class MyPopupMenuItem(PopupMenuItem):

    def __init__(self, db_name: str, group_name_item: str, db_datatable: DataTable):
        self.result = list()
        self.new_rows = list()

        def click_event(e):
            with DBService.DBService(db_name) as dbService:
                self.result = dbService.query_db_by_group('contactlist', group_name_item)
                print(self.result)
            for i in self.result:
                self.new_rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(i[1])),
                            DataCell(Text(i[2])),
                            DataCell(Text(i[3])),
                        ],
                    ),
                )
            if db_datatable.rows:
                db_datatable.rows.clear()
                db_datatable.update()
            db_datatable.rows = self.new_rows
            db_datatable.update()

        super().__init__(
            text=group_name_item,
            on_click=click_event
        )


class GroupPage(Column):

    def __init__(self, _page: Page):

        self.page = _page
        self.db_name = str()
        self.group_list = list()  # 分组列表
        self.group_list_item = list()  # 存放分组按钮item
        self.db_DataTable = DataTable(
            column_spacing=200,
            columns=[
                DataColumn(Text("姓名")),
                DataColumn(Text("手机号")),
                DataColumn(Text("通讯地址"), numeric=True),
            ], )
        if not self.page.client_storage.get("DB_PATH"):
            self.db_name = self.page.client_storage.get("DB_NAME")
        else:
            self.db_name = self.page.client_storage.get("DB_PATH")
        with DBService.DBService(db_name=self.db_name) as dbService:
            for _, group_name in dbService.query_db_all("grouplist"):
                self.group_list.append(group_name)
        for i in self.group_list:
            self.group_list_item.append(MyPopupMenuItem(self.db_name, i, self.db_DataTable))

        super().__init__(
            alignment=MainAxisAlignment.END,
            scroll=ScrollMode.ADAPTIVE,
            controls=[
                PopupMenuButton(
                    icon=icons.GROUP,
                    tooltip="切换分组",
                    items=self.group_list_item
                ),
                self.db_DataTable
            ])
