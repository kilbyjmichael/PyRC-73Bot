import sqlite3

class LastSeen:
    '''
    An independent class for calculating and storing the time a user was last seen in a channel
    '''
    
    def __init__(self):
        self.db_filename = 'test.db'
        self.connection = sqlite3.connect(self.db_filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE if not exists irc (
                        nick text primary key,
                        channel text,
                        last_active date)''')
        return

    def last_seen(self, user):
        self.cursor.execute("SELECT last_active, channel FROM irc WHERE nick = ?", (user,))
        is_data = self.cursor.fetchone() # I'm ugly, fix me
        if is_data is not None:
            self.cursor.execute("SELECT last_active, channel FROM irc WHERE nick = ?", (user,))
            last_active, user_channel = self.cursor.fetchone()
            return [str(last_active), str(user_channel)] # str for error handling
        return ['none', 'never']

    def store_active(self, user, channel):
        self.cursor.execute("UPDATE irc SET last_active=DATETIME('now'), channel=? WHERE nick=?", (channel, user))
        if self.cursor.rowcount != 1:
            self.cursor.execute("INSERT INTO irc (nick, channel, last_active) VALUES (?, ?, DATETIME('now'))", (user, channel,))
        return
