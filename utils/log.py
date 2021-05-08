import logging.handlers
import time
from logging import config

# logging初始化工作
# filetime=time.strftime('%m-%d-%H', time.localtime())
# myapp = logging.getLogger('test')
# myapp.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s==> %(message)s')
# filehandler = logging.handlers. RotatingFileHandler(filetime+"api_log.txt", mode='a', maxBytes=1024*1024*10,backupCount=10)#20M,分文件大小
# filehandler.setFormatter(formatter)
# myapp.addHandler(filehandler)


# def log(*args,**kwargs):
#     myapp.info(*args,**kwargs)


log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S" #如果不加这个会显示到毫秒。
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',#日志打印到屏幕显示的类。
            'level': 'INFO',
            'formatter': 'detail'
        },
        'loginapi': {
            'class': 'logging.handlers.RotatingFileHandler',#日志打印到文件的类。
            'maxBytes': 1024 * 1024 * 5,             #单个文件最大内存
            'backupCount': 10,                       #备份的文件个数
            'filename': "logs/login_api.txt", #日志文件名
            'level': 'INFO',# 日志等级
            'formatter': 'detail', #调用上面的哪个格式
            'encoding': 'utf-8', #编码
        },
        'combineapi': {
            'class': 'logging.handlers.RotatingFileHandler',#日志打印到文件的类。
            'maxBytes': 1024 * 1024 * 5,             #单个文件最大内存
            'backupCount': 10,                       #备份的文件个数
            'filename': "logs/combine_api.txt", #日志文件名
            'level': 'INFO',# 日志等级
            'formatter': 'detail', #调用上面的哪个格式
            'encoding': 'utf-8', #编码
        }

    },
    'loggers': {
        'loginlogger': {
            'handlers': ['loginapi'],                #打印到屏幕和写入文件
            'level': 'DEBUG',                               #只显示错误的log
        },
        'combinelogger': {
            'handlers': ['combineapi'],
            'level': 'DEBUG',
        },
        'changenickname': {
            'handlers': ['loginapi'],
            'level': 'DEBUG',
        },

        'register_third': {
            'handlers': ['loginapi'],
            'level': 'DEBUG',
        },

        'other': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


config.dictConfig(log_config)
loginlogger = logging.getLogger('loginlogger')
combinelogger = logging.getLogger('combinelogger')
changenicknamelogger=logging.getLogger('changenickname')
register_third_logger=logging.getLogger('register_third')

def callback_log(requesturl,requstsdata,responsedata,_logger,return_msg=''):
    '''日志回调'''
    #组装请求url
    url=requesturl+"?"
    for key,value in requstsdata.items():
        url+=str(key)+"="+str(value)+"&"
    url=url.strip('&')

    _logger.info(url)
    _logger.info('except msg:' + return_msg)
    _logger.info(responsedata)
    _logger.info(' ')
