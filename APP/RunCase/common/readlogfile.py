# -*- coding:utf-8 -*-
import config
__author__ = 'rudolf_han'

def log_file(log_name, log_info = []):

    try:
        c = open(config.log_path + '/' + log_name, 'r+')
        lines = c.readlines()
        for line in lines:
            log_info.append(line)
    except Exception as e:
        log_info.append(e)
    return log_info

