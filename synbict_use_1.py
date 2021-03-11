import sbol2, logging, os
from sbol2 import Component, ComponentDefinition
from sequences_to_features import FeatureLibrary
from sequences_to_features import FeatureAnnotater

cwd = os.getcwd()

# Set pySBOL configuration parameters
sbol2.setHomespace('http://mynamespace.org')
sbol2.Config.setOption('validate', True)
sbol2.Config.setOption('sbol_typed_uris', False)

# Set up log file - can be commented out
logger = logging.getLogger('synbict')
logger.setLevel(logging.DEBUG)
logger.propagate = False

formatter = logging.Formatter('%(asctime)s ; %(levelname)s ; %(message)s')

file_handler = logging.FileHandler('SrpR_annotation_log.txt', "w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Load Cello genetic circuit feature library
feature_doc = sbol2.Document()
feature_doc.read(os.path.join(cwd, 'test', 'cello_library.xml'))

feature_library = FeatureLibrary([feature_doc])

# Annotate raw target sequence
min_feature_length = 40

annotater = FeatureAnnotater(feature_library, min_feature_length)    

seq_name = 'seq_name1'
# doi = 'ttt.ttt/dkjsk'
# sequence_name = "seq_test"
target_seq = (
    'CTGAAGCGCTCAACGGGTGTGCTTCCCGTTCTGATGAGTCCGTGAGGACGAAAGCGCCTCTACAAATAATTTTGTTTAAGAGTCTATGGACTATGTTTTCACAAAGGAAGTACCAGGATGGCACGTAAAACCGCAGCAGAAGCAGAAGAAACCCGTCAGCGTATTATTGATGCAGCACTGGAAGTTTTTGTTGCACAGGGTGTTAGTGATGCAACCCTGGATCAGATTGCACGTAAAGCCGGTGTTACCCGTGGTGCAGTTTATTGGCATTTTAATGGTAAACTGGAAGTTCTGCAGGCAGTTCTGGCAAGCCGTCAGCATCCGCTGGAACTGGATTTTACACCGGATCTGGGTATTGAACGTAGCTGGGAAGCAGTTGTTGTTGCAATGCTGGATGCAGTTCATAGTCCGCAGAGCAAACAGTTTAGCGAAATTCTGATTTATCAGGGTCTGGATGAAAGCGGTCTGATTCATAATCGTATGGTTCAGGCAAGCGATCGTTTTCTGCAGTATATTCATCAGGTTCTGCGTCATGCAGTTACCCAGGGTGAACTGCCGATTAATCTGGATCTGCAGACCAGCATTGGTGTTTTTAAAGGTCTGATTACCGGTCTGCTGTATGAAGGTCTGCGTAGCAAAGATCAGCAGGCACAGATTATCAAAGTTGCACTGGGTAGCTTTTGGGCACTGCTGCGTGAACCGCCTCGTTTTCTGCTGTGTGAAGAAGCACAGATTAAACAGGTGAAATCCTTCGAATAATTCAGCCAAAAAACTTAAGACCGCCGGTCTTGTCCACTACCTTGCAGTAATGCGGTGGACAGGATCGGCGGTTTTCTTTTCTCTTCTCAATCTATGATTGGTCCAGATTCGTTACCAATTGACAGCTAGCTCAGTCCTAGGTATATACATACATGCTTGTTTGTTTGTAAAC'
)

min_target_length = 0
annotated_doc = sbol2.Document()

# Annotate
annotated_comp = annotater.annotate_raw_sequences(target_seq, seq_name, min_target_length)
print(annotated_comp)
annotated_comp.wasGeneratedBy =  "https://synbiohub.org/public/sbksactivities/ACS_Synbio_Generation/1"
# annotated_comp.wasDerivedFrom = f'https://doi.org/{doi}'
# if sequence_name != "unknown" and sequence_name != "_unknown_seq":
#     annotated_comp.name= sequence_name
annotated_doc.addComponentDefinition(annotated_comp)

#Write Document
annotated_doc.write(os.path.join(cwd, 'synbict_output', f'{seq_name}.xml'))