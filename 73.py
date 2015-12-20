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
        irc.IRCClient.connectionMade(self)
    
    def signedOn(self):
        self.join(self.factory.channel)
        log.msg("Signed on as %s." % (self.nickname))
    
    def joined(self, channel):
        log.msg("Joined %s." % (channel))
    
    def privmsg(self, user, channel, msg):
        if not user:
            return
        if not msg.startswith("!"):
            return
        if msg.startswith("!roll"):
            msg = msg[6:]
            user = "%s: " % (user.split('!', 1)[0], )
            roll = dicer.base_roll(msg)
            self.msg(self.factory.channel, user + roll)
        elif msg.startswith("!help"):
            msg = msg[5:]
            self.msg(self.factory.channel,
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
        elif msg.startswith("!fullhelp"):
            msg = msg[9:]
            self.msg(self.factory.channel, "https://github.com/kilbyjmichael/PyRC-73Bot/blob/master/README.md")
        elif msg.startswith("!begin"):
            msg = msg[7:]
            self.msg(self.factory.channel, "**********Begin Session**********")
        elif msg.startswith("!pause"):
            msg = msg[7:]
            self.msg(self.factory.channel, "**********Pause Session**********")
        elif msg.startswith("!end"):
            msg = msg[5:]
            self.msg(self.factory.channel, "**********End Session************")
        elif msg.startswith("!"):
            self.msg(self.factory.channel, "wut")
            log.err("Unknown Command: " + msg)

class SeventyThreeFactory(protocol.ClientFactory):
    protocol = SeventyThree
    
    def __init__(self, channel, nickname='SeventyThree', realname='73'):
        self.channel = channel
        self.nickname = nickname
        self.realname = realname
    
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
    server=config.get('irc', 'server')
    port=config.get('irc', 'port')
    chanlist = [
            channel.strip()
            for channel
            in config.get('channels', 'list').split('\n')
            if channel.strip()
        ]
    # channel=config.get('irc', 'channel')
    nickname=config.get('irc', 'nickname')
    realname=config.get('irc', 'realname')
    ''' Debug:
    print server
    print port
    print chanlist
    print nickname
    print realname
    '''
    for channel in chanlist:
        reactor.connectTCP(server, int(port), SeventyThreeFactory(channel, nickname, realname))
    reactor.run()