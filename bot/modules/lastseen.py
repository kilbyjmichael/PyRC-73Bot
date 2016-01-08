from pydblite import Base
from datetime import datetime

class LastSeen:
    '''
    An independent class for calculating and storing the time a user was last seen in a channel
    '''
    
    def __init__(self):
        self.database = Base('test.pdl') #      'activetime' for last talk
        self.database.create('user', 'channel', 'jointime', 'quittime', mode='open')
        self.database.insert('firstUser', '#not_a_channel', '0', '0') # this is so the database won't break
        return
        
    def calculate_last_seen(self, joined, quit):
        date_format = "%Y-%m-%d %H:%M:%S"
        if joined == None:
            return ['never', 'none']
        if quit == None:
            return ['never', 'none']
        else:
            joined = datetime.strptime(str(joined), date_format)
            quit = datetime.strptime(str(quit), date_format)
        
        join_delta = datetime.now() - joined # join time minus now
        quit_delta = datetime.now() - quit # quit time minus now
        
        if join_delta > quit_delta:
            # user would have quit
            # because quit delta is smaller (meaning closer to now)
            is_on = False
            '''return last_seen #find this somewhere'''
        else: # quit delta larger than join delta
            # uesr should still be on
            # because joined is bigger than quit
            is_on = True
        return is_on
    
    def last_seen_user(self, user):
        record = self.database(user=user)
        user_jointime = None
        user_quittime = None
        user_channel = None
        for item in record:
            user_quittime = item['quittime']
            user_jointime = item['jointime']
            user_channel = item['channel']
        is_on = self.calculate_last_seen(user_jointime, user_quittime)
        if is_on: # True
            return ['now', str(user_channel)]
        else:
            return [str(user_quittime), str(user_channel)] # str for error handling
    
    def store_joined(self, user, channel):
        jointime = "2016-01-07 18:55:24"#str(datetime.now())[:19]
        user_exists = self.database(user=user)
        if user_exists:
            self.database.update(user_exists, jointime=jointime)
            self.database.update(user_exists, channel=channel)
            print "I updated the users jointime: " + str(user_exists)
        else:
            self.database.insert(user, channel, jointime, quittime="")
            print "I made a dude"
        self.database.commit()
        return
    
    def store_quit(self, user, channel):
        quittime = str(datetime.now())[:19]
        user_exists = self.database(user=user)
        if user_exists:
            self.database.update(user_exists, quittime=quittime)
            self.database.update(user_exists, channel=channel)
            print "I updated the users quittime: " + str(user_exists)
        else:
            self.database.insert(user, channel, jointime="", quittime=quittime)
            print "I made a dude"
        self.database.commit()
        return