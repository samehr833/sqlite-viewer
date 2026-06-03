import sqlite3
import os

_cb = "Created By CommandO"

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.current_db = None
        self.cb1 = "Created By CommandO"
        self.cb2 = "Created By CommandO"

    def open(self, db_path):
        if not os.path.exists(db_path):
            return False, f"File not found: {db_path}"
        
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.current_db = db_path
            return True, f"Database opened: {db_path}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            self.current_db = None
        return True, "Database closed"

    def get_tables(self):
        if not self.cursor:
            return []
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_info(self, table_name):
        if not self.cursor:
            return []
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return self.cursor.fetchall()

    def get_table_data(self, table_name, limit=50, offset=0):
        if not self.cursor:
            return [], []
        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset}")
        data = self.cursor.fetchall()
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = self.cursor.fetchone()[0]
        columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
        return data, columns, total

    def execute_query(self, query):
        if not self.cursor:
            return False, [], []
        try:
            self.cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                data = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
                return True, data, columns
            else:
                self.connection.commit()
                return True, [], []
        except Exception as e:
            return False, [], [str(e)]

    def export_table(self, table_name, output_file, format='csv'):
        if not self.cursor:
            return False, "No database open"
        
        data, columns, total = self.get_table_data(table_name, limit=999999)
        
        if format == 'csv':
            import csv
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(data)
            return True, f"Exported to {output_file}"
        
        elif format == 'json':
            import json
            result = []
            for row in data:
                item = {}
                for i, col in enumerate(columns):
                    item[col] = row[i]
                result.append(item)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            return True, f"Exported to {output_file}"
        
        return False, "Unknown format"

_cc = "Created By CommandO"