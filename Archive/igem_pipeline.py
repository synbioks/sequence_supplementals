# import sbol2, os
# from sbol2 import Document, PartShop

# cwd = os.getcwd()

# doc = Document()
# doc.read(os.path.join(cwd, 'to_download', 'igem_collection.xml'))
# part_shop = PartShop('https://synbiohub.org/public/igem')
# # part_shop = PartShop('https://synbiohub.org/public/bsu/bsu_collection/1')

# for obj in doc:
#     col_members = obj.members
#     for ind, item in enumerate(col_members):
#         if '_seq' not in item:
#             print(f'{ind} of {len(col_members)}')
#             try:
#                 part_shop.pull(item, doc)
#             except:
#                 pass
# # doc = Document()
# # igem = PartShop('https://synbiohub.org/public/igem')

# doc.write(os.path.join(cwd, f'igem_library.xml'))


#%%%%%


#import the needed libraries
import os, sbol2, json, requests
from sbol2 import BIOPAX_DNA, ComponentDefinition, Sequence, SBOL_ENCODING_IUPAC, Document
from sequences_to_features import FeatureLibrary
from sequences_to_features import FeatureAnnotater



#%%%

def synbict_init(cwd):
    # Load all library sbol files in the folder libraries
    library_list = os.listdir(os.path.join(cwd, 'libraries'))
    library_list = [os.path.join(cwd, 'libraries', x) for x in library_list] #list of file paths to sbol documents of libraries

    feature_doc = []
    for ind, library in enumerate(library_list):
        feature_doc.append(sbol2.Document())
        feature_doc[ind].read(library)

    feature_library = FeatureLibrary(feature_doc)

    # Annotate raw target sequence
    min_feature_length = 40

    annotater = FeatureAnnotater(feature_library, min_feature_length)
    return(annotater)


#define sequence info puller
def seq_file_reader(seq_file, annotator, annotated_num=0):
    problem_rows = []
    molecule_type = BIOPAX_DNA

    doc_read = Document()
    doc_read.read(seq_file)

    for ind, compdef in enumerate(doc_read.componentDefinitions):
        if ind%25 ==0:
            doc_write = Document()

        if ind >-1:
            print(compdef, f'{ind+1} of {len(doc_read.componentDefinitions)}')
            seq_name = str(compdef.sequence)
            seq = doc_read.sequences[seq_name].elements
            component, annotated_num = synbict_use(sequence, compdef.name, annotator, annotated_num=annotated_num)

            component.name= compdef.name

            #adding sequence
            sequence = seq.lower() #removes spaces, enters, and makes all lower case
            sequence_obj = Sequence(f"{compdef.name}_sequence", sequence, SBOL_ENCODING_IUPAC)
            if sequence_name.strip() != "unknown":
                sequence_obj.name = f"{component.name} Sequence"
            doc_write.addSequence(sequence_obj)
            component.sequences = sequence_obj

            doc_write.addComponentDefinition(component)

        if ind%25 ==24:
            sbol_doc.write(os.path.join(cwd, 'igem output', f'igem_file_{ind}.xml'))
        
    return(annotated_num)

#define synbict functionality
def synbict_use(target_seq, seq_name, annotator, min_target_length=0, annotated_num=0):
    annotated_list = annotator.annotate_raw_sequences(target_seq, seq_name, min_target_length)
    # print(annotated_list)

    if (len(annotated_list.componentDefinitions)-1)>0:
        print(len(annotated_list.componentDefinitions)-1)
        annotated_num += 1
    for comp in annotated_list.componentDefinitions:
        if comp.displayId == f'{seq_name}_comp':
            comp_out = comp
    return(comp_out, annotated_num)
#%%%

#define variables
cwd = os.getcwd()
exist_list = []
annotated_num = 0
annotator = synbict_init(cwd)



file_path = os.path.join(cwd,'igem_library.xml')

annotated_num = seq_file_reader(file_path, annotator, annotated_num=annotated_num)

print(f'annotated_num: {annotated_num}')
# print(seq_files.difference(exist_list))
