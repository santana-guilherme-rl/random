import csv
import sys
from typing import List

_, file_1, file_2 = sys.argv

WIDTH = 40

#stack overflow
class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

	@classmethod
	def pcolor(cls, text: str, color: str) -> str:
		"""PutColor"""
		return f"{color}{text}{cls.END}"

#### table stuff
def return_rows(row: dict) -> str:
	rows_to_print = []
	for i in range(max(len(row["diff"]), len(row['diff2']))):
		title = row['file_name'][WIDTH*i:(WIDTH*i) + WIDTH]
		diff = row["diff"][i] if len(row['diff'])-1 >= i else ''
		diff2 = row['diff2'][i] if (len(row['diff2'])-1) >= i else ''
		rows_to_print.append(f"|{color.pcolor(title, color.BOLD) + ' '*(WIDTH-len(title))}|{diff + ' '*(WIDTH-(len(diff)))}|{diff2 + ' '*(WIDTH-len(diff2))}|")
	return '\n'.join(rows_to_print)

def print_table(table: List) -> None:
	"""
	Table is a list of dicts
	"""
	for row in table:
		horizontal = '-'*WIDTH
		print(f"|{horizontal}|{horizontal}|{horizontal}|")
		print(return_rows(row))
	print(color.pcolor(f"|{horizontal}|{horizontal}|{horizontal}|", color.BOLD))

### diff stuff
def build_file_dict(file_path):
    file_1_dict = {
        "meta": {
            "file_name": file_path
        },
        "data_elements": {}
    }
    with open(file_path, "r") as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader) # skip header
        for line in spamreader:
            key = line[4].split(":", 1)[-1].strip()
            file_1_dict['data_elements'][key] = file_1_dict["data_elements"].get(key, []) + [line[5]]
    return file_1_dict

def build_diff_dict(d1: dict, d2: dict):
    diff_dict = {
            "meta": [],
            "data_elements": []
    }
    d1_keys = set(d1['data_elements'].keys())
    d2_keys = set(d2['data_elements'].keys())
    d2_keys.update(d1_keys)

    for key in sorted(d2_keys):
        data_elements1 = set(sorted(d1['data_elements'].get(key, [])))
        data_elements2 = set(sorted(d2['data_elements'].get(key, [])))
        if data_elements1 != data_elements2:
            diff_dict["data_elements"].append({"file_name": key, "diff": list(data_elements1), "diff2": list(data_elements2)})
    return diff_dict


findings1 = build_file_dict(file_1)
findings2 = build_file_dict(file_2)
diff_dict = build_diff_dict(findings1, findings2)


f1_keys = set(findings1["data_elements"].keys())
f2_keys = set(findings2["data_elements"].keys())


print("Overall files")
print(f"Finding in 1 but not in 2: {f1_keys.difference(f2_keys)}\n\n\t------------------------\t\n")
print(f"Finding in 2 but not in 1: {f2_keys.difference(f1_keys)}\n\n")

print_table(diff_dict["data_elements"])




