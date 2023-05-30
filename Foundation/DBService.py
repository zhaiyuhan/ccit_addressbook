import sqlite3


class DBService:
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    # 创建表 参数:表的名称
    def create_table(self, table_name: str):
        try:
            self.cur.execute(table_name)
        except Exception as e:
            print(e)

    # 插入数据 参数:表的名称 插入数据(字典类型)
    def insert_db(self, table_name: str, record: dict):
        insert_key = str()
        insert_value = str()
        for key, value in record.items():
            insert_key = insert_key + key + ','
            insert_value = insert_value + '\'' + value + '\'' + ','
        insert_value = insert_value[0:len(insert_value) - 1]
        insert_key = insert_key[0:len(insert_key) - 1]
        insert_str = '''INSERT INTO {table_name}({key})VALUES ({value})''' \
            .format(table_name=table_name, key=insert_key, value=insert_value)
        try:
            self.con.execute(insert_str)
            self.con.commit()
        except Exception as e:
            print(e)

    def query_db_all(self, table_name: str):
        try:
            self.cur.execute(f'SELECT * FROM {table_name}')
            result = []
            for row in self.cur:
                result.append(row)
            self.con.commit()
            return result
        except Exception as e:
            print(e)
            return []

    def query_db_by_name(self, table_name: str, contact_name: str):
        results = self.cur.execute(f'''SELECT * FROM {table_name} WHERE name = '{contact_name}';''')
        return results.fetchall()

    def query_db_by_group(self, table_name: str, group_name: str):
        results = self.cur.execute(f'''SELECT * FROM {table_name} WHERE address_group = '{group_name}';''')
        return results.fetchall()

    def query_db_by_name_fuzzy(self, table_name: str, contact_name: str):
        results = self.cur.execute(f'''SELECT * FROM {table_name} WHERE name LIKE '%{contact_name}%';''')
        return results.fetchall()

    def delete_by_name(self, table_name: str, contact_name: str):
        self.cur.execute(f'''DELETE FROM {table_name} WHERE name= '{contact_name}';''')
        self.con.commit()

    def update_db_by_id(self, table_name: str, contact_id: int, update_record: list):
        update_str = '''UPDATE {table_name} SET name = '{new_name}', tel = '{new_tel}', 
        address = '{new_address}' WHERE id = '{contact_id}';''' \
            .format(table_name=table_name, new_name=update_record[0], new_tel=update_record[1],
                    new_address=update_record[2], contact_id=contact_id)
        try:
            self.con.execute(update_str)
        except Exception as e:
            print(e)
        self.con.commit()

    def close_db(self):
        self.cur.close()
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_db()
