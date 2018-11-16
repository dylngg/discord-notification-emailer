import discord
import sys
import os
import logging
import asyncio
import threading
import socket
import time
import smtplib
from email.message import EmailMessage
import configparser


class ClusterManager():

    def __init__(self, callback, clustering_period=10):
        """Defines a cluster manager that allows for the clustering of objects
        in a period of time. After that period of time, a callback is called
        and the cluster is reset.

        :param callback: A function to call when the clustering period is
        over. The objects in the cluster are passed into that callback as the
        sole argument.
        :param clustering_period: The period of time in seconds in which all
        objects added are clustered together.
        """
        self.callback = callback
        self.clustering_period = clustering_period
        self._clustering = False
        self._cluster = []

    def append(self, obj):
        """Appends a obj and clusters it accordingly.

        :param obj: An object that is added to the cluster
        """
        if not self._clustering:
            self._start_clustering()

        self._cluster.append(obj)

    def _start_clustering(self):
        """Starts a clustering timer that does a callback with all the obj in
        the cluster after a period of time.
        """
        self._clustering = True
        t = threading.Thread(target=self.end_cluster)
        t.start()

    def end_cluster(self):
        logging.debug("Waiting...")
        time.sleep(self.clustering_period)
        logging.debug("Calling callback")
        self.callback(self._cluster)
        self._clustering = False
        self._cluster = []

config = configparser.ConfigParser()
config.read('config.cfg')

# Email
email_config = config['Email']
to = email_config['to']
sender = f'discord_bot@{str(socket.gethostname())}'
smtp_username = email_config.get('smtp_username')
smtp_server = email_config.get('smtp_server')
smtp_port = email_config.get('smtp_port')
smtp_password = email_config.get('smtp_password')

# Bot Configuration
clustering_config = config['Clustering']
clustering_period = clustering_config.get('clustering_period', 60)
key = config['Discord'].get('key')

def send_message(messages):
    content = "Your teammates have posted some messages. The messages are below:<br>"
    for message in messages:
        content += (f"{message.author} on {message.channel.name}"
                    f"({message.timestamp.strftime('%I')}): {message.clean_content}<br>")

    msg = EmailMessage()
    msg.set_content(content)

    msg['Subject'] = f'{str(len(messages))} New messages from discord!'
    msg['From'] = sender
    msg['To'] = to

    print(smtp_server, smtp_port)
    mail = smtplib.SMTP()
    mail.connect(smtp_server, smtp_port)
    mail.starttls()
    mail.login(smtp_username, smtp_password)
    mail.sendmail(sender, to, msg.as_string())
    mail.quit()

logger = logging.getLogger('discord_emailer')
logging.basicConfig(stream=sys.stdout,
                    level=os.environ.get('LOGLEVEL', 'DEBUG'))

clusterer = ClusterManager(send_message)
client = discord.Client()

@client.event
async def on_ready():
    logger.info('Bot is now online.')

@client.event
async def on_message(message):
    logger.debug('Recieved %s', message.content)
    clusterer.append(message)

client.run(key)
