import os
import requests


username = ''
pwd = ''

cwd = os.getcwd()
dir_in = os.path.join(cwd, 'collection_output')


response = requests.post('https://synbioks.org/login', 
                         headers={'X-authorization': '<token>',
                                  'Accept': 'text/plain'
                                 },
                         data={'email': username, 'password' : pwd}
                        )

xtoken = response.content

for ind, file in enumerate(os.listdir(dir_in)):
    if 504 <= ind <= 799:
        print(ind, file)
        collec_id = file.replace('.xml', '').replace('_collection', '')
        response = requests.post(
            'https://synbioks.org/submit',
            headers={
                'X-authorization': xtoken,
                'Accept': 'text/plain'
            },
            files={
            'files': open(os.path.join(cwd, 'collection_output', file),'rb')
            },
            data={
                'rootCollections' : 'https://synbioks.org/user/jet/fb656a9ac/fb656a9ac_collection/1',
                'overwrite_merge' : '3'
            }
        )
        response = requests.post(
            f'https://synbioks.org/user/jet/fb656a9ac/{collec_id}/1/makePublic',
            headers={
                'X-authorization': xtoken,
                'Accept': 'text/plain'
            },
            data={
                'tabState' : 'existing',
                'collections': 'https://synbioks.org/public/a932bf113a/a932bf113a_collection/1'
                },
        )
        print(response.status_code)