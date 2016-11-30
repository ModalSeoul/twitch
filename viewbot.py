import requests
import json
import operator


class Twitch:

    def __init__(self, oauth):
        self._user = 'https://api.twitch.tv/kraken/users/'
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
        self.outfile = open(channel, 'w+')

        for indx, chatter in enumerate(chatters):
            user = self.parse_date(self.request_user(chatter)['created_at'])
            if user:
                outfile.write('{}{}'.format(user, '\n'))
                print(indx)
        self.evaluate_scan(channel)

    def evaluate_scan(self, channel):
        with open(channel, 'r+') as infile:
            entries = infile.readlines()
            evaluation = {}

            for entry in entries:
                if entry in evaluation:
                    evaluation[entry] += 1
                else:
                    evaluation[entry] = 1

        most_common = max(evaluation, key=lambda i: evaluation[i])
        json.dump(
            evaluation, open(channel + '.json', 'w'), indent=4, sort_keys=False)
        print('{} : {}'.format(
            self.remove_break(most_common), evaluation[most_common]))

    # ---------
    # Utility
    # ---------

    def parse_date(self, str_date):
        return str_date.split('T')[0].replace('\n', '')

    def remove_break(self, string):
        return string.replace('\n', '')

if __name__ == '__main__':
    channel = input('Enter channel to scan\n--------\n')
    twitch = Twitch('your_oauth')
    twitch.scan_channel(channel)
    twitch.evaluate_scan(channel)
