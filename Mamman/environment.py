from os import getenv, path, mkdir

class userdir(object):
    _init_path = getenv('LOCALAPPDATA')
    
    _company_path = path.join(_init_path, 'LTS AS')
    if not path.exists(_company_path):
        print('generating path '+ _company_path)
        mkdir(_company_path)
        
    workspace = path.join(_company_path, 'workspace')
    if not path.exists(workspace):
        print('generating path '+ workspace)
        mkdir(workspace)

    crypto = path.join(_company_path, 'crypto')
    if not path.exists(crypto):
        print('generating path '+ crypto)
        mkdir(crypto)
      
if __name__ == '__main__':
    test = userdir()
    print(test.workspace)
    print(test.crypto)
