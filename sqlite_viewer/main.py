#!/usr/bin/env python3

import sys
import os
import sqlite3
import json
import csv
import platform

_cb1 = "Created By CommandO"
_cb2 = "Created By CommandO"
_cb3 = "Created By CommandO"

SYSTEM = platform.system()

def clear_screen():
    if SYSTEM == "Windows":
        os.system('cls')
    else:
        os.system('clear')

ASCII_ART = """
 ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▖  ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄  ▗▄▖ 
▐▌   ▐▌ ▐▌▐▛▚▞▜▌▐▛▚▞▜▌▐▌ ▐▌▐▛▚▖▐▌▐▌  █▐▌ ▐▌
▐▌   ▐▌ ▐▌▐▌  ▐▌▐▌  ▐▌▐▛▀▜▌▐▌ ▝▜▌▐▌  █▐▌ ▐▌
▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▐▌  ▐▌▐▌ ▐▌▐▌  ▐▌▐▙▄▄▀▝▚▄▞▘
"""
print(f"\n{'='*60}")
print(f"SQLite Viewer - Created By CommandO")
print(f"In Collaboration With XR Studio")
print(f"{'='*60}\n")

CONFIG_FILE = os.path.expanduser("~/.sqlite_viewer_config.json")
CURRENT_PATH = os.getcwd()

def load_last_db():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_db', None)
    return None

def save_last_db(db_path):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'last_db': db_path}, f)

def format_table(columns, data, max_rows=20):
    if not data:
        return "No data found"
    
    col_widths = [len(col) for col in columns]
    for row in data[:max_rows]:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    header = "| " + " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns)) + " |"
    
    rows = []
    for row in data[:max_rows]:
        row_str = "| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + " |"
        rows.append(row_str)
    
    result = separator + "\n" + header + "\n" + separator + "\n" + "\n".join(rows) + "\n" + separator
    
    if len(data) > max_rows:
        result += f"\n\nShowing {max_rows} of {len(data)} rows"
    
    return result

def list_directory(path):
    items = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                items.append({'name': item, 'type': 'dir', 'path': item_path})
            else:
                size = os.path.getsize(item_path)
                items.append({'name': item, 'type': 'file', 'path': item_path, 'size': size})
    except PermissionError:
        return [{'name': 'Permission denied', 'type': 'error'}]
    
    items.sort(key=lambda x: (x['type'] != 'dir', x['name'].lower()))
    return items

def format_directory(items, current_path):
    result = f"\nCurrent Directory: {current_path}\n"
    result += "=" * 60 + "\n"
    result += " 0  | .. (Go back)\n"
    
    idx = 1
    for item in items:
        if item['type'] == 'dir':
            result += f" {idx:2} | [DIR]  {item['name']}\n"
        elif item['type'] == 'file':
            result += f" {idx:2} | [FILE] {item['name']} ({item['size']} bytes)\n"
        else:
            result += f" {idx:2} | [ERR]  {item['name']}\n"
        idx += 1
    
    result += "=" * 60 + "\n"
    return result, items

