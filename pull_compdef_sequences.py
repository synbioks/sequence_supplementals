# import sbol2, os

# cwd = os.getcwd()

# file_in_name = os.path.join(cwd, 'to_download', 'igem_collection.xml')

# doc_read = sbol2.Document()
# doc_read.read(file_in_name)

# for sbol_object in doc_read:
#     print(sbol_object)
#%%% igem pull sequences

# import sbol2, os
# from sbol2 import Document, PartShop

# cwd = os.getcwd()

# doc = Document()
# doc.read(os.path.join(cwd, 'to_download', 'igem_collection.xml'))
# part_shop = PartShop('https://synbiohub.org/public/igem')
# # part_shop = PartShop('https://synbiohub.org/public/bsu/bsu_collection/1')

# counter = 99
# for obj in doc:
#     col_members = obj.members
#     for ind, item in enumerate(col_members):
#         if ind > 9899:
#             print(f'{ind} of {len(col_members)}')+
#             try:
#                 part_shop.pull(item, doc)
#             except:
#                 pass
#             if ind%100 == 99:
#                 doc.write(os.path.join(cwd, f'igem_library_with_seq_{counter}.xml'))
#                 counter += 1

# # doc = Document()
# # igem = PartShop('https://synbiohub.org/public/igem')

# doc.write(os.path.join(cwd, f'igem_library_with_seq.xml'))

#%% iGEM single file creation

import sbol2, os
from sbol2 import Document, PartShop

cwd = os.getcwd()
igem_pulled = os.listdir(os.path.join(cwd, 'igem_pulled'))

doc = Document()

for xml in igem_pulled:
    print(xml)
    doc.read(os.path.join(cwd, 'igem_pulled', xml))
    print(doc)

print(doc)