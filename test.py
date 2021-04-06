import sbol2, os
from sbol2 import BIOPAX_DNA, ComponentDefinition

cwd = os.getcwd()

sbol_doc = sbol2.Document()
paper_collect = sbol2.Collection('test collection')
sbol_doc.addCollection(paper_collect)
molecule_type = BIOPAX_DNA
component1 = ComponentDefinition(f'comp1', molecule_type)
component2 = ComponentDefinition(f'comp2', molecule_type)
# print(component1.identity)
paper_collect.members = [component2.identity, component1.identity]
sbol_doc.addComponentDefinition(component1)
sbol_doc.addComponentDefinition(component2)
sbol_doc.write(os.path.join(cwd, f'test12345.xml'))