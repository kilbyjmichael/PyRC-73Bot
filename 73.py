import os, sys

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from ConfigParser import ConfigParser

from dice import DiceRoller
dicer = DiceRoller()

class SeventyThree(irc.IRCClient):
    
    def connectionMade(self):
        """Called when a connection is made."""
        self.nickname = self.factory.nickname
        self.realname = self.factory.realname
        self.password = self.factory.password
        self.channels = self.factory.channels
        self.admin_nicks = self.factory.admins
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
                "!begin - prints session begin\n" +
                "!end - prints session end\n" +
                "!pause - prints session pause\n" +
                "!help - prints this screen\n" +
                "!fullhelp - prints link to readme\n")
        elif msg.startswith("!joinchan"):
            msg = msg[10:]
            user = user.split('!', 1)[0]
            if user in self.admin_nicks:
                self.join(msg)
            else:
                self.msg(channel, "I can't join a channel unless an admin tells me to, please contact %s." % (self.admin_nicks))
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
    
    def __init__(self, channels, password, admins, nickname='SeventyThree', realname='73'):
        self.channels = channels
        self.nickname = nickname
        self.password = password
        self.realname = realname
        self.admins = admins
    
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
            in config.get('admins', 'list').split('\n')
            if admin.strip()
        ]
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
    reactor.connectTCP(server, int(port), SeventyThreeFactory(chanlist, password, admins, nickname, realname))
    reactor.run()