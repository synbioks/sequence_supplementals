#expected format of .seq.txt files is:
# <unknown|sequence_name>:<articleID>:<pathname_of_file>:<seq_count>

#each supplemental file has a .seq.txt associated with it

# import csv
import os
import glob
from sbol2 import Document, Collection, Component, ComponentDefinition
from sbol2 import BIOPAX_DNA, Sequence, SBOL_ENCODING_IUPAC, Config, SO_CIRCULAR

def check_name(name_to_check):
    """
    the function verifies that the names is alphanumeric and separated by underscores
    if that is not the case the special characters are replaced by their unicode decimal code number

    Parameters
    ----------
    name_to_check : string
    
    Returns
    -------
    compliant_name : string
        alphanumberic name with special characters replaced by _u###
    """
    
    
    if not bool(re.match('^[a-zA-Z0-9]+$', name_to_check)):
        #replace special characters with numbers
        for letter in name_to_check:
            if ord(letter) > 122:
                #122 is the highest decimal code number for common latin letters or arabic numbers
                #this helps identify special characters like ä or ñ, which isalnum() returns as true
                #the characters that don't meet this criterion are replaced by their decimal code number separated by an underscore
                name_to_check = name_to_check.replace(letter, str( f"_{ord(letter)}"))
            elif ord(letter) == 32:
                name_to_check = name_to_check.replace(letter, "_")
            else:
                letter = re.sub('[\w, \s]', '', letter) #remove all letters, numbers and whitespaces
                #this enables replacing all other special characters that are under 122
                if len(letter) > 0:
                    name_to_check = name_to_check.replace(letter, str( f"_u{ord(letter)}_"))
    
    if name_to_check[0].isnumeric():
        #ensures it doesn't start with a number
        name_to_check = f"_{name_to_check}"

    return(name_to_check)

cwd = os.getcwd()
path_in = os.path.join(cwd, "sequences-files")

supplemental_dict = {}

doc = Document()
problem_rows = []
molecule_type = BIOPAX_DNA
component_defs_added = 0
new_docs = 0
for file_name in glob.glob(os.path.join(path_in, "*.seq.txt")):
    
    with open(file_name, 'rt') as names:
        print(file_name)
        #split file based on > at the start of each information row
        rows = names.read().split('>')
        for i, row in enumerate(rows):
            if len(row)>0:
                print(row)
                #information row is separated by |
                if len([field.strip() for field in row.split('|')])==5:
                    sequence_name, doi, pathname_of_file, seq_count, seq = [field.strip() for field in row.split('|')]
                else:
                    problem_rows.append(row)
                    continue
                

                sequence = "".join([field.strip() for field in seq.split('\n')])

                #create sbol files with dictionary entry
                articleID = pathname_of_file.split('/')[0]
                # name_use = check_name(articleID)
                component = ComponentDefinition(f'{articleID}_{i}', molecule_type)
                component.wasGeneratedBy =  "https://synbiohub.org/public/sbksactivities/ACS_Synbio_Generation/1"
                component.wasDerivedFrom = f'https://doi.org/{doi}'
                if sequence_name != "unknown" and sequence_name != "_unknown_seq":
                    component.name= sequence_name

                #adding sequence
                sequence = sequence.lower() #removes spaces, enters, and makes all lower case
                sequence_obj = Sequence(f"{articleID}_{i}_sequence", sequence, SBOL_ENCODING_IUPAC)
                if sequence_name.strip() != "unknown":
                    sequence_obj.name = f"{component.name} Sequence"
                doc.addSequence(sequence_obj)
                component.sequences = sequence_obj

                #this is to ensure the documents don't get too big
                if component_defs_added<100:
                    doc.addComponentDefinition(component)
                    component_defs_added += 1
                else:
                    doc.write(os.path.join(path_in, f'output_sbol_{new_docs}.xml'))
                    new_docs += 1
                    doc = Document()
                    doc.addComponentDefinition(component)
                    component_defs_added = 1

# print(supplemental_dict)
print(problem_rows)
doc.write(os.path.join(path_in, 'output_sbol.xml'))