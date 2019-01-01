# Discord Notification Emailer

I got tired of push notifications interupting me, so I made a discord bot that sends message notifications to me via email (which I can control the timing of). This is the code for that.

## How it works

Upon a new message in any of the text channels, the bot will start recording the new messages within a set period of time (plus the original). After that period of time, a email will be sent with all the notifications during that period of time and the timing will reset. This is done so the user doesn't get a ton of emails. This period of time can be set in the configuration.

## Installing

Discord bot needs Python 3.6.5+ and requires the python `discord` package (via `pip install discord`). This will be shown below. You'll also want to clone this repo (`git clone https://github.com/dylngg/discord_notification_emailer.git`) or download the zip and unzip it.

### Installing Python3 and `discord` package on MacOS/Linux

You can download the latest python version from [here](https://www.python.org/downloads/ "Python Downloads"). After installing, you'll want to jump into the Terminal. From there, you'll need to install the discord python package by running `sudo pip install discord` (The sudo should be used carefully since it elevates your permissions, allowing whatever command is in front to modify things with higher permissions (like root permissions)).

### Installing Python3 and `discord` package on Windows

Installing on Windows is similar to MacOS/Linux. You'll want to download the latest python version from [here](https://www.python.org/downloads/ "Python Downloads"). During the installation, you'll want to make sure the "Add Python3.X to PATH" is checked. After installing, you'll want to open up the command prompt with admin privileges (Required to install the `discord` python package). You can do this by right clicking the windows start button and selecting "Command Prompt (Admin)". After that you'll want to run `pip install discord`.

## Configuring

By now you should have installed Python3.6+, the `discord` package via the `pip` command and downloaded the source code. You'll now want to configure the bot to fit your preferences, as well as register the bot with discord.

### Setting up a bot with discord

To register your bot with discord, go to [discord's developer site](https://discordapp.com/developers/applications/) and create a application. Name it whatever you want, but I named mine "Discord Emailer" to be clear what the bot does. After that, on the left, click on the bot tab. Once there you'll want to create a bot. You don't need to give it any special permissions since all the bot does is read messages. After that is done, make sure you copy the token on the bot tab. You'll put this in your config.

### Configuring the `config.cfg`

There are several settings in here...

```INI
[Discord]
key={Enter Key Here!}
```

**Make sure you enter token** that you got from the bot tab in discord's developer site into the key variable.

```INI
[Email]
to = username@gmail.com
smtp_username = username@gmail.com
smtp_server = smtp.gmail.com
smtp_port = 587
smtp_password = password
```

Here is where you'll want to setup how your emails get sent out. You need a mail server for this, so you can either set one up yourself, or just use your email provider's. The example configuration above is for a gmail user. The port and server will change depending on your email provider. `to` is obviously for who this message is being sent to.

```INI
[Clustering]
clustering_period = 10
```

This is where you'll set the period of time (in seconds) that responses and messages sent after a inital message are clustered together in the same email. A longer period will result in less emails, but the emails also come at a later time than the original messages were sent. I chose 300s (5 minutes), since I figure most discord messages aren't too urgent.

### Inviting the bot to your server

Make sure you have server permissions to do this. To add the bot to the server, go to [discord's developer site](https://discordapp.com/developers/applications/) again and click on your application. Once there, click on the OAuth2 tab. Then scroll to the bottom and select the bot scope. After clicking that box, a url will popup below all the scope options. Open that url in a new tab, and from there you should be able to select which server you want to add it to. The bot will then appear in that channel when the bot program is running.

## Running the Program

After those things are installed, you can `cd discord_notification_emailer` and `python3 bot.py` from either the Terminal (MacOS/Linux), or Command Prompt. As long as you want messages to appear in your inbox, you'll want to run this in the background (I ran mine on a raspberry pi). Below are some links for making this easier. That's it! Enjoy your emails!

## Links for running the program in the background

For MacOS, you'll want to use the [http://www.launchd.info/](http://www.launchd.info/) program.

For Linux, I'd suggest `systemd` if you're on a newer system that uses it. There is a example service file in this repository.

For Windows, `¯\_(ツ)_/¯` (I'm not a windows person). This link might be helpful (https://www.howtogeek.com/50786/using-srvstart-to-run-any-application-as-a-windows-service/)

