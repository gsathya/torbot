"""
An IRC bot that idles in one channel listening for certain
interesting "words" and when a msg contains one such word,
it informs another channel of this msg.

To run -

  $ python torbot.py
"""

OWNER = "gsathya"
NICK = "torbot"
READ_CHANNEL = 'tor-bots'
WRITE_CHANNEL = 'andromeda'
WORD_LIST = "words.txt"

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys

def reload_words():
    with open(WORD_LIST) as fh:
        words = fh.read().split()
    return words

class TorBot(irc.IRCClient):
    """An IRC bot."""
    
    nickname = NICK

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "[connected at %s]" % time.asctime(time.localtime(time.time()))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "[disconnected at %s]" % time.asctime(time.localtime(time.time()))

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.read_chan)
        self.join(self.factory.write_chan)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "My creator is %s. He's awesome" % self.factory.owner
            self.msg(user, msg)
            return
        
        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            if user == self.factory.owner:
                msg = msg.split(':')[1]
                if msg.strip() == "reload":
                    self.factory.words = reload_words()
                    print "Reloaded words"
                elif msg.strip() == "die":
                    reactor.stop()
            else:
                msg = "%s: I am a trac bot. I inform %s about stuff. I'm awesome." % (user, self.factory.owner)
                self.msg(channel, msg)

        if channel != '#'+self.factory.read_chan:
            return

        for word in self.factory.words:
            if word in msg:
                self.msg('#'+self.factory.write_chan, self.factory.owner+':'+msg)
                return

class TorBotFactory(protocol.ClientFactory):
    """
    A factory for TorBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, read_chan, write_chan):
        self.read_chan = read_chan
        self.write_chan = write_chan
        self.words = reload_words()
        self.owner = OWNER

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
    f = TorBotFactory(READ_CHANNEL, WRITE_CHANNEL)

    # connect factory to this host and port
    reactor.connectTCP("irc.oftc.net", 6667, f)

    # run bot
    reactor.run()
