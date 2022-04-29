from settings import create_app

url = 'http://127.0.0.1:5000/api'


def client():
    flask_app = create_app()
    return flask_app.test_client()


request = {
    "video_file": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "frequency": 60,
    "content_id": "xyzb13",
    "title": "Elephant"
}

request_2 = {
    "video_file": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "frequency": 10,
    "content_id": "xyzb13",
    "title": "Elephant"
}

request_1 = {
            "video_file": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
            "frequency": 0,
            "content_id": "",
            "title": "Elephants Dream"
        }

payload = {
        "payload": [
            {
                "image_url": "https://xyzbc13.s3.amazonaws.com/Elephant_2.jpg",
                "timestamp": 2.0
            },
            {
                "image_url": "https://xyzbc13.s3.amazonaws.com/Elephant_120.jpg",
                "timestamp": 120.0
            }
        ]
    }

msg1 = 'PIP generate event is triggered, please wait for processing...'
msg2 = 'Bucket is already exist. or Private Bucket. Forbidden Access'
msg3 = 'Request parameter should not be null.'
msg4 = 'Request parameter should not be empty or null.'
msg5 = 'Getting some issue to generate the frame, please check video metadata.'
msg6 = 'The frequency should be less then video duration'
msg7 = 'Request data has some issue please check.'
msg11 = 'Bucket does not exist. or Private Bucket. Forbidden Access'
msg12 = 'PIP update event is triggered, please wait for processing...'

msg8 = b'{"message":"content id should not be null."}'
msg9 = b'{"message":"xyzb13 is removed from s3 successfully."}'
msg10 = b'{"message":"Bucket is not found. or Private Bucket. Forbidden Access"}'

req = b'{"payload":"ip and port working fine..."}'
req1 = b'{"message":"Either content id or title should not be null."}'
req2 = b'{"message":"Either content id or title should not be empty."}'
req3 = b'{"message":"Bucket is not found. or Private Bucket. Forbidden Access"}'
