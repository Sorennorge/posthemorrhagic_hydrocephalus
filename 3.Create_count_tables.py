# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 10:42:59 2021

@author: dcs839
"""

### Rsem to count tables ###

## Import libs ##

import os

### Folder and Files ###

## Folders ##
# Biomart folder
folder1 = "Lists"
# RSEM file folder
folder2 = "Lists/Rsem"


folder_out = "Lists/Count Tables"

# if output folder doesn't exists, make one
if os.path.exists(folder_out):
    pass
else:
    os.mkdir(folder_out)

## Files ##

# Biomart #
file_biomart = "Rat_biomart.txt"

# Input files #
file1 = "Sample15_rsem.txt"
file2 = "Sample16_rsem.txt"

# Output files #
file1_out = "Sample15_control_TPM.csv"
file2_out = "Sample16_Treatment_TPM.csv"

## Variables ##

biomart = {}

sample15_rsem_gene_ids = {}
sample16_rsem_gene_ids = {}


### Read files ###

## Read biomart ##
with open(os.path.join(folder1,file_biomart),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(",")
        biomart[line[0]] = line[1].upper()
read.close


## Sample 15 ##

with open(os.path.join(folder2,file1),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split("\t")
        #if TPM > 0, add to dict
        if float(line[5]) > 0:
            # Make sure there isnt dublicates
            if not line[0] in sample15_rsem_gene_ids:
                sample15_rsem_gene_ids[line[0]] = line[1:]
            else:
                print(line[0])
                break
read.close

## Sample 16 ##

with open(os.path.join(folder2,file2),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split("\t")
        #if TPM > 0, add to dict
        if float(line[5]) > 0:
            # Make sure there isnt dublicates
            if not line[0] in sample16_rsem_gene_ids:
                sample16_rsem_gene_ids[line[0]] = line[1:]
            else:
                print(line[0])
                break
read.close


### Save count table to file ###

## Sample X1 ##

with open(os.path.join(folder_out,file1_out),'w+') as out:
    #Add header
    out.write("Ensembl gene id;Ensembl transcripts;Gene Symbol;TPM\n")
    for key in sample15_rsem_gene_ids:
        if biomart[key] == '':
            out.write("{};{};Missing information;{}\n".format(key,sample15_rsem_gene_ids[key][0],sample15_rsem_gene_ids[key][4].replace(".",",")))
        else:
            out.write("{};{};{};{}\n".format(key,sample15_rsem_gene_ids[key][0],biomart[key],sample15_rsem_gene_ids[key][4].replace(".",",")))
out.close

### Save count table to file ###

## Sample X2 ##

with open(os.path.join(folder_out,file2_out),'w+') as out:
    #Add header
    out.write("Ensembl gene id;Ensembl transcripts;Gene Symbol;TPM\n")
    for key in sample16_rsem_gene_ids:
        if biomart[key] == '':
            out.write("{};{};Missing information;{}\n".format(key,sample16_rsem_gene_ids[key][0],sample16_rsem_gene_ids[key][4].replace(".",",")))
        else:
            out.write("{};{};{};{}\n".format(key,sample16_rsem_gene_ids[key][0],biomart[key],sample16_rsem_gene_ids[key][4].replace(".",",")))
out.close
