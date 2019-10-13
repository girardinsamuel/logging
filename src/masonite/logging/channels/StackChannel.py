from ..factory import DriverFactory
from masonite.helpers import config
from masonite.helpers.filesystem import make_directory
import os
import pendulum
from .BaseChannel import BaseChannel
from ..ChannelFactory import ChannelFactory

class StackChannel(BaseChannel):

    def __init__(self, channels=[]):
        channels = channels or config('logging.channels.stack.channels')
        self.channels = []
        for channel in channels:
            channel = ChannelFactory.make(channel)()
            self.channels.append(channel)
    
    def debug(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('debug', channel.max_level):
                continue
            
            print('using', channel.driver)
            channel.driver.debug(message, *args, **kwargs)
            
    def notice(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('notice', channel.max_level):
                continue
            
            print('using', channel.driver)
            channel.driver.notice(message, *args, **kwargs)
