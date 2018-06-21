import requests

ERROR_CODE_SESSION_EXPIRED = 105

class WeatherStationApi:
    """An implementation of a Weather Station API."""

    def _initialize_api_token(self):
        self._access_token = self._get_token()

    def _get_token(self):
        payload = {'grant_type': 'password',
                   'username': self._username,
                   'password': self._password,
                   'client_id': self._client_id,
                   'client_secret': self._client_secret,
                   'scope': 'read_station'}
        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            access_token = response.json()["access_token"]
            #refresh_token = response.json()["refresh_token"]
            return access_token

        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)

    def get_data(self, device_id):
        params = {
            'access_token': self._access_token,
            'device_id': device_id
        }
        try:
            response = requests.post("https://api.netatmo.com/api/getstationsdata", params=params)
            response.raise_for_status()
            return response.json()["body"]
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)

    def _get_json(self, url, params):
        try:
            params['access_token'] = self._access_token
            response = requests.post(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.debug(error.response.status_code, error.response.text)
            if error.response.status_code == 403:
                raise SessionExpiredException('Session expired')

    def _get_json_with_retry(self, url, params):
        try:
            return self._get_json(url, params)
        except SessionExpiredException:
            self._initialize_api_token()
            return self._get_json(url, params)

    def get_rain_data(self, station_id, pluvio_id):
        params = {
            'access_token': self._access_token,
            'device_id': station_id
        }
        r = self._get_json_with_retry("https://api.netatmo.com/api/getstationsdata", params)
        json_response = r["body"]
        dashboard_data = ""
        for device in json_response["devices"]:
            if device["_id"] == station_id:
                for module in device["modules"]:
                    if module["_id"] == pluvio_id:
                        dashboard_data = module["dashboard_data"]
                        break
        return dashboard_data

    def __init__(self, username, password, client_id, client_secret):
        """Initialize a Weather station API."""
        print 'Starting Weather Station API'
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._initialize_api_token()


class SessionExpiredException(Exception):
    """An error indicating session expired."""
    pass
