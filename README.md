TorBot
====

An IRC bot that idles on one channel listening for certain
interesting "words" and when a msg contains one such 
word, it informs another channel of this msg.

Typically you'd run this on #tor-bots and make it listen for
particular keywords which could be components, devs, etc
and make it inform you of msgs that interest you in a separate
channel. 

I have this running on #tor-bots, listening for words like "compass"
(a component), "stem"(another component), "gsathya"(me), 
"neena"(hacker), etc. So I get pinged in real time when a new ticket
is filed for "Compass" or assigned to me.

Setup
====

* You need ```twisted``` for this.

```
$ apt-get install python-twisted
```

* Modify torbot.py

```OWNER``` =  Your ```IRC``` nick, 

```NICK``` = Bot's nick

```READ_CHANNEL``` = Channel to listen/idle in

```WRITE_CHANNEL``` = Channel to write the msgs in

```WORD_LIST``` = path to space separated word list

* Run ```torbot.py```

```
$ python torbot.py
```

Extras
====

Also, you can reload the words anytime instead of restarting it, by using the "reload" command. You can also kill the bot by asking it to "die".
