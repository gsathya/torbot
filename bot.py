"""
An example IRC log bot - logs a channel's events to a file.

If someone says the bot's name in the channel followed by a ':',
e.g.

  <foo> logbot: hello!

the bot will reply:

  <logbot> foo: I am a log bot

Run this script with two arguments, the channel name the bot should
connect to, and file to log to, e.g.:

  $ python ircLogBot.py test test.log

will log channel #test to the file 'test.log'.
"""


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys

class TorBot(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = "satbot"
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "[connected at %s]" % time.asctime(time.localtime(time.time()))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "[disconnected at %s]" % time.asctime(time.localtime(time.time()))

    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        for channel in self.factory.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        print "<%s> %s" % (user, msg)
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I am a log bot" % user
            self.msg(channel, msg)
            print "<%s> %s" % (self.nickname, msg)

class TorBotFactory(protocol.ClientFactory):
    """
    A factory for TorBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channels):
        self.channels = channels

    def buildProtocol(self, addr):
        p = TorBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    f = TorBotFactory([sys.argv[1], sys.argv[2]])

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
