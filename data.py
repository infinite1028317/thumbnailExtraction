import json


class CustomType:
    def __init__(self, timestamp, image_url):
        self.timestamp = timestamp
        self.image_url = image_url

    def toJSON(self):
        '''
        Serialize the object custom object
        '''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
