import aws_bucket


def validate_generate_frame_request(video_file, frequency, content_id, title):
    if content_id is None or video_file is None or frequency is None or title is None:
        return 'Request parameter should not be null.'

    if title == '' or video_file == '' or frequency == '' or content_id == '':
        return 'Request parameter should not be empty or null.'

    if not aws_bucket.is_video_file_fine(video_file):
        return 'Getting some issue to generate the frame, please check video metadata.'

    if not aws_bucket.is_frequency_valid(video_file, frequency):
        return 'The frequency should be less then video duration'

    exists, access = aws_bucket.bucket_exists(content_id)
    if exists:
        return 'Bucket is already exist. or Private Bucket. Forbidden Access'

    return ''


def validate_get_frame_from_s3(content_id, title):
    if content_id is None or title is None:
        return 'Either content id or title should not be null.'

    if content_id == '' or title == '':
        return 'Either content id or title should not be empty.'

    exists, access = aws_bucket.bucket_exists(content_id)
    if (not access and exists) or (not access and not exists):
        return 'Bucket is not found. or Private Bucket. Forbidden Access'

    return ''


def validate_delete_bucket_from_s3(content_id):
    if content_id is None:
        return 'content id should not be null.'

    exists, access = aws_bucket.bucket_exists(content_id)
    if (not access and exists) or (not access and not exists):
        return 'Bucket is not found. or Private Bucket. Forbidden Access'

    return ''


def validate_update_bucket_at_s3(video_file, frequency, content_id, title):
    if content_id is None or video_file is None or frequency is None or title is None:
        return 'Request parameter should not be null.'

    if title == '' or video_file == '' or frequency == '' or content_id == '':
        return 'Request parameter should not be empty or null.'

    if not aws_bucket.is_video_file_fine(video_file):
        return 'Getting some issue to generate the frame, please check video metadata.'

    if not aws_bucket.is_frequency_valid(video_file, frequency):
        return 'The frequency should be less then video duration'

    exists, access = aws_bucket.bucket_exists(content_id)
    if (exists and not access) or (not exists and not access):
        return 'Bucket does not exist. or Private Bucket. Forbidden Access'

    return ''
