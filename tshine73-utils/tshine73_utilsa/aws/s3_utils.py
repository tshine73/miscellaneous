import logging
import os
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError


def is_key_exists_s3(bucket, key, profile_name=None):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
        print(f"Key: '{key}' found!")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Key: '{key}' does not exist!")
            return False
        else:
            print("Something else went wrong")
            raise


def get_object(bucket, key, profile_name=None):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client("s3")

    response = s3.get_object(Bucket=bucket, Key=key)
    object_bytes = response['Body'].read()

    return object_bytes


def upload_file_to_s3(file_name, bucket, object_name=None, profile_name=None):
    """Upload a file to an S3 bucket

    :param profile_name:
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client("s3")

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f"upload [{file_name}] to bucket [{bucket}/{object_name}] succeed")
    except ClientError as e:
        logging.error(e)
        return False

    return True


def write_object(bucket, key, data, profile_name=None):
    """
    Writes in-memory data to an S3 bucket with the specified key.

    :param bucket: The S3 bucket name.
    :param key: The object key in the bucket.
    :param data: The in-memory object data to be uploaded (e.g., bytes, string).
    :param profile_name: AWS named profile for session (optional).
    :return: True if the object was successfully written, otherwise False.
    """
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client("s3")

    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=data)
        print(f"Successfully written object to s3://{bucket}/{key}")
        return True
    except ClientError as e:
        print(e)
        return False


def get_file_folders(bucket_name, prefix=""):
    s3_client = boto3.client('s3')

    file_names = []

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        for obj in page['Contents']:
            file_names.append(obj["Key"])

    return file_names


def download_files(bucket_name, local_path, file_names, folders):
    for folder in folders:
        folder_path = Path.joinpath(Path(local_path), folder)
        folder_path.mkdir(parents=True, exist_ok=True)

    for file_name in file_names:
        download_file(bucket_name, file_name, local_path)


def download_file(bucket_name, file_name, local_path):
    local_path = Path(local_path)

    s3_client = boto3.client('s3')
    file_path = Path.joinpath(local_path, file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # file_path = os.path.join(local_path, file_name)
    # print(file_path)
    # os.makedirs(os.path.join(local_path, file_name), exist_ok=True)

    s3_client.download_file(
        bucket_name,
        file_name,
        str(file_path)
    )


def parse_s3_path(s3_path):
    o = urlparse(s3_path, allow_fragments=False)
    return o.netloc, o.path[1:]


def delete_path(bucket, s3_path):
    s3_client = boto3.client('s3')
    file_names, _ = get_file_folders(bucket, s3_path)

    for file_name in file_names:
        s3_client.delete_object(Bucket=bucket, Key=file_name)
        print("success deleted file s3://%s/%s" % (bucket, file_name))
