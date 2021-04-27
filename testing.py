import os, sbol2
from sbol2 import Document

cwd = os.getcwd()

seq_file = os.path.join(cwd, 'libraries', 'YTK_collection.xml')

doc_read = Document()
doc_read.read(seq_file)
print('hi')
for ind, compdef in enumerate(doc_read.componentDefinitions):
    if ind <10:
        print(compdef, f'{ind+1} of {len(doc_read.componentDefinitions)}')
        seq_name = str(compdef.sequence)
        seq = doc_read.sequences[seq_name].elements
        component, annotated_num = synbict_use(sequence, compdef.title(), annotator, annotated_num=annotated_num)