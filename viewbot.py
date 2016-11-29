import requests
import json


class Twitch:

    def __init__(self, oauth):
        self._user = 'https://api.twitch.tv/kraken/users/';
        self._headers = {
            'Authorization': 'OAuth {}'.format(oauth)
        }

    def request_user(self, user):
        r = requests.get('{}{}'.format(self._user, user), headers=self._headers)
        if r.status_code == 200:
            user_data = r.json()

twitch = Twitch('your_oauth')
twitch.request_user('jellypeanut')
