import requests
import json


class connection():
    url = None
    headers = None

    def __init__(self):
        #setting up variables
        with open('conf\config.json') as conf_file:    
            conf = json.load(conf_file)
        conf_file.close()
        self.url='https://api.lts.no/api/v2/db/_table/'
        self.headers ={'X-Dreamfactory-API-Key': conf['api-key-lts']}
    
    def get_all(self, table):
        resp = requests.get(url=self.url+table, headers=self.headers)
        if resp.status_code != 200:
            raise Exception('ERROR: API status code ' + str(resp.status_code))
        else:
            return(resp.json()['resource'])
    
    def get(self, table):
        resp = requests.get(url=self.url+table, headers=self.headers)
        if resp.status_code != 200:
            print(json.loads(resp._content)['error']['message'])
            raise Exception('ERROR: API status code ' + str(resp.status_code))
        else:
            if len(resp.json()["resource"]) == 0:
                raise Exception('no task in table')
            else:
                return(resp.json()['resource'][0])
    
    def post(self, table, data):
        resp = requests.post(url=self.url+table, data=json.dumps({'resource': [data]}), headers=self.headers) 
        if resp.status_code != 200:
            print(
                'Status code',
                resp.status_code,
                'from server:',
                json.loads(resp._content)['error']['message'])
            #print(resp._content)
            raise Exception('ERROR: API status code ' + str(resp.status_code))
        else:
            return(resp.json())
    
