import glob
import os
import shutil

import boto3
from PIL import Image
from botocore.exceptions import ClientError
from moviepy.video.io.VideoFileClip import VideoFileClip


def is_video_file_fine(video_file):
    try:
        clips = VideoFileClip(video_file)
        var = clips.duration
        clips.get_frame(2)
        clips.close()
        return True
    except IOError:
        return False


def is_frequency_valid(video_file, frequency):
    clips = VideoFileClip(video_file)
    video_duration = clips.duration
    return video_duration > frequency


def generate_frames(video_file, frequency, title, tempdir):
    try:
        clips = VideoFileClip(video_file)
        duration = clips.duration
        max_duration = int(duration) + 1

        i = 0
        while i < max_duration:
            if i == 0:
                frame = clips.get_frame(2)
                new_image_file = os.path.join(tempdir, f"{title}_{2}.jpg")
            else:
                frame = clips.get_frame(i)
                new_image_file = os.path.join(tempdir, f"{title}_{i}.jpg")

            new_image = Image.fromarray(frame)
            new_image.save(new_image_file)
            i = i + frequency

        clips.close()

    except IOError:
        print('Getting some issue to generate the frame, please check video metadata.')


def bucket_exists(bucket_name):
    global exists
    global access
    try:
        session = boto3.session.Session()
        # User can pass customized access key, secret_key and token as well
        s3_resource = session.resource('s3')
        s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        print("Bucket exists.", bucket_name)
        exists = True
        access = True
    except ClientError as error:
        error_code = int(error.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access! ", bucket_name)
            exists = True
            access = False
        elif error_code == 404:
            print("Bucket Does Not Exist!", bucket_name)
            exists = False
            access = False
    return exists, access


def delete_temp_dir(tempdir):
    print("upload image process done")
    shutil.rmtree(tempdir)


def upload_all_files(bucket_name, tempdir):
    files = glob.glob(tempdir + "/*")
    for file in files:
        print("my data: " + str(file))
        _upload_file(file, bucket_name)


def _upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    botoClient = boto3.client('s3')
    botoClient.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read',
                                                                      'ContentType': 'image/jpeg'})


def find_timestamp_in_sec(url, title):
    index = url.find(title)
    data = url[index:len(url)]
    return data


def extract_nbr(input_str):
    if input_str is None or input_str == '':
        return 0

    out_number = ''
    for ele in input_str:
        if ele.isdigit():
            out_number += ele
    return float(out_number)


def delete_file_from_s3(bucket_name):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    for my_bucket_object in my_bucket.objects.all():
        s3.Object(bucket_name, my_bucket_object.key).delete()


def replace_space(string):
    return string.replace(" ", "-")
