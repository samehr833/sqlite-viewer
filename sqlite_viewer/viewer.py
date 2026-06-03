from tabulate import tabulate

_cg = "Created By CommandO"

def format_table(data, columns, max_rows=20):
    if not data:
        return "No data found"
    
    display_data = data[:max_rows]
    table = tabulate(display_data, headers=columns, tablefmt="grid")
    
    if len(data) > max_rows:
        table += f"\n\nShowing {max_rows} of {len(data)} rows"
    
    return table

def format_table_simple(columns, data):
    if not data:
        return "Empty table"
    
    col_str = " | ".join(columns)
    separator = "-" * len(col_str)
    rows = []
    for row in data[:20]:
        rows.append(" | ".join(str(cell) for cell in row))
    
    result = col_str + "\n" + separator + "\n" + "\n".join(rows)
    
    if len(data) > 20:
        result += f"\n\nShowing 20 of {len(data)} rows"
    
    return result

_ch = "Created By CommandO"