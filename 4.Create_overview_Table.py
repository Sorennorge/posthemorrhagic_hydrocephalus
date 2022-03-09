# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:11:09 2021

@author: dcs839
"""

### Create overview table ###

## Libs ##

import os
import math

## Functions ##

def Percentage_increase( a, b ):      
    P_increase = round(abs( ( b - a ) / a ) * 100,2)
    return( float( P_increase ) )
    
def Log2foldchange( a, b ):
    log2FC = round(math.log2( b / a ),4)
    return( log2FC )

## Folders ##

# Input folders #
folder = "Lists/Count Tables"

# Output folders #
folder_out = "Results"
folder_out2 = "Results/overview"

if os.path.exists(folder_out):
    pass
else:
    os.mkdir(folder_out)

if os.path.exists(folder_out2):
    pass
else:
    os.mkdir(folder_out2)

## Files ##

file1 = "Sample15_control_TPM.csv"
file2 = "Sample16_Treatment_TPM.csv"

file_out = "Overview_PHH.csv"

## Global variables ##

Control_dict = {}
PHH_dict = {}
All_ensembl_ids = []
Log2FC_dict = {}
Percentage_increase_dict = {}
Difference_oritation_dict = {}
Differential_expressed_dict = {}

# Cut_offs #

TPM_cut_off = 1
Percentage_cut_off = 20

## Load files ##

# Control file #
with open(os.path.join(folder,file1),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        Control_dict[line[0]] = [line[2],float(line[3].replace(",","."))]
read.close

# PHH file #
with open(os.path.join(folder,file2),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        PHH_dict[line[0]] = [line[2],float(line[3].replace(",","."))]
read.close

### Create list of all ensembl ids ###
## Exclude ids where TPM below 0.5 of both control and PHH ##
# Add if found in control/PHH and not in the other #
for key in Control_dict:
    # If not found in the PHH, include #
    if key not in PHH_dict:
        # if TPM of Control less than 0.5 and not in control, exclude
        if Control_dict[key][1] < 0.5:
            pass
        elif key not in All_ensembl_ids:
            All_ensembl_ids.append(key)
        else:
            pass
    else:
        #If TPM of both below 0.5, exclude, else include #
        if Control_dict[key][1] < 0.5 and PHH_dict[key][1] < 0.5:
            pass
        elif key not in All_ensembl_ids:
            All_ensembl_ids.append(key)
        else:
            pass
for key in PHH_dict:
    # If not found in the Control, include #
    if key not in Control_dict:
        # if TPM of PHH less than 0.5 and not in control, exclude
        if PHH_dict[key][1] < 0.5:
            pass
        elif key not in All_ensembl_ids:
            All_ensembl_ids.append(key)
        else:
            pass
    else:
        #If TPM of both below 0.5, exclude, else include #
        if Control_dict[key][1] < 0.5 and PHH_dict[key][1] < 0.5:
            pass
        elif key not in All_ensembl_ids:
            All_ensembl_ids.append(key)
        else:
            pass

## sort list of all ensembl ids ##

Sorted_all_ensembl_ids = sorted(All_ensembl_ids)

## calculate Log2FC and percentage increase ##

for key in Sorted_all_ensembl_ids:
    if key in Control_dict and key in PHH_dict:
        Log2FC_dict[key] = Log2foldchange(Control_dict[key][1],PHH_dict[key][1])
        Percentage_increase_dict[key] = Percentage_increase(Control_dict[key][1],PHH_dict[key][1])
        if Control_dict[key][1] == PHH_dict[key][1]:
            Difference_oritation_dict[key] = 'No difference'
        elif Control_dict[key][1] > PHH_dict[key][1]:
            Difference_oritation_dict[key] = 'Decreased'
        else:
            Difference_oritation_dict[key] = 'Increased'
        if abs(Control_dict[key][1] - PHH_dict[key][1]) >= TPM_cut_off and Percentage_increase_dict[key] >= Percentage_cut_off:
            Differential_expressed_dict[key] = 'Yes'
        else:
            Differential_expressed_dict[key] = 'No'
            
## Save to overview file ##
with open(os.path.join(folder_out2,file_out),'w+') as out:
    out.write("Ensembl ID;Gene Symbol;Control (TPM);PHH (TPM);Log2FC;Percentage difference;Percentage Orientation;Differential Expresed\n")
    for key in Sorted_all_ensembl_ids:
        if key in Control_dict and key in PHH_dict:
            # convert float numbers to strings for file writing #
            ctrl_TPM = str(Control_dict[key][1]).replace(".",",")
            PHH_TPM = str(PHH_dict[key][1]).replace(".",",")
            Log2_number = str(Log2FC_dict[key]).replace(".",",")
            percent_number = str(Percentage_increase_dict[key]).replace(".",",")
            #write to file
            out.write("{};{};{};{};{};{};{};{}\n".format(key,Control_dict[key][0],ctrl_TPM,PHH_TPM,Log2_number,percent_number,Difference_oritation_dict[key],Differential_expressed_dict[key]))
        elif key in Control_dict and key not in PHH_dict:
            ctrl_TPM = str(Control_dict[key][1]).replace(".",",")
            out.write("{};{};{};N/A;N/A;N/A;N/A;N/A\n".format(key,Control_dict[key][0],ctrl_TPM))
        elif key not in Control_dict and key in PHH_dict:
            PHH_TPM = str(PHH_dict[key][1]).replace(".",",")
            out.write("{};{};N/A;{};N/A;N/A;N/A;N/A\n".format(key,PHH_dict[key][0],PHH_TPM))
        else:
            print("Something went wrong")
            print(key)
            break
out.close