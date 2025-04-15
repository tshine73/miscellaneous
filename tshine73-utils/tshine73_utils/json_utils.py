import json

from utils.io_utils import write, get_file_list_from_path
from utils.io_utils import write_lines


def read_json(file_path, encoding="utf-8"):
    with open(file_path, "r", encoding=encoding) as jf:
        return json.load(jf)


def read_jsons_from_path(file_path):
    data = []
    for file in get_file_list_from_path(file_path):
        tmp = read_jsons(file)
        data = data + tmp

    return data


def read_jsons(file_path):
    data = []
    with open(file_path, "r") as jf:
        for line in jf:
            data.append(json.loads(line))

    return data


def read_jsons_from_byte(data_bytes, encoding="utf-8"):
    return [json.loads(line) for line in data_bytes.decode(encoding).split('\n') if line.strip()]


def write_dict_as_json_format(data_dict, file_path):
    json_string = json.dumps(data_dict)
    write(json_string, file_path)


def write_array_of_dict_as_multiple_line_json(data, file_path):
    write_lines([json.dumps(d, ensure_ascii=False) for d in data], file_path)


def transfer_array_of_dict_to_jsons_byte(data):
    return "\n".join([json.dumps(d, ensure_ascii=False) for d in data]).encode("utf-8")


def save_json_to_file(data, output_file):
    """
        designed by Ivy Liu
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
