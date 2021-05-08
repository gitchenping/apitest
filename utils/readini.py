import configparser

def readini(path):
    cf=configparser.ConfigParser()

    cf.read(path,encoding='utf-8')

    return cf