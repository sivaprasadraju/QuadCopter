import json
import uuid

class Issue:
    def __init__(self, gps_coord):
        self.id = str(uuid.uuid4())
        self.area_id = '271341877551151953'
        self.latitude = str(gps_coord['latitude'])
        self.longitude = str(gps_coord['longitude'])
        self.altitude =  str(gps_coord['altitude'])

    def to_json(self):
        return json.dumps({
            'description': 'Pipe is broken',
            'issue_type': {
                'id': 271341877549072763,
                'name': 'Defect'
            },
            'location_detail': 'Latitude: ' + self.latitude + 'N Longitude:' + self.longitude + 'E Altitude:' + self.altitude + 'mts',
            'area': {
                'id': self.area_id
            },
            'issue_id': self.id,
        })

    def get_area_id(self):
        return self.area_id


    def get_id(self):
        return self.id

