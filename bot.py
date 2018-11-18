import discord
import logging
import socket
import configparser
import clusterer
import email_tools

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)


class EmailerBot(discord.Client):

    def __init__(self, emailer, to, *args, clustering_period=60,
                 sender=f'discordbot@{socket.gethostname()}', loop=None,
                 **options):
        """Inializes a bot that sends new messages to a email

        :param emailer: A email_tools.Emailer obj that will be used to send
        emails.
        :param clustering_period: The period of time between messages in which
        messages are grouped together in a single email.
        """
        self.emailer = emailer
        self.to = to
        self.sender = sender
        self.cluster_manager = clusterer.ClusterManager(self.send_email,
                                                        clustering_period)
        super().__init__(*args, loop=loop, **options)

    async def on_ready(self):
        logger.info('Bot is now online.')

    async def on_message(self, message):
        await self.add_to_cluster(message)

    async def add_to_cluster(self, message):
        self.cluster_manager.append(message)

    def send_email(self, messages):
        channels = set([msg.channel.name for msg in messages])
        channel_content = {channel: '' for channel in channels}

        for message in messages:
            thread = (f'<br><h2>{message.author.name}</h2>'
                      f'<span class="date">{message.timestamp.strftime("%H:%M on %b %d")}'
                      f'</span>')
            thread += f'<br><p>{message.content}</p>'
            channel_content[message.channel.name] += thread

        style = ('* { font-size: 14px; }'
                 '.date { padding-left: 15px; opacity: 50%; }'
                 'h2 { display: inline; padding-bottom: 15px; }')
        content = (f'<html><head><style>{style}</style></head><body>'
                   f'{"".join([th for th in channel_content.values()])}'
                   f'</body></html>')
        subject = (f'{len(messages)} New Messages from Discord '
                   f'({",".join(channels)})')
        self.emailer.send_email(self.to,
                                self.sender,
                                subject,
                                content,
                                content_type='text/html')


def configuration(filename='config.cfg'):
    """Reads a config file and returns a dict with it's properties"""
    reader = configparser.ConfigParser()
    reader.read(filename)
    config = {}

    # Email
    email_config = reader['Email']
    config['to'] = email_config['to']
    config['smtp_username'] = email_config.get('smtp_username')
    config['smtp_server'] = email_config.get('smtp_server')
    config['smtp_port'] = email_config.get('smtp_port')
    config['smtp_password'] = email_config.get('smtp_password')

    # Bot Configuration
    clustering_config = reader['Clustering']
    config['period'] = int(clustering_config.get('clustering_period', 60))
    config['key'] = reader['Discord'].get('key')

    return config


def main():
    config = configuration()
    emailer = email_tools.Emailer(config['smtp_username'],
                                  config['smtp_server'],
                                  config['smtp_port'],
                                  config['smtp_password'])
    bot = EmailerBot(emailer, config['to'], clustering_period=config['period'])
    bot.run(config['key'])


if __name__ == '__main__':
    main()
