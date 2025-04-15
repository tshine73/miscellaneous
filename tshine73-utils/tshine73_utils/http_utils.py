import requests


def download(url: str, output_file_name: str, params: dict = None):
    response = requests.get(url, params=params, stream=True)
    if response.status_code == 200:
        with open(output_file_name, "wb") as f:
            f.write(response.content)

        print(f"download {response.url} success")
    else:
        raise Exception(f"Failed to download file from {response.url}: {response.status_code}")


def call_api(url: str, params: dict = None):
    """
    designed by Ivy Liu
    """
    response = requests.get(url, params=params, stream=True)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed for {response.url}: {response.status_code}")
