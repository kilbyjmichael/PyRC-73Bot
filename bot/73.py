import os, sys

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from ConfigParser import ConfigParser

from modules.dice import DiceRoller
dicer = DiceRoller()

class SeventyThree(irc.IRCClient):
    
    def connectionMade(self):
        """Called when a connection is made."""
        self.nickname = self.factory.nickname
        self.realname = self.factory.realname
        self.password = self.factory.password
        self.channels = self.factory.channels
        self.admin_nicks = self.factory.admins
        self.adminpass = self.factory.adminpass
        irc.IRCClient.connectionMade(self)
    
    def signedOn(self):
        if self.password:
            self.msg("Nickserv", "IDENTIFY " + self.password)
        for chan in self.channels: 
            if isinstance(chan, dict): 
                channel = chan.get('channel', None) 
                password = chan.get('password', None) 
            else: 
                channel = chan 
                password = None 
                self.join(channel=channel, key=password) 
    
    def joined(self, channel):
        log.msg("Joined %s." % (channel))
    
    def kickedFrom(self,channel,kicker,message):
        log.msg("Kicked from %s by %s because %s"% (channel, kicker, message))

    def action(self, user, channel, data):
        return
        
    def privmsg(self, user, channel, msg):
        channel = channel.lower()
        if not user:
            return
        if not msg.startswith("!"):
            return
        if msg.startswith("!roll"):
            msg = msg[6:]
            user = "%s: " % (user.split('!', 1)[0], ) # formatted nicely
            roll = dicer.base_roll(msg)
            self.msg(channel, user + roll)
        elif msg.startswith("!help"):
            msg = msg[5:]
            self.msg(channel,
                "Basic Usage:\n" +
                "!roll XdY \n" +
                "!roll XdY+-Z \n" +
                "!roll Z*XdY \n" +
                "!roll sXdY - sort low to high\n" +
                "!roll vXdY - verbose\n" +
                "!roll aXdY - array (no total)\n" +
                "!help - prints this screen\n" +
                "!fullhelp - prints link to readme\n")

        elif msg.startswith("!message"):
            if msg == "":
                self.say(channel, "Well, ya gotta say somethin'...")
            else:
                self.msg(chan, ''.join(msg_list)) # privmsg a user or channel with the message

        elif msg.startswith("!joinchan"):
            msg = msg[10:]
            user = user.split('!', 1)[0]
            if user in self.admin_nicks:
                self.join(msg)
                # log to config file here
            else:
                self.msg(channel, "I can't join a channel unless an admin tells me to.")
                for admin in self.admin_nicks:
                    self.notice(admin, "I am being told to stop by " + user)
        elif msg.startswith("!quitchan"):
            user = user.split('!', 1)[0]
            if user in self.admin_nicks:
                if msg == "!quitchan":
                    self.part(channel)
                else:
                    msg = msg[10:]
                    self.part(msg)
            else:
                self.msg(channel, "I can't quit a channel unless an authorized user tells me to.")
                for admin in self.admin_nicks:
                    self.notice(admin, "I am being told to stop by " + user)

        elif msg.startswith("!stop"):
            msg = msg[6:]
            user = user.split('!', 1)[0]
            if user in self.admin_nicks and msg == self.adminpass:
                self.quit() # will rejoin unless ugly shit
                os._exit(0) # fix this ugly shit
            else:
                self.msg(channel, "I can't quit unless an authorized user tells me to.")
                for admin in self.admin_nicks:
                    self.notice(admin, "I am being told to stop by " + user)

        elif msg.startswith("!fullhelp"):
            msg = msg[9:]
            self.msg(channel, "https://github.com/kilbyjmichael/PyRC-73Bot/blob/master/README.md")
        elif msg.startswith("!begin"):
            msg = msg[7:]
            self.msg(channel, "**********Begin Session**********")
        elif msg.startswith("!pause"):
            msg = msg[7:]
            self.msg(channel, "**********Pause Session**********")
        elif msg.startswith("!end"):
            msg = msg[5:]
            self.msg(channel, "**********End Session************")
        elif msg.startswith("!"):
            self.msg(channel, "wut")
            log.err("Unknown Command: " + msg)

class SeventyThreeFactory(protocol.ClientFactory):
    protocol = SeventyThree
    
    def __init__(self, channels, password, admins, adminpass, nickname='SeventyThree', realname='73'):
        self.channels = channels
        self.nickname = nickname
        self.password = password
        self.realname = realname
        self.admins = admins
        self.adminpass = adminpass
    
    def clientConnectionLost(self, connector, reason):
        log.err("Lost connection (%s), reconnecting." % (reason))
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        log.err("Could not connect: %s" % (reason))
        reactor.stop()

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    config = ConfigParser()
    config.read('settings.ini')
    server = config.get('irc', 'server')
    port = config.get('irc', 'port')
    chanlist = [
            channel.strip()
            for channel
            in config.get('channels', 'list').split('\n')
            if channel.strip()
        ]
    admins = [
            admin.strip()
            for admin
            in config.get('admin', 'admins').split('\n')
            if admin.strip()
        ]
    adminpass = config.get('admin', 'controlPass')
    # channel = config.get('irc', 'channel')
    nickname = config.get('irc', 'nickname')
    password = config.get('irc', 'password')
    realname = config.get('irc', 'realname')
    ''' Debug:
    print server
    print port
    print chanlist
    print nickname
    print realname
    '''
    reactor.connectTCP(server, int(port), SeventyThreeFactory(chanlist, password, admins, adminpass, nickname, realname))
    reactor.run()