# coding=utf-8

'''
Created on 3 Oct 2016

@author: Luiza Utsch
'''

import hashlib
import os


class FollowersCheck(object):
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
        self.new_followers = None
        md5, current_followers = self.check_followers()
        old_followers_list = self.read_config(md5)

        print('old=' + len(old_followers_list).__repr__() + ' new=' + len(current_followers).__repr__())
        if len(old_followers_list) > 0:
            self.unfollowers, self.new_followers = self.check_followers_changes(old_followers_list, current_followers)

        self.write_config(md5, current_followers)

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

    def check_followers_changes(self, old_list, new_list):
        print("Checking followers")
        self.unfollowers = [str(unf) for unf in old_list if unf not in new_list]
        print(self.unfollowers)
        self.new_followers = [str(fol) for fol in new_list if fol not in old_list]
        print(self.new_followers)

        unf_info = []
        fol_info = []

        print("unfollowers: ")
        if len(self.unfollowers) > 0:

            unf_info = self.api.get_friendship_status_by_id(self.unfollowers)
            print(unf_info, len(unf_info))

            # Twitter returns a dict response when error, list of dicts when success
            '''if len(unf_info) > 0 and type(unf_info) == list:
                for d in unf_info:
                    print(d.get('id_str') + " " + d.get('name') + " @" + d.get('screen_name'))
            else:
                print('error getting unfollowers info')'''

        else:
            print('no unfollowers found')

        print("followers: ")
        if len(self.new_followers) > 0:

            fol_info = self.api.get_friendship_status_by_id(self.new_followers)
            print(fol_info, len(fol_info))

            # Twitter returns a dict response when error, list of dicts when success
            '''if len(fol_info) > 0 and type(fol_info) == list:
                for d in fol_info:
                    print(d.get('id_str') + " " + d.get('name') + " @" + d.get('screen_name'))
            else:
                print('error getting new followers info')'''

        else:
            print('no new followers found')

        return unf_info, fol_info
