# import os
# import sbol2

# cwd = os.getcwd()

# # make list of all papers
# ACS_doc = sbol2.Document()
# paper_collect1 = sbol2.Collection('collection1')
# ACS_doc.addCollection(paper_collect1)
# ACS_doc.write(os.path.join(cwd, 'synbict_output', '_collection_test.xml'))

# paper_collect2 = sbol2.Collection('collection2')
# ACS_doc.addCollection(paper_collect2)
# collect_obj.members +=[sequence_obj.identity]

# ACS_doc.read(os.path.join(cwd, 'ACS_collection.xml'))
# for col in ACS_doc.collections:
#     col_list = list(col.members)

test = 'sb7b00382/suppl/Supporting Information 2.pdf'
print(test.replace(' ','_'))
