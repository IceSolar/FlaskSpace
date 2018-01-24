# -*- coding:utf-8 -*-
__author__ = 'rudolf_han'
import logging
from logging.handlers import RotatingFileHandler
import threading
import configparser
import config
import os

class LogSignleton(object):

    def __init__(self, s_name_log, s_path_log=config.log_path, i_level_log=logging.DEBUG):

        self.console_log_on = 1
        self.logfile_log_on = 1

        #自定义一个名为s_name_log的logger
        self.customLogger = logging.getLogger(s_name_log)

        # 实例化一个format,定义了log的格式
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
        # 实例化一个filehander，log可以将message写入文件中
        #fh = logging.FileHandler(os.path.join(s_path_log, s_name_log))

        # sh = logging.StreamHandler()
        # 实例化一个filter，对logger的name进行过滤，如果s_name_log=='JeremyLogging'，输出；反之，过滤掉
        # 这个filter可以配置到handler中，也可以直接配置到logger中
        # ft = logging.Filter('JeremyLogging')


        if self.console_log_on == 1:  # 如果开启控制台日志
            # 实例化一个streamhandler，log可以将message输出到控制台中
            console = logging.StreamHandler()
            console.setFormatter(fmt)
            self.customLogger.addHandler(console)
            self.customLogger.setLevel(i_level_log)

        if self.logfile_log_on == 1:  # 如果开启文件日志
            # 实例化一个filehander，log可以将message写入文件中
            rt_file_handler = RotatingFileHandler(os.path.join(s_path_log, s_name_log))
            rt_file_handler.setFormatter(fmt)
            self.customLogger.addHandler(rt_file_handler)
            self.customLogger.setLevel(i_level_log)

    def debug(self, s_message_log):
        self.customLogger.debug(s_message_log)

    def info(self, s_message_log):
        self.customLogger.info(s_message_log)

    def warning(self, s_message_log):
        self.customLogger.warning(s_message_log)

    def error(self, s_message_log):
        self.customLogger.error(s_message_log)

    def critical(self, s_message_log):
        self.customLogger.critical(s_message_log)




