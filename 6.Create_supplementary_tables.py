# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 08:33:31 2021

@author: dcs839
"""

#### Create Final supplementary tables - Immune respons and receptors ####

## Import packages ###

import os

## Folders ##

Folder1 = "Lists/Information"
Folder2 = "Results/Immune/Manual evaluation"
Folder3 = "Results/Immune"

Folder_out = "Results/Supplementary"

if os.path.exists(Folder_out):
    pass
else:
    os.mkdir(Folder_out)

## Files ##

File1 =  "Information_list.csv"
#We manually evaluated the receptors to see if they are correctly assigned as receptor, and success would be noted as "YES" in column 3.
File2 = "Immune receptors Manual evaluated.csv"
File3 = "Immune table.csv"

File_out1 = "Supplementary_Recetpors.csv"
File_out2 = "Supplementary_immune_respons.csv"

## Global variables ##

Info_dict = {}
Receptor_list = []
Immune_dict = {}

## Load files ##

# Info table #
with open(os.path.join(Folder1,File1),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        if not line[2] == '':
            Info_dict[line[0]] = line[2]
read.close

# Receptor list #

with open(os.path.join(Folder2,File2),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        if line[2].upper() == "YES":
            Receptor_list.append(line[0])
read.close

# Immune dict #

with open(os.path.join(Folder3,File3),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        if not line[0] == '':
            Immune_dict[line[0]] = line[1:7]
read.close


## save receptor supplementary ##

with open(os.path.join(Folder_out,File_out1),'w+') as out:
    out.write("Ensembl ID;Gene symbol;Name;Control (TPM);PHH (TPM);Log2FC;Percentage difference;Percentage Orientation\n")
    for key in Receptor_list:
        out.write("{};{};{};{}\n".format(key,Immune_dict[key][0],Info_dict[key],";".join(Immune_dict[key][1:])))
out.close

## save rest of immune respons supplementary ##

with open(os.path.join(Folder_out,File_out2),'w+') as out:
    out.write("Ensembl ID;Gene symbol;Name;Control (TPM);PHH (TPM);Log2FC;Percentage difference;Percentage Orientation\n")
    for key in Immune_dict:
        if key not in Receptor_list:
            out.write("{};{};{};{}\n".format(key,Immune_dict[key][0],Info_dict[key],";".join(Immune_dict[key][1:])))
        else:
            pass
out.close
