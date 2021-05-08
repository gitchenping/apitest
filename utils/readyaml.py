import yaml

def readyml(filepath):

    f=open(filepath,encoding='utf-8')
    ret=yaml.load(f,Loader=yaml.FullLoader)
    f.close()

    #

    return ret