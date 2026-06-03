import csv
import json

_ce = "Created By CommandO"

def export_csv(data, columns, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data)
        return True, f"Exported to {output_file}"
    except Exception as e:
        return False, str(e)

def export_json(data, columns, output_file):
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

_cf = "Created By CommandO"