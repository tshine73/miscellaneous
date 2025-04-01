def camel_to_snake(camel_case):
    result = [camel_case[0].lower()]

    for char in camel_case[1:]:
        if char.isupper():
            result.extend(['_', char.lower()])
        else:
            result.append(char)

    return ''.join(result)


def replace_windows_path_to_unix_path(path):
    """
        designed by Ivy Liu
    """
    return path.replace("\\", "/")
