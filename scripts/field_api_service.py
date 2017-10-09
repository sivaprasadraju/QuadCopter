import grequests

class FieldAPIService:
    def __init__(self):
        self.domain = 'https://apiprod.aconex.com'

    def send_create_issue_request(self, issue):
        requests = [grequests.put(
            self.domain + '/field-management/api/projects/1879048279/areas/' + issue.get_area_id() + '/issues/' + issue.get_id(),
            data = issue.to_json(),
            auth = ('mjenner', 'Auth3nt1c'),
            headers = {
                'X-application': '63fc4887-aed9-497f-bad5-d7ef2b90cdaf',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )]
        grequests.map(requests, exception_handler=self.exception_handler)
        print('issue captured')

    def send_attach_photo_to_issue_request(self, issue, filename):
        requests = [grequests.post(
            self.domain + '/field/api/1879048279/issues/' + issue.get_id() + '/attachments',
            files = { 'file': (filename, open(filename, 'rb'), 'image/jpeg')},
            auth = ('mjenner', 'Auth3nt1c'),

        )]
        grequests.map(requests, exception_handler=self.exception_handler)
        print('image uploaded')

    def exception_handler(request, exception):
        print(exception)