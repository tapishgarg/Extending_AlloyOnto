from owlready2 import *
import numpy as np
import pandas as pd
import os

## Specify the path for existing owl file
onto = get_ontology("file:///Users/tapishgarg/Documents/BTP-Ontologies/Extending_AlloyOnto/AlloyOnto6.owl")
onto.load()

print(onto.get_namespace(onto.base_iri))
print(list(onto.classes()))


## Import excel sheet 
data = pd.read_excel("/Users/tapishgarg/Documents/BTP-Ontologies/Extending_AlloyOnto/Phases_Properties_2.xlsx")
data_2 = pd.read_excel("/Users/tapishgarg/Documents/BTP-Ontologies/Extending_AlloyOnto/Phases_reaction.xlsx")


## Create Class

class Phase_Properties(Thing):
    namespace = onto


## Create Subclass

class Pearson_Symbol(Phase_Properties):
    pass

class Space_Group(Phase_Properties):
    pass


## Create Object Properties

with onto:
    class hasPearsonSymbol(ObjectProperty):
        domain = [onto.Phase]
        range = [onto.Pearson_Symbol]
        pass

with onto:
    class hasSpaceGroup(ObjectProperty):
        domain = [onto.Phase]
        range = [onto.Space_Group]

# with onto:
#     class hasParentPhase(ObjectProperty):
#         domain = [onto.Reaction]
#         range = [onto.Phase]

# with onto:
#     class hasProductPhase(ObjectProperty):
#         domain = [onto.Reaction]
#         range = [onto.Phase]
        

## Create Inverse Properties

with onto:
    class pearsonSymbolIn(ObjectProperty):
        domain = [onto.Pearson_Symbol]
        range = [onto.Phase]
        inverse_property = hasPearsonSymbol

with onto:
    class spaceGroupIn(ObjectProperty):
        domain = [onto.Space_Group]
        range = [onto.Phase]
        inverse_property = hasSpaceGroup


## Create Data Properties

with onto:
    class density_of_phase(DataProperty):
        domain = [onto.Phase]
        range = [float]

    class volume_of_phase(DataProperty):
        domain = [onto.Phase]
        range = [float]


## Create Individuals for a class

with onto:
    for i in range(data.shape[0]):
        pearson_symbol = onto.Pearson_Symbol(data["Pearson_Symbol"][i])
    # pearson_symbol = onto.Pearson_Symbol()

    for i in range(data.shape[0]):
        space_group = onto.Space_Group(data["Space Group"][i])


## Creating Axioms

with onto:
    for i in range(data.shape[0]):
        individual = onto.Phase(data['Formula'][i])
        individual.hasPearsonSymbol.append(onto.Pearson_Symbol(data['Pearson_Symbol'][i]))
        individual.hasSpaceGroup.append(onto.Space_Group(data['Space Group'][i]))
        individual.density_of_phase.append(float(data['Density'][i]))
        individual.volume_of_phase.append(float(data['Volume'][i]))

    ## Adding Parent and Product Phase

    # for i in range(data_2.shape[0]):
    #     individual = onto.Reaction(data_2['Reaction Name 1'][i])
    #     if data_2['Invariant Reaction'][i] in ["Monotectic"]:
    #         individual.hasProductPhase.append(onto.Phase(data_2["Phase 3"][i]))


onto.save(file="./AlloyOnto7.owl", format="rdfxml")