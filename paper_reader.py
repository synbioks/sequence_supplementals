import os, sbol2, json

cwd = os.getcwd()

with open(os.path.join(cwd,'test', 'ACS_collection.json'), 'r', encoding='utf-8') as file:
    papers_json = file.read()
    papers_json = json.loads(papers_json)

#1554 papers, 826 have associated sequences
dont_exist = 0
dont_exist_list = []
exist = 0
for ind, paper in enumerate(papers_json['attachments']):
    if ind<10:
        file_name = os.path.split(os.path.split(paper['uri'])[0])[1] #this is used to go from uri of the form: https://synbioks.org/public/ACS/sb5b00179/1 to just the sb5b00179 bit
        file_path = os.path.join(cwd,'sequences-files', f'{file_name}.seq.txt')
        # print(file_path)
        try:
            with open(file_path) as file:
                print(file.read())
            exist+=1

            #create collection with paper info
            #paper description
            #paper displayid
            #paper annotations
            
        except:
            # print(f'{file_name} does not exist')
            dont_exist+=1
            dont_exist_list.append(file_name)

print(dont_exist, exist)#weird there seem to be papers missing as have 826 sequences but only 799 are matching to papers

