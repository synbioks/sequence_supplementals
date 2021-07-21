#pull basic unique promoter sequences (2495)
#run synbict like for seq supplementals

#basic unique rbs
import os, sbol2
from sbol2.constants import SBOL_ENCODING_IUPAC
from sequences_to_features import FeatureLibrary
from sequences_to_features import FeatureAnnotater

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
    min_feature_length = 10

    annotater = FeatureAnnotater(feature_library, min_feature_length)
    return(annotater)

#%%

cwd = os.getcwd()
annotator = synbict_init(cwd)

rbs_files = os.listdir(os.path.join(cwd, 'Basic_Unique_RBS_SBOL'))

annotated_num = 0
# output_ind = 0
annotated_doc = sbol2.Document()
for ind, file in enumerate(rbs_files): # there are 448 unqiue basic  rbs sequence files
    if ind > -1: # useful for testing
        print(ind)
        doc = sbol2.Document()
        doc.read(os.path.join(cwd, 'Basic_Unique_RBS_SBOL', file))
        for seq in doc.sequences:
            sequence = seq.elements
            file_name = file.split(".")[0]
            annotated_list = annotator.annotate_raw_sequences(sequence, f'{file_name}', 0)
            annotated_comp = annotated_list.componentDefinitions[f'http://examples.org/ComponentDefinition/{file_name}_comp/1']
            sbolobj_seq = sbol2.Sequence(f'{file_name}_seq', sequence, SBOL_ENCODING_IUPAC)
            annotated_comp.sequence = sbolobj_seq
            annotated_doc.addComponentDefinition(annotated_comp)
            annotated_doc.addSequence(sbolobj_seq)
            # annotated_doc.addSequence(sequence)
    # if (ind+1)%100 == 0:
    #     annotated_doc.write(os.path.join(cwd, f'igem_basic_unique_rbs_synbict_annotated_{output_ind}.xml'))
    #     output_ind +=1
    #     annotated_doc = sbol2.Document()
annotated_doc.write(os.path.join(cwd, f'igem_basic_unique_rbs_synbict_annotated_ALL.xml'))