import json

path = "<add path here including file name>"
with open(path) as read_file:
    sample_string = read_file.read()

json_string = json.loads(sample_string)

all_headers = []
new_all_dics = [{}]
nominees = []
temp_row = {}
last_header = None


def run_for_roots(do_func):
    all_nominees = nominees.copy()

    while all_nominees:
        line = all_nominees.pop()
        if line:
            if isinstance(line, list):
                for item in line:
                    all_nominees.append(item)
            if isinstance(line, dict):
                keys = do_func(line)
                for key in keys:
                    all_nominees.append(line[key])


def get_headers(line):
    for key in line.keys():
        if key not in all_headers and not isinstance(line[key], list):
            all_headers.append(key)
    return list(line.keys())


def get_values(line):
    for header in all_headers:
        if header in line.keys():
            value = line[header]
            if not isinstance(value, (list, dict)):
                temp_row[header] = value
            if header == last_header:
                new_all_dics.append(temp_row.copy())
    return list(line.keys())


# prep list (all_nominees)
if isinstance(json_string, dict):
    nominees.append(json_string.copy())
    print("the root is a dict")
elif isinstance(json_string, list):
    print("the root is a list")
    for item in json_string:
        nominees.append(item.copy())
else:
    raise TypeError(f"the root is {type(json_string)}")


# get headers
run_for_roots(get_headers)
last_header = all_headers[-1]

# prep template list of dics
for h in all_headers:
    temp_row[h] = ""

# get values
run_for_roots(get_values)

# print everything
with open(f"{path}", "w") as write_file:
    for header in all_headers:
        write_file.write(f"{header},")
    write_file.write('\n')
    for row in new_all_dics[1:]:
        for header in all_headers:
            value = row[header]
            if "'" in str(value):
                value = str(value).replace("'", "")
            if ',' in str(value) or '"' in str(value):
                value = f'"{value}"'
            write_file.write(f"{value},")
        write_file.write('\n')