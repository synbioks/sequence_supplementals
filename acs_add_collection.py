import requests
import sbol2
import os
import re

cwd = os.getcwd()
editted_acs_collections = os.path.join(cwd, 'ACS_collection_sbol_edited.xml')
# editted_acs_collections = os.path.join(cwd, 'ACS_testing.xml')


# #change file to be reupload ready for synbiohub
# ACS_collect = os.path.join(cwd, 'ACS_collection_sbol.xml')
# with open(ACS_collect, encoding='utf8') as file:
#     data = file.read()
#     data = data.replace('https://synbioks.org/public/ACS/','http://examples.org/')
#     data = data.replace('<sbh:ownedBy rdf:resource="https://synbioks.org/user/myers"/>', '')
#     print(data)
#     data = re.sub('<sbh:topLevel rdf:resource="http:\/\/examples.org\/[a-zA-Z0-9_]*\/1"\/>', '', data)
#     with open(editted_acs_collections, "w", encoding='utf8') as f:
#         # Writing data to a file
#         f.write(data)

# load collections file in sbol
acs_doc = sbol2.Document()
acs_doc.read(editted_acs_collections)

# for file converted to sbol add contents to collection
sbol_paper_list = os.listdir(os.path.join(cwd, 'synbict_output'))
for ind, file in enumerate(sbol_paper_list):
    if 0 <= ind <=799:
        print(f'ind: {ind}')

        short_doi = file.replace('.xml','')
        collect_obj = acs_doc.collections[f'http://examples.org/{short_doi}/1']

        paper_doc = sbol2.Document()
        paper_doc.read(os.path.join(cwd, 'synbict_output', file))
        for compdef in paper_doc.componentDefinitions:
            collect_obj.members += [compdef.identity]
        for seq in paper_doc.sequences:
            collect_obj.members += [seq.identity]
        paper_doc.addCollection(collect_obj)
        paper_doc.write(os.path.join(cwd, 'collection_output', f'{short_doi}_collection.xml'))

# upload file to sbol
# make file public


# email = ''
# password = ''

# response = requests.post(
#     'https://synbioks.org/login',
#     headers={
#         'X-authorization': '<token>',
#         'Accept': 'text/plain'
#     },
#     data={
#         'email': email,
#         'password' : password,
#         },
# )

# xtoken = response.content

# load all collections
# add members to collection
# post collection to synbio
# make collection public

# response = requests.post(
#     'https://synbioks.org/public/collecttest/ComponentDefinition_sb5b00156_10_comp/1/addToCollection',
#     headers={
#         'X-authorization': xtoken,
#         'Accept': 'text/plain'
#     },
#     data={
#         'collections': 'https://synbioks.org/public/collecttest/collection1/1',
#         },
# )

# print(response.status_code)
# print(response.content)