# coding=utf-8

'''
Created on Jan 22, 2016

@author: Luiza Utsch
'''

from flask import flash


class TwitterApiAccess(object):
    '''
    classdocs
    '''

    def __init__(self, consumer_key, consumer_secret, twitter_oauth, session):
        '''
        Constructor
        '''

        self.MAX_IDS = 100
        self.api = twitter_oauth
        self.session = session
        token_key = self.session['twitter_oauth']['oauth_token']
        token_secret = self.session['twitter_oauth']['oauth_token_secret']

        print(session['twitter_oauth'])
        print(consumer_key, consumer_secret, token_key, token_secret)
        r = self.api.request('users/show.json', {'screen_name': self.session['twitter_oauth']['screen_name']})
        if r.status != 200:
            flash("Error: #%d, %s " % (
                r.data.get('errors')[0].get('code'),
                r.data.get('errors')[0].get('message'))
                  )
        self.user_info = r.data
        print(self.user_info)

    def get_followers_list(self):
        followers = []
        # for usr in self.api.request('followers/ids', {'count': 10}):
        _cursor = -1
        while _cursor != 0:
            r = self.api.request('followers/ids.json', {'cursor': _cursor})

            if r.status == 200:
                for usr in r.data['ids']:
                    followers.append(usr)
                _cursor = r.data['next_cursor']

            else:
                flash("Error: #%d, %s " % (
                    r.data.get('errors')[0].get('code'),
                    r.data.get('errors')[0].get('message'))
                      )
                _cursor = 0

            print(followers)
            return followers

    def get_users_info_by_id(self, id_list=[]):
        return self.get_info(id_list, 'user_id', 'users')

    def get_users_info_by_name(self, id_list=[]):
        return self.get_info(id_list, 'screen_name', 'users')

    def get_friendship_status_by_id(self, id_list=[]):
        return self.get_info(id_list, 'user_id', 'friendships')

    def get_friendship_status_by_name(self, id_list=[]):
        return self.get_info(id_list, 'screen_name', 'friendships')

    def get_info(self, data_list, data_type, info_type='users'):
        resource = ""
        if info_type == 'users':
            resource = 'users/lookup.json'
        elif info_type == 'friendships':
            resource = 'friendships/lookup.json'
        else:
            flash("info_type %s is invalid" % info_type)
            return []

        print('Getting info %s' % info_type)
        print(data_list, len(data_list))
        # max ids = 100
        info = []
        range_ini = 0
        if len(data_list) > self.MAX_IDS:
            range_end = self.MAX_IDS - 1
        else:
            range_end = len(data_list) - 1

        while range_end < len(data_list):
            ids = ",".join(data_list[range_ini:range_end + 1])
            print("ids ", ids)
            r = self.api.request(resource, {data_type: ids})
            if r.status != 200:
                flash("Error: #%d, %s " % (
                    r.data.get('errors')[0].get('code'),
                    r.data.get('errors')[0].get('message'))
                      )
                return []
            print("respo ", r.status)
            range_ini += self.MAX_IDS
            range_end += self.MAX_IDS

            print(r.data)
            info += r.data

        print(info)
        return info

    def get_timeline(self):
        r = self.api.request('statuses/home_timeline.json')
        if r.status == 200:
            tweets = r.data
            return tweets
        else:
            flash('Unable to load tweets from Twitter', 'error')
            return ""
