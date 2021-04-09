import os, glob, requests

password = ''
email = ''

cwd = os.getcwd()
path_in = os.path.join(cwd, "synbict_output")

response = requests.post(
    'https://synbioks.org/login',
    headers={
        'X-authorization': '<token>',
        'Accept': 'text/plain'
    },
    data={
        'email': email,
        'password' : password,
        },
)

x_token = response.content
new_collection = False
# for ind, file_name in enumerate([os.path.join(path_in,"output_sbol_10.xml"), os.path.join(path_in,"output_sbol_11.xml")]):
# print(glob.glob(os.path.join(path_in, "output_sbol_*.xml")).index('C:\\Users\\JVM\\Downloads\\supplemental_sequence_conversion\\sequences-files\\output_sbol_948.xml'))
for ind, file_name in enumerate(glob.glob(os.path.join(path_in, "*.xml"))[0:]):
    print(file_name, f'{ind} of 799 is {(ind)/799}%')
    if ind < 0 and new_collection:
        #for first file create the collection, then add to it
        response = requests.post(
        'https://synbioks.org/submit',
        headers={
            'X-authorization': x_token,
            'Accept': 'text/plain'
        },
        files={
        'files': open(file_name,'rb'),
        },
        data={
            'id': 'sbks_annotated_sequence_supplementals',
            'version' : '1',
            'name' : 'sbks sequence supplementals',
            'description' : 'Sequence supplementals pulled from ACS Synthetic Biology and annotated using synbict',
            'overwrite_merge' : '1'
        })
        print(response .content)
    elif ind==505: #505 skipped (sb7b00461) and 604 (sb8b00284)
        response = requests.post(
        'https://synbioks.org/submit',
        headers={
            'X-authorization': x_token,
            'Accept': 'text/plain'
        },
        files={
        'files': open(file_name,'rb'),
        },
        data={
            'rootCollections': 'https://synbioks.org/user/jet/sbks_annotated_sequence_supplementals/sbks_annotated_sequence_supplementals_collection/1',
            'overwrite_merge' : '3'
        })
        print(response.content)

