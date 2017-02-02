# coding=utf-8

'''
Created on 3 Oct 2016

@author: Luiza Utsch
'''

import hashlib
import os


class UnfollowCheck(object):
    '''
    classdocs
    '''

    def __init__(self, api):
        '''
        Constructor
        '''

        self.api = api
        self.CONFIG_FILE = './' + self.api.user_info['screen_name'] + '.ini'
        self.unfollowers = None
        md5, followers = self.check_followers()
        old_list = self.read_config(md5)

        print('old=' + len(old_list).__repr__() + ' new=' + len(followers).__repr__())
        if len(old_list) > 0:
            self.unfollowers = self.check_unfollowers(old_list, followers)

        self.write_config(md5, followers)

    def write_config(self, md5, ids):
        print("Writing configuration")
        if os.path.exists(self.CONFIG_FILE):
            f = open(self.CONFIG_FILE, "w")
        else:
            f = open(self.CONFIG_FILE, "x")

        print(md5)
        print(ids)
        f.write(md5 + "\n")

        for i in ids:
            f.write(str(i) + " ")

    def read_config(self, current_md5):
        print("Reading configuration")
        ids = []
        if os.path.exists(self.CONFIG_FILE):
            f = open(self.CONFIG_FILE, "r")

            md5 = f.readline()[:-1]

            if md5 != current_md5:
                print("md5 has changed. Parsing ids")
                ids_text = f.readline()

                for i in ids_text.split(" "):
                    if i.isdigit():
                        ids.append(int(i))
            else:
                print("md5 is the same. No changes")
        else:
            print("Configuration %s file not found. Creating" % self.CONFIG_FILE)
            open(self.CONFIG_FILE, "w")

        return ids

    def check_followers(self):
        print("Checking followers")

        followers = self.api.get_followers_list()
        hashseed = "".join(str(followers))

        for t in followers:
            hashseed += "%s" % t

        m = hashlib.md5()
        m.update(hashseed.encode("utf-8"))

        _md5 = m.hexdigest()

        print(followers)

        return _md5, followers

    def check_unfollowers(self, old_list, new_list):
        print("Checking unfollowers")
        self.unfollowers = [str(unf) for unf in old_list if unf not in new_list]
        print(self.unfollowers)

        if len(self.unfollowers) > 0:

            info = self.api.get_friendship_status_by_id(self.unfollowers)
            print(info, len(info))

            # Twitter returns a dict response when error, list of dicts when success
            if len(info) > 0 and type(info) == list:
                for d in info:
                    print(d.get('id_str') + " " + d.get('name') + " @" + d.get('screen_name'))

                return info
            else:
                print('error getting unfollowers info')

        else:
            print('no unfollowers found')

        return []