class SQLiteViewer:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.current_db = None
        self.running = True
        self.current_path = CURRENT_PATH

    def print_banner(self):
        clear_screen()
        print(ASCII_ART)
        print(f"SQLite Viewer - Created By CommandO [{SYSTEM}]")
        print("=" * 60)
        if self.current_db:
            print(f"Connected to: {self.current_db}")
        print()

    def print_main_menu(self):
        print("=" * 60)
        print("MAIN MENU - Enter number:")
        print("=" * 60)
        print("  1  | Open SQLite database")
        print("  2  | Show tables")
        print("  3  | View table data")
        print("  4  | Execute SQL query")
        print("  5  | Export table to CSV")
        print("  6  | Export table to JSON")
        print("  7  | Close database")
        print("  8  | Browse files")
        print("  0  | Exit")
        print("=" * 60)
        print("Created By CommandO | In Collaboration With XR Studio")

    def wait_for_enter(self):
        input("\nPress Enter to continue...")

    def browse_and_open_file(self):
        while True:
            items = list_directory(self.current_path)
            dir_text, dir_items = format_directory(items, self.current_path)
            clear_screen()
            self.print_banner()
            print(dir_text)
            
            choice = input("\nEnter number (0=back, b=main menu): ").strip()
            
            if choice.lower() == 'b':
                return None
            
            if choice == '0':
                parent = os.path.dirname(self.current_path)
                if parent != self.current_path:
                    self.current_path = parent
                continue
            
            try:
                num = int(choice)
                if 1 <= num <= len(dir_items):
                    selected = dir_items[num-1]
                    if selected['type'] == 'dir':
                        self.current_path = selected['path']
                    elif selected['type'] == 'file':
                        if selected['name'].endswith('.db') or selected['name'].endswith('.sqlite') or selected['name'].endswith('.sqlite3'):
                            return selected['path']
                        else:
                            print(f"Not a database file: {selected['name']}")
                            self.wait_for_enter()
                    continue
            except ValueError:
                pass
            
            if os.path.exists(choice):
                if os.path.isdir(choice):
                    self.current_path = choice
                elif choice.endswith('.db') or choice.endswith('.sqlite') or choice.endswith('.sqlite3'):
                    return choice
                else:
                    print("Not a database file")
                    self.wait_for_enter()
            else:
                print(f"Path not found: {choice}")
                self.wait_for_enter()

    def open_db(self, db_path):
        if not os.path.exists(db_path):
            return False, f"File not found: {db_path}"
        
        try:
            if self.connection:
                self.connection.close()
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.current_db = db_path
            return True, f"Database opened: {db_path}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def close_db(self):
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

    def get_table_data(self, table_name, limit=50):
        if not self.cursor:
            return [], []
        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
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

    def export_csv(self, table_name, output_file):
        if not self.cursor:
            return False, "No database open"
        
        data, columns, total = self.get_table_data(table_name, 999999)
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(data)
            return True, f"Exported to {output_file}"
        except Exception as e:
            return False, str(e)

    def export_json(self, table_name, output_file):
        if not self.cursor:
            return False, "No database open"
        
        data, columns, total = self.get_table_data(table_name, 999999)
        
        try:
            result = []
            for row in data:
                item = {}
                for i, col in enumerate(columns):
                    item[col] = row[i]
                result.append(item)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            return True, f"Exported to {output_file}"
        except Exception as e:
            return False, str(e)

    def run(self):
        last_db = load_last_db()
        if last_db and os.path.exists(last_db):
            success, msg = self.open_db(last_db)
        
        while self.running:
            self.print_banner()
            self.print_main_menu()
            
            try:
                cmd = input("\n> ").strip().lower()
                
                if cmd == "1" or cmd == "open":
                    db_path = self.browse_and_open_file()
                    if db_path:
                        success, msg = self.open_db(db_path)
                        clear_screen()
                        self.print_banner()
                        print(msg)
                        if success:
                            save_last_db(db_path)
                    self.wait_for_enter()
                
                elif cmd == "2" or cmd == "show":
                    clear_screen()
                    self.print_banner()
                    if not self.current_db:
                        print("No database open. Use option 1 first")
                    else:
                        tables = self.get_tables()
                        if tables:
                            print("\nTABLES:")
                            print("-" * 40)
                            for t in tables:
                                print(f"  - {t}")
                        else:
                            print("No tables found")
                    self.wait_for_enter()
                
                elif cmd == "3" or cmd == "view":
                    clear_screen()
                    self.print_banner()
                    if not self.current_db:
                        print("No database open. Use option 1 first")
                    else:
                        tables = self.get_tables()
                        if not tables:
                            print("No tables found")
                        else:
                            print("\nAvailable tables:")
                            for i, t in enumerate(tables, 1):
                                print(f"  {i}. {t}")
                            choice = input("\nEnter table name or number: ").strip()
                            try:
                                num = int(choice)
                                if 1 <= num <= len(tables):
                                    table = tables[num-1]
                                else:
                                    table = choice
                            except:
                                table = choice
                            
                            limit = input("Rows to show (default 50): ").strip()
                            limit = int(limit) if limit.isdigit() else 50
                            data, columns, total = self.get_table_data(table, limit)
                            if data:
                                print(f"\nTable: {table} (Total rows: {total})")
                                print(format_table(columns, data))
                            else:
                                print(f"No data in table '{table}'")
                    self.wait_for_enter()
                
                elif cmd == "4" or cmd == "query":
                    clear_screen()
                    self.print_banner()
                    if not self.current_db:
                        print("No database open. Use option 1 first")
                    else:
                        query = input("Enter SQL query: ").strip()
                        success, data, columns = self.execute_query(query)
                        if success:
                            if data:
                                print(format_table(columns, data))
                            else:
                                print("Query executed successfully (no results)")
                        else:
                            print(f"Error: {columns[0] if columns else 'Unknown error'}")
                    self.wait_for_enter()
                
                elif cmd == "5" or cmd == "export":
                    clear_screen()
                    self.print_banner()
                    if not self.current_db:
                        print("No database open. Use option 1 first")
                    else:
                        tables = self.get_tables()
                        if not tables:
                            print("No tables found")
                        else:
                            print("\nAvailable tables:")
                            for i, t in enumerate(tables, 1):
                                print(f"  {i}. {t}")
                            choice = input("\nEnter table name or number: ").strip()
                            try:
                                num = int(choice)
                                if 1 <= num <= len(tables):
                                    table = tables[num-1]
                                else:
                                    table = choice
                            except:
                                table = choice
                            
                            output = input("Output file name (table.csv): ").strip()
                            if not output:
                                output = f"{table}.csv"
                            if not output.endswith('.csv'):
                                output += '.csv'
                            success, msg = self.export_csv(table, output)
                            print(msg)
                    self.wait_for_enter()
                
                elif cmd == "6" or cmd == "exportj":
                    clear_screen()
                    self.print_banner()
                    if not self.current_db:
                        print("No database open. Use option 1 first")
                    else:
                        tables = self.get_tables()
                        if not tables:
                            print("No tables found")
                        else:
                            print("\nAvailable tables:")
                            for i, t in enumerate(tables, 1):
                                print(f"  {i}. {t}")
                            choice = input("\nEnter table name or number: ").strip()
                            try:
                                num = int(choice)
                                if 1 <= num <= len(tables):
                                    table = tables[num-1]
                                else:
                                    table = choice
                            except:
                                table = choice
                            
                            output = input("Output file name (table.json): ").strip()
                            if not output:
                                output = f"{table}.json"
                            if not output.endswith('.json'):
                                output += '.json'
                            success, msg = self.export_json(table, output)
                            print(msg)
                    self.wait_for_enter()
                
                elif cmd == "7" or cmd == "close":
                    clear_screen()
                    self.print_banner()
                    success, msg = self.close_db()
                    print(msg)
                    self.wait_for_enter()
                
                elif cmd == "8" or cmd == "browse":
                    db_path = self.browse_and_open_file()
                    if db_path:
                        success, msg = self.open_db(db_path)
                        clear_screen()
                        self.print_banner()
                        print(msg)
                        if success:
                            save_last_db(db_path)
                    self.wait_for_enter()
                
                elif cmd == "0" or cmd == "exit":
                    clear_screen()
                    print(ASCII_ART)
                    print("\nGoodbye - Created By CommandO")
                    print("=" * 60)
                    self.close_db()
                    self.running = False
                
                else:
                    clear_screen()
                    self.print_banner()
                    print(f"Unknown command: {cmd}")
                    print("Please enter a number from 0 to 8")
                    self.wait_for_enter()
            
            except KeyboardInterrupt:
                clear_screen()
                print(ASCII_ART)
                print("\nGoodbye - Created By CommandO")
                print("=" * 60)
                self.close_db()
                self.running = False
            except Exception as e:
                print(f"Error: {e}")
                self.wait_for_enter()

if __name__ == "__main__":
    app = SQLiteViewer()
    app.run()

_cc1 = "Created By CommandO"
_cc2 = "Created By CommandO"
_cc3 = "Created By CommandO"