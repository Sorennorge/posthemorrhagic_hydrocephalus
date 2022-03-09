# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:30:38 2021

@author: dcs839
"""

### Immune analysis ###

## Libs ##

import os

## folders ##

folder = "Results/overview"
folder_info = "Lists/Information"
folder_out = "Results/Immune"

if os.path.exists(folder_out):
    pass
else:
    os.mkdir(folder_out)

## Files ##

file = "Overview_PHH.csv"
file_info = "Information_list.csv"

file_out = "Immune table.csv"
file_out2 = "Immune receptors.csv"

## Key terms ##

Key_terms = []

Key_terms.append('Inflammation'.lower())
Key_terms.append('inflammatory'.lower())
Key_terms.append('Immune'.lower())
Key_terms.append('Cytokine'.lower())
Key_terms.append('Chemokine'.lower())
Key_terms.append('Interleukin'.lower())
Key_terms.append('Lymphokine'.lower())
Key_terms.append('Interferon'.lower())
Key_terms.append('Toll-like receptor'.lower())
Key_terms.append('Tumor necrosis factor'.lower())
Key_terms.append('Transforming growth factor'.lower())
Key_terms.append('Cyclooxygenase'.lower())
Key_terms.append('Oxidative stress'.lower())
Key_terms.append('Epiplexus'.lower())
Key_terms.append('Kolmer'.lower())

## Global variables ##

Ensembl_ids = []
Overview_info = {}

Information_dict = {}

Immune_list = []

Receptor_dict = {}


## Read files ##

# Overview file #
with open(os.path.join(folder,file),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        if line[7] == "Yes":
            Ensembl_ids.append(line[0])
            Overview_info[line[0]] = line[1:8]
        else:
            pass
read.close

#Information file
with open(os.path.join(folder_info,file_info),'r') as read:
    #next(read)
    for line in read:
        line = line.strip().split(";")
        if line[0] in Ensembl_ids:
            Information_dict[line[0]] = line[1:5]
read.close

## Find immune entries ##

for key in Ensembl_ids:
    # If no information is available, pass entry
    if Information_dict[key][2] == '' and Information_dict[key][3] == '':
        pass
    # If information only have go-term search go-terms for search-key
    elif Information_dict[key][2] == '' and Information_dict[key][3] != '':
        for search_term in Key_terms:
            #if Search key in go-term, add key to immune_list, if not there.
            if search_term in Information_dict[key][3].lower():
                if key not in Immune_list:
                    Immune_list.append(key)
                else:
                    pass
            else:
                pass
    # If information only have function and no go-term search function for search-key
    elif Information_dict[key][2] != '' and Information_dict[key][3] == '':
        for search_term in Key_terms:
            #if Search key in function, add key to immune_list, if not there.
            if search_term in Information_dict[key][3].lower():
                if key not in Immune_list:
                    Immune_list.append(key)
                else:
                    pass
            else:
                pass
    # If information only have both function and go-term search function and go-term for search-key
    elif Information_dict[key][2] != '' and Information_dict[key][3] != '':
        for search_term in Key_terms:
            #if Search key in function or go-term, add key to immune_list, if not there.
            if search_term in Information_dict[key][2].lower() or search_term in Information_dict[key][3].lower():
                if key not in Immune_list:
                    Immune_list.append(key)
                else:
                    pass
            else:
                pass
    else:
        print("something went wrong: {}".format(key))

### Get all receptor in name, function and go-term ###

for key in Immune_list:
    
    # Search name #
    if 'receptor' in Information_dict[key][1].lower():
        if key not in Receptor_dict:
            Receptor_dict[key] = {}
            Receptor_dict[key]['Name'] = Information_dict[key][1]
        else:
            Receptor_dict[key]['Name'] = Information_dict[key][1]
    else:
        pass
    
    # Search Function #
    if 'receptor' in Information_dict[key][2].lower():
        if key not in Receptor_dict:
            Receptor_dict[key] = {}
            for item in Information_dict[key][2].split("||"):
                if 'receptor' in item.lower():
                    if 'Function' not in Receptor_dict[key]:
                        Receptor_dict[key]['Function'] = []
                        Receptor_dict[key]['Function'].append(item)
                    else:
                        Receptor_dict[key]['Function'].append(item)
                else:
                    pass
        else:
            pass
    else:
        pass
                    
    # Search Go-term #
    if 'receptor' in Information_dict[key][3].lower():
        if key not in Receptor_dict:
            Receptor_dict[key] = {}
            for item in Information_dict[key][3].split("||"):
                if 'receptor' in item.lower():
                    if 'GOTerm' not in Receptor_dict[key]:
                        Receptor_dict[key]['GOTerm'] = []
                        Receptor_dict[key]['GOTerm'].append(item)
                    else:
                        Receptor_dict[key]['GOTerm'].append(item)
                else:
                    pass
        else:
            pass
    else:
        pass

### Save Immune list, and receptor list to files ###
        
# Immune list #
with open(os.path.join(folder_out,file_out),'w+') as out:
    out.write("Ensembl ID;Gene symbol;Control (TPM);PHH (TPM);Log2FC;Percentage difference;Percentage Orientation;Differential Expresed\n")
    for key in Immune_list:
        out.write("{};{}\n".format(key,";".join(Overview_info[key])))
out.close

# Receptor list #
        
with open(os.path.join(folder_out,file_out2),'w+') as out:
    out.write("Ensembl ID;Gene symbol;Name;Receptor in Name;Function;Go-Term\n")
    for key in Receptor_dict:
        out.write("{};{};{}".format(key,Overview_info[key][0],Information_dict[key][1]))
        if 'Name' in Receptor_dict[key]:
            out.write(";{}".format(Receptor_dict[key]['Name']))
        else:
            out.write(";")
        if 'Function' in Receptor_dict[key]:
            out.write(";{}".format("||".join(Receptor_dict[key]['Function'])))
        else:
            out.write(";")
        if 'GOTerm' in Receptor_dict[key]:
            out.write(";{}".format("||".join(Receptor_dict[key]['GOTerm'])))
        else:
            out.write(";")
        out.write("\n")
out.close