import os, sbol2, json

#%%%
# {'http://purl.org/dc/elements/1.1/publisher', 'http://purl.org/dc/terms/dateAccepted', 'http://purl.org/dc/terms/dateCopyrighted', 'http://wiki.synbiohub.org/wiki/Terms/synbiohub#ownedBy', 'http://purl.org/dc/elements/1.1/creator', 'http://purl.org/dc/terms/created', 'http://purl.org/dc/elements/1.1/subject', 'http://purl.org/dc/terms/type', 'http://wiki.synbiohub.org/wiki/Terms/synbiohub#topLevel', 'http://purl.org/dc/terms/references', 'http://purl.org/dc/terms/isPartOf', 'http://purl.obolibrary.org/obo/OBI_0002110', 'http://purl.org/dc/terms/dateSubmitted', 'http://purl.obolibrary.org/obo/OBI_0001617', 'http://purl.org/dc/terms/abstract', 'http://purl.org/dc/terms/rightsHolder', 'http://purl.org/dc/elements/1.1/rights', 'http://purl.org/dc/elements/1.1/type'}
# class paper_annot:
#     def switch(self, switch_term, paper_annot, sbol_collect):
#         self.switch_term = switch_term
#         self.paper_annot = paper_annot
#         self.sbol_collect = sbol_collect
#         switch_dict = {'http://purl.org/dc/elements/1.1/publisher':'publisher',
#                      'http://purl.org/dc/terms/dateAccepted':'dateAccepted',
#                      'http://purl.org/dc/terms/dateCopyrighted':'dateCopyrighted',
#                      'http://purl.org/dc/elements/1.1/creator':'creator',
#                      'http://purl.org/dc/terms/created':'created',
#                      'http://purl.org/dc/elements/1.1/subject':'subject',
#                      'http://purl.org/dc/terms/references':'references',
#                      'http://purl.org/dc/terms/isPartOf':'partOf',
#                      'http://purl.obolibrary.org/obo/OBI_0002110':'doi',
#                      'http://purl.org/dc/terms/dateSubmitted':'dateSubmitted',
#                      'http://purl.obolibrary.org/obo/OBI_0001617':'pubMed',
#                      'http://purl.org/dc/terms/abstract':'abstract',
#                      'http://purl.org/dc/terms/rightsHolder':'rightsHolder',
#                      'http://purl.org/dc/elements/1.1/rights':'rights',
#                      'http://purl.org/dc/elements/1.1/type':'articleType'}
#         switch_term_func = switch_dict[switch_term]
#         return getattr(self, switch_term_func)()

#     def         switch_dict = {'http://purl.org/dc/elements/1.1/publisher':'publisher',
#                      'http://purl.org/dc/terms/dateAccepted':'dateAccepted',
#                      'http://purl.org/dc/terms/dateCopyrighted':'dateCopyrighted',
#                      'http://purl.org/dc/elements/1.1/creator':'creator',
#                      'http://purl.org/dc/terms/created':'created',
#                      'http://purl.org/dc/elements/1.1/subject':'subject',
#                      'http://purl.org/dc/terms/references':'references',
#                      'http://purl.org/dc/terms/isPartOf':'partOf',
#                      'http://purl.obolibrary.org/obo/OBI_0002110':'doi',
#                      'http://purl.org/dc/terms/dateSubmitted':'dateSubmitted',
#                      'http://purl.obolibrary.org/obo/OBI_0001617':'pubMed',
#                      'http://purl.org/dc/terms/abstract':'abstract',
#                      'http://purl.org/dc/terms/rightsHolder':'rightsHolder',
#                      'http://purl.org/dc/elements/1.1/rights':'rights',
#                      'http://purl.org/dc/elements/1.1/type':'articleType'}


#%%%

cwd = os.getcwd()

seq_files = os.listdir(os.path.join(cwd, 'sequences-files'))[1:]
seq_files = set([x.replace('.seq.txt', '') for x in seq_files])

with open(os.path.join(cwd,'test', 'ACS_collection.json'), 'r', encoding='utf-8') as file:
    papers_json = file.read()
    papers_json = json.loads(papers_json)

#1554 papers, 826 have associated sequences
dont_exist = 0
dont_exist_list = []
exist_list = []
an_list= []
exist = 0
for ind, paper in enumerate(papers_json['attachments']):
    if ind<10:
        file_name = os.path.split(os.path.split(paper['uri'])[0])[1] #this is used to go from uri of the form: https://synbioks.org/public/ACS/sb5b00179/1 to just the sb5b00179 bit
        file_path = os.path.join(cwd,'sequences-files', f'{file_name}.seq.txt')

        p_displayId = paper['displayId']
        p_descript = paper['description']
        annot = paper['annotations']
        annotated_doc = sbol2.Document()
        paper_collect = sbol2.Collection('Collect_Name')
        for ind1, an in enumerate(annot):
            if an['type']=='uri':
                setattr(paper_collect,f'an{ind1}',sbol2.URIProperty(paper_collect, an['name'], 0, 1,[]))
                setattr(paper_collect,f'an{ind1}',an['value'])
            if an['type']=='string':
                setattr(paper_collect,f'an{ind1}',sbol2.TextProperty(paper_collect, an['name'], 0, 1,[]))
                setattr(paper_collect,f'an{ind1}',an['value'])
        annotated_doc.addCollection(paper_collect)
        try:
            with open(file_path) as file:
                # print(file.read())
                
                pass
            exist+=1
            exist_list.append(file_name)

            #create collection with paper info
            #paper description
            #paper displayid
            #paper annotations
            
        except:
            # print(f'{file_name} does not exist')
            dont_exist+=1
            dont_exist_list.append(file_name)

print(dont_exist, exist)#weird there seem to be papers missing as have 826 sequences but only 799 are matching to papers
# print(exist_list)
exist_list=set(exist_list)
# print(seq_files.difference(exist_list))
annotated_doc.write(os.path.join(cwd, 'output_sbol_collect.xml'))

