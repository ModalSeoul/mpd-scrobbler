#! /usr/bin/python

import os
import json
import requests
from time import sleep

Auth = 'https://modal.moe/api/api-token-auth/'
Scrobble = 'https://modal.moe/api/scrobbles/'

post = requests.post
get = requests.get


class Wilt:

    def __init__(self):
        self.user = input('Username: ')
        self.password = input('Password: ')
        self.logged_in = False
        self.header = {'Authorization': 'Token {}'.format(self.login())}
        self.last_played = ''  # Clarity

    def login(self):
        r = post(Auth, data={'username': self.user, 'password': self.password})
        if 'token' in r.text:
            self.logged_in = True
            os.system('clear')
        else:
            print('Something went wrong - Not logged in!')
            return None
        return json.loads(r.text)['token']

    def scrobble(self, scrobble):
        if scrobble['song'] != self.last_played:
            r = post(Scrobble, data=scrobble, headers=self.header)
            self.last_played = scrobble['song']
        else:
            return None

Wilt = Wilt()

def query_mpd():
    try:
        query = os.popen('mpc current').read()
        artist = query.split(' - ')[0].strip()
        song = query.split(' - ')[1].strip()
        Wilt.scrobble({'song': song, 'artist': artist})
    except:
        print('Non fatal exception. Query failed.')

if __name__ == '__main__':
    while 1:
        query_mpd()
        sleep(25)
