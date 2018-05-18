import requests
#https://global.download.synology.com/download/Document/DeveloperGuide/Surveillance_Station_Web_API_v2.0.pdf

class SurveillanceCameraApi:
    """An implementation of a Synology SurveillanceStation API."""

    def get_sid(self, base_url, username, password):

        payload = {'api': 'SYNO.API.Auth',
                   'method': 'Login',
                   'version': 6,
                   'account': username,
                   'passwd': password,
                   'session': 'SurveillanceStation',
                   'format':'sid'}
        r = requests.get(base_url + 'auth.cgi', params=payload)
        content = r.json()
        return content['data']['sid']

    def get_camera_by_name(self, camera_name):
        camera = {}
        payload = {'api': 'SYNO.SurveillanceStation.Camera',
                   'method': 'List',
                   'version': 6,
                   '_sid': self._sid}
        r = requests.get(self._base_url + 'entry.cgi', params=payload)
        content = r.json()
        for cam in content['data']['cameras']:
            if cam["name"] == camera_name:
                camera = cam
                break
        return camera

    def enable_camera(self, cameraIds):
        payload = {'api': 'SYNO.SurveillanceStation.Camera',
                   'method': 'Enable',
                   'version': 6,
                   'cameraIds': cameraIds,
                   '_sid': self._sid}
        r = requests.get(self._base_url + 'entry.cgi', params=payload)
        content = r.json()
        return content['success']

    def disable_camera(self, cameraIds):
        payload = {'api': 'SYNO.SurveillanceStation.Camera',
                   'method': 'Disable',
                   'version': 6,
                   'cameraIds': cameraIds,
                   '_sid': self._sid}
        r = requests.get(self._base_url + 'entry.cgi', params=payload)
        content = r.json()
        return content['success']

    def __init__(self, base_url, account, password):
        """Initialize a Synology Surveillance API."""
        print 'Starting surveillance API'
        self._base_url = base_url + '/webapi/'
        self._account = account
        self._password = password
        self._sid = self.get_sid(self._base_url, self._account, self._password)