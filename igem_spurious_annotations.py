# import requests
# import os

# cwd = os.getcwd()


# with open('spurious_real_igem_uris.csv', 'r') as f:
#     lines = f.readlines()

# for ind, line in enumerate(lines):
#     if 0<ind:
#         print(ind)
#         line = line.split(',')
#         spurious = line[0]
#         real = line[1].replace('\n', '')
#         real_name = real.split('/')[-2]
#         spur_name = spurious.split('/')[-2]

#         real_out_path = os.path.join(cwd, 'spurious_and_real_xml',
#                                      f'{real_name}.xml')
#         spur_out_path = os.path.join(cwd, 'spurious_and_real_xml',
#                                      f'{spur_name}.xml')

#         r = requests.get(f'{real}/sbol')
#         with open(real_out_path, 'w') as f:
#             f.write(r.text)

#         r = requests.get(f'{spurious}/sbol')
#         with open(spur_out_path, 'w') as f:
#             f.write(r.text)

#################################################################
# import os
# import sbol2
# from sbol2.constants import SBOL_ENCODING_IUPAC
# from sequences_to_features import FeatureLibrary
# from sequences_to_features import FeatureAnnotater


# def synbict_init(cwd):
#     # Load all library sbol files in the folder libraries
#     library_list = os.listdir(os.path.join(cwd, 'libraries'))

#     # list of file paths to sbol documents of libraries
#     library_list = [os.path.join(cwd, 'libraries', x) for x in library_list]

#     feature_doc = []
#     for ind, library in enumerate(library_list):
#         feature_doc.append(sbol2.Document())
#         feature_doc[ind].read(library)

#     feature_library = FeatureLibrary(feature_doc)

#     # Annotate raw target sequence
#     min_feature_length = 10

#     annotater = FeatureAnnotater(feature_library, min_feature_length)
#     return(annotater)


# use_real = True

# cwd = os.getcwd()
# annotator = synbict_init(cwd)

# with open('spurious_real_igem_uris.csv', 'r') as f:
#     lines = f.readlines()

# annotated_doc = sbol2.Document()
# for ind, line in enumerate(lines):
#     if 0 < ind:  # useful for testing
#         print(ind)
#         doc = sbol2.Document()

#         line = line.split(',')
#         spurious = line[0]
#         real = line[1].replace('\n', '')
#         real_name = real.split('/')[-2]
#         spur_name = spurious.split('/')[-2]

#         if use_real:
#             file_nm = real_name
#         else:
#             file_nm = spur_name

#         doc.read(os.path.join(cwd, 'spurious_and_real_xml', f'{file_nm}.xml'))
#         for seq in doc.sequences:
#             if use_real:
#                 pref = 'real'
#             else:
#                 pref = 'spurious'
#             sequence = seq.elements
#             comp_name = f'{pref}_{file_nm}'
#             annotated_list = annotator.annotate_raw_sequences(sequence,
#                                                               comp_name, 0)
#             annotated_comp = annotated_list.componentDefinitions[f'http://examples.org/ComponentDefinition/{comp_name}_comp/1']
#             sbolobj_seq = sbol2.Sequence(f'{comp_name}_seq', sequence,
#                                          SBOL_ENCODING_IUPAC)
#             annotated_comp.sequence = sbolobj_seq
#             annotated_doc.addComponentDefinition(annotated_comp)
#             annotated_doc.addSequence(sbolobj_seq)

# if use_real:
#     annotated_doc.write(os.path.join(cwd, 'annotated_real_igem.xml'))
# else:
#     annotated_doc.write(os.path.join(cwd, 'annotated_spurious_igem.xml'))
#############################################################################

# READ IN THE TWO FILES 104 and 106 and count annotations#############
import sbol2
import os

cwd = os.getcwd()

doc = sbol2.Document()
doc.read(os.path.join(cwd, 'annotated_spurious_igem.xml'))

for ind, cd in enumerate(doc.componentDefinitions):
    if -1 < ind:
        print(ind)
        anno_list = []
        range_list = []
        for anno in cd.sequenceAnnotations:
            for loc in anno.locations:
                if [loc.start, loc.end] not in range_list:
                    anno_list.append([anno.identity, loc.start, loc.end])
                    range_list.append([loc.start, loc.end])
        with open('annotated_spurious_count.txt', 'a') as f:
            f.write(f'{cd.identity}|{len(anno_list)}|{anno_list}\n')
