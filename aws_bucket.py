import json
import tempfile
import threading

import botocore
from botocore.config import Config

from data import CustomType

from util import *


# save frames api
def save_frames(video_file, frequency, bucket_name, title):
    new_title = replace_space(title)
    tempdir = tempfile.mkdtemp(prefix="frames-")

    client = boto3.client('s3')
    client.create_bucket(Bucket=bucket_name)

    thread = threading.Thread(target=generate_frames, args=(video_file, frequency, new_title, tempdir,))
    thread.start()
    thread.join()

    # upload file to s3 bucket
    thread1 = threading.Thread(target=upload_all_files, args=(bucket_name, tempdir))
    thread1.start()
    thread1.join()

    # Delete temp dir
    thread2 = threading.Thread(target=delete_temp_dir, args=(tempdir,))
    thread2.start()


# get frames api
def get_data_from_aws_bucket(bucket_name, title):
    new_title = replace_space(title)
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    data_list = []

    for my_bucket_object in my_bucket.objects.all():
        my_config = Config(signature_version=botocore.UNSIGNED)
        url = boto3.client("s3", config=my_config).generate_presigned_url(
            "get_object", ExpiresIn=0, Params={"Bucket": bucket_name, "Key": my_bucket_object.key}
        )

        key = find_timestamp_in_sec(url, new_title)
        obj = CustomType(extract_nbr(key), url)
        data_list.append(json.loads(obj.toJSON()))

    data_list.sort(key=lambda x: x["timestamp"])
    response = {"payload": data_list}
    return json.dumps(response)


# delete frames api
def delete_aws_bucket(bucket_name):
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket_name)
    s3_bucket.objects.all().delete()
    s3_bucket.delete()
    return f"{bucket_name} is removed from s3 successfully."


# update frames api
def update_aws_bucket(video_file, frequency, bucket_name, title):
    new_title = replace_space(title)
    tempdir = tempfile.mkdtemp(prefix="frames-")
    # Generate frames
    thread = threading.Thread(target=generate_frames, args=(video_file, frequency, new_title, tempdir,))
    thread.start()
    thread.join()

    # delete bucket from s3
    thread1 = threading.Thread(target=delete_file_from_s3, args=(bucket_name,))
    thread1.start()
    thread.join()

    # upload file to s3 bucket
    thread2 = threading.Thread(target=upload_all_files, args=(bucket_name, tempdir,))
    thread2.start()
    thread2.join()

    # Delete temp dir
    thread3 = threading.Thread(target=delete_temp_dir, args=(tempdir,))
    thread3.start()
