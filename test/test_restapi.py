from flask import json

from test_util import *


def test_status():
    response = client().get(f"{url}/status")
    assert req in response.data


def test_get_content_from_cms():
    response = client().post(
        f"{url}/getContent",
        data=json.dumps(request),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['message'] == msg1 or data['message'] == msg2


def test_get_content_from_cms_error_use_case():
    response = client().post(
        f"{url}/getContent",
        data=json.dumps(request_1),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    assert data['message'] == msg7 or data['message'] == msg2 or data['message'] == msg3 or \
           data['message'] == msg4 or \
           data['message'] == msg5 or data['message'] == msg6


def test_get_frames_from_s3_error_use_case():
    response = client().get(f"{url}/postContent?content_id=xyzb13")
    assert response.status_code == 200

    assert req1 in response.data or \
           req2 in response.data or \
           req3 in response.data


def test_get_frames_from_s3():
    response = client().get(f"{url}/postContent?content_id=xyzb13&title=Elephant")
    assert response.status_code == 200
    res_data = json.dumps(payload)
    data = json.loads(res_data)
    result = data['payload']
    assert result is not None and len(result) > 0


def test_delete_bucket_from_s3_error_use_case():
    response = client().delete(f"{url}/deleteContent")
    assert response.status_code == 200

    assert msg8 in response.data or msg10 in response.data or msg9 in response.data


def test_delete_bucket_from_s3():
    response = client().delete(f"{url}/deleteContent?content_id=xyzb13")
    assert response.status_code == 200

    assert msg8 in response.data or msg10 in response.data or msg9 in response.data


def test_update_bucket_at_s3():
    response = client().post(
        f"{url}/updateContent",
        data=json.dumps(request_2),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['message'] == msg12 or data['message'] == msg11 or data['message'] == msg3 or data['message'] == msg4 or \
           data['message'] == msg5 or data['message'] == msg6 or data['message'] == msg7
