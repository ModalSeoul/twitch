import requests
import json


class Twitch:

    def __init__(self, oauth):
        self._user = 'https://api.twitch.tv/kraken/users/';
        self._headers = {
            'Authorization': 'OAuth {}'.format(oauth)
        }

    def get_chatters(self, user):
        r = requests.get('http://tmi.twitch.tv/group/user/%s/chatters'%user)
        return r.json()['chatters']['viewers']

    def request_user(self, user):
        r = requests.get('{}{}'.format(self._user, user), headers=self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def scan_channel(self, channel):
        chatters = self.get_chatters(channel)
        outfile = open(channel, 'w+')
        for chatter in chatters:
            user = self.parse_date(self.request_user(chatter)['created_at'])
            if user:
                outfile.write('{}{}'.format(user, '\n'))

    # ---------
    # Utility
    # ---------

    def parse_date(self, str_date):
        return str_date.split('T')[0]

if __name__ == '__main__':
    channel = input('Enter channel to scan\n--------\n')
    twitch = Twitch('your_oauth')
    twitch.scan_channel(channel)
