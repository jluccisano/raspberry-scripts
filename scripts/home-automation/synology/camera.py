import requests
#https://global.download.synology.com/download/Document/DeveloperGuide/Surveillance_Station_Web_API_v2.0.pdf

ERROR_CODE_SESSION_EXPIRED = 105

class SurveillanceCameraApi:
    """An implementation of a Synology SurveillanceStation API."""

    def _initialize_api_sid(self):
        payload = {'api': 'SYNO.API.Auth',
                   'method': 'Login',
                   'version': 6,
                   'account': self._account,
                   'passwd': self._password,
                   'session': 'SurveillanceStation',
                   'format':'sid'}
        r = self._get_json_with_retry(self._base_url + 'auth.cgi', payload)
        self._sid = r['data']['sid']

    def get_camera_by_name(self, camera_name):
        camera = {}
        payload = {'api': 'SYNO.SurveillanceStation.Camera',
                   'method': 'List',
                   'version': 6,
                   '_sid': self._sid}
        r = self._get_json_with_retry(self._base_url + 'entry.cgi', payload)
        for cam in r['data']['cameras']:
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
        r = self._get_json_with_retry(self._base_url + 'entry.cgi', payload)
        return r['success']

    def disable_camera(self, cameraIds):
        payload = {'api': 'SYNO.SurveillanceStation.Camera',
                   'method': 'Disable',
                   'version': 6,
                   'cameraIds': cameraIds,
                   '_sid': self._sid}
        r = self._get_json_with_retry(self._base_url + 'entry.cgi', payload)
        return r['success']

    def _get(self, url, payload):
        response = requests.get(url, payload, timeout=self._timeout,
                            verify=self._verify_ssl)

        response.raise_for_status()
        return response

    def _get_json_with_retry(self, url, payload):
        try:
            return self._get_json(url, payload)
        except SessionExpiredException:
            self._initialize_api_sid()
            return self._get_json(url, payload)

    def _get_json(self, url, payload):
        response = self._get(url, payload)
        content = response.json()
        if 'success' not in content or content['success'] is False:
            error_code = content.get('error', {}).get('code')

            if ERROR_CODE_SESSION_EXPIRED == error_code:
                raise SessionExpiredException('Session expired')

            raise ValueError('Invalid or failed response', content)

        return content

    def __init__(self, base_url, account, password):
        """Initialize a Synology Surveillance API."""
        print 'Starting surveillance API'
        self._base_url = base_url + '/webapi/'
        self._account = account
        self._password = password
        self._timeout = 10
        self._verify_ssl = True

        self._initialize_api_sid()

class SessionExpiredException(Exception):
    """An error indicating session expired."""
    pass