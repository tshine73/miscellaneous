import os


def write(data, file_name):
    with open(file_name, 'w') as f:
        f.write(data)


def write_lines(lines, file_name):
    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line + "\n")


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def read_file(file_name):
    data = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            data.append(line.strip())

    return data


def read_from_bytes(data_bytes, encoding="utf-8"):
    return [line for line in data_bytes.decode(encoding).split('\n') if line.strip()]


def get_file_suffix(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension


def get_file_list_from_path(file_path):
    files = []
    for names in os.listdir(file_path):
        files.append(os.path.join(file_path, names))

    return files


def mkdir_if_not_exists(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        print(f"path {path} has been created")


def get_directory_from_path(file_path):
    return os.path.dirname(file_path)


def move_data(src_file, dest_file):
    """Move data from source file to destination file."""
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"source file [{src_file}] does not exist.")

    with open(src_file, "r") as f_src, open(dest_file, "w") as f_dest:
        f_dest.write(f_src.read())

    # Remove source file only after successful write
    os.remove(src_file)
    print(f"source file [{src_file}] has been moved to [{dest_file}].")
