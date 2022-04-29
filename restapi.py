import threading

from flask import Blueprint, request, jsonify

from botocore.exceptions import *

from error_utility import *

content_api = Blueprint('api', __name__)


@content_api.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    return jsonify({'sum': data['a'] + data['b']})


@content_api.route('/status', methods=['GET'])
def get_status():
    return jsonify({'payload': 'ip and port working fine...'})


@content_api.route('/getContent', methods=['POST'])
def get_content_from_cms():
    try:
        data = request.get_json()

        video_file = data["video_file"]
        frequency = data["frequency"]
        content_id = data["content_id"]
        title = data["title"]

        msg = validate_generate_frame_request(video_file, frequency, content_id, title)
        if msg != '':
            return jsonify({'message': msg})

        thread = threading.Thread(target=aws_bucket.save_frames, args=(video_file, frequency
                                                                       , content_id, title))
        thread.start()

        return jsonify({'message': 'PIP generate event is triggered, please wait for processing...'})
    except ParamValidationError as er:
        return jsonify({'message': 'The parameters you provided are incorrect: {}'.format(er)})
    except ClientError as error:
        error_http_code = int(error.response['Error']['Code'])
        error_msg = int(error.response['Error']['Message'])
        return jsonify({'error_code': str(error_http_code), 'message': error_msg})
    except KeyError:
        return jsonify({'message': 'Request data has some issue please check.'})


@content_api.route('/postContent', methods=['GET'])
def get_frames_from_s3():
    try:
        args = request.args
        content_id = args.get('content_id')
        title = args.get('title')

        msg = validate_get_frame_from_s3(content_id, title)

        if msg != '':
            return jsonify({'message': msg})

        return aws_bucket.get_data_from_aws_bucket(content_id, title)

    except ParamValidationError as er:
        return jsonify({'message': 'The parameters you provided are incorrect: {}'.format(er)})
    except ClientError as error:
        error_http_code = int(error.response['Error']['Code'])
        error_msg = int(error.response['Error']['Message'])
        return jsonify({'error_code': str(error_http_code), 'message': error_msg})
    except KeyError:
        return jsonify({'message': 'Request data has some issue please check.'})


@content_api.route('/deleteContent', methods=['DELETE'])
def delete_bucket_from_s3():
    try:
        args = request.args
        content_id = args.get('content_id')

        msg = validate_delete_bucket_from_s3(content_id)

        if msg != '':
            return jsonify({'message': msg})

        return_value = aws_bucket.delete_aws_bucket(content_id)
        return jsonify({'message': return_value})

    except ParamValidationError as er:
        return jsonify({'message': 'The parameters you provided are incorrect: {}'.format(er)})
    except ClientError as error:
        error_http_code = int(error.response['Error']['Code'])
        error_msg = int(error.response['Error']['Message'])
        return jsonify({'error_code': str(error_http_code), 'message': error_msg})
    except KeyError:
        return jsonify({'message': 'Request data has some issue please check.'})


@content_api.route('/updateContent', methods=['POST'])
def update_bucket_at_s3():
    try:
        data = request.get_json()

        video_file = data["video_file"]
        frequency = data["frequency"]
        content_id = data["content_id"]
        title = data["title"]

        msg = validate_update_bucket_at_s3(video_file, frequency, content_id, title)
        if msg != '':
            return jsonify({'message': msg})

        thread = threading.Thread(target=aws_bucket.update_aws_bucket, args=(data["video_file"], data["frequency"]
                                                                             , data["content_id"], data["title"]))
        thread.start()

        return jsonify({'message': 'PIP update event is triggered, please wait for processing...'})

    except ParamValidationError as er:
        return jsonify({'message': 'The parameters you provided are incorrect: {}'.format(er)})
    except ClientError as error:
        error_http_code = int(error.response['Error']['Code'])
        error_msg = int(error.response['Error']['Message'])
        return jsonify({'error_code': str(error_http_code), 'message': error_msg})
    except KeyError:
        return jsonify({'message': 'Request data has some issue please check.'})
