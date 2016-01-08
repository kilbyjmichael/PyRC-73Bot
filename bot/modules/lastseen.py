from pydblite import Base
from datetime import datetime

class LastSeen:
    '''
    An independent class for calculating and storing the time a user was last seen in a channel
    '''
    
    def __init__(self):
        self.database = Base('test.pdl') #      'activetime' for last talk
        self.database.create('user', 'channel', 'jointime', 'quittime', mode='open')
        self.database.insert('poopy', '#sage', '0', '0')
        return
        
    def calculate_last_seen(self, joined, quit):
        date_format = "%Y-%m-%d %H:%M:%S"
        
        joined = datetime.strptime(joined, date_format)
        quit = datetime.strptime(quit, date_format)
        
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