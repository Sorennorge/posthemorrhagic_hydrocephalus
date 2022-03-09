# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:32:37 2021

@author: dcs839
"""

### Information table ###

## Libs ##

import os
import mygene

## Functions ##

mg = mygene.MyGeneInfo()

## Folders ##

folder = "Lists/Count Tables"
folder_out = "Lists/Information"

if os.path.exists(folder_out):
    pass
else:
    os.mkdir(folder_out)

## Files ##

file1 = "Sample15_Saline_TPM.csv"
file2 = "Sample16_Blood_TPM.csv"

File_out1 = "Information_list.csv"
File_out2 = "Failed_entries_ensembl_ids.csv"


## Global variables ##

Information_dict = {}
Info_first = {}
Info_list = {}

## Load entry list ##

with open(os.path.join(folder,file1),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        Information_dict[line[0]] = line[2]
        Info_first[line[0]] = line[2]
read.close

with open(os.path.join(folder,file2),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        if line [0] not in Information_dict:
            Information_dict[line[0]] = line[2]
        else:
            pass
read.close

### Program ###

## Initialize progress counter ##
counter = 0

with open(os.path.join(folder_out, File_out2),'w+') as out2:
    with open(os.path.join(folder_out,File_out1),'w+',encoding="utf-8") as out:
        out.write("ID;Gene;Name;Function;Go terms\n")
        for key in Information_dict:
            ## progress info ##
            counter += 1
            print("{} - {}/{}".format(key,counter,len(Information_dict)))
            ### Get lookup values ###
            ## Initialize local variables ##
            lookup = []
            Info_list[key] = {}
            ## get lookup ##
            try:
                lookup = mg.getgene(key)
            except:
                #print("Case 2: {}".format(key))
                out2.write("{}\n".format(key))
                print("case 1")
            ### Initialize dicts ###
            ## Info_list ##
            Info_list[key]['symbol'] = []
            Info_list[key]['name'] = []
            Info_list[key]['go'] = []
            Info_list[key]['pathway'] = []
            
            ## If more entries have been written to ensembl id, take the first ##
            if isinstance(lookup,list):
                lookup = lookup[0]
            else:
                pass
            
            ### Complete info list ###
            if not lookup:
                out.write("{};;;;;;\n".format(key))
                print("case 3")
                continue
                
            
            ### Handle Symbol ###
            try:
                if lookup:
                    if 'symbol' in lookup.keys():
                        if isinstance(lookup['symbol'],str):
                            Info_list[key]['symbol'].append(lookup['symbol'].upper())
                        elif isinstance(lookup['symbol'],list):
                            for item in lookup['symbol']:
                                Info_list[key]['symbol'].append(item.upper())
                    else:
                        pass
                else:
                    pass
                
                ### Handle Names ###
                if lookup:
                    if 'name' in lookup.keys():
                        if isinstance(lookup['name'],str):
                            Info_list[key]['name'].append(lookup['name'].replace(';',',').capitalize())
                        elif isinstance(lookup['name'],list):
                            for item in lookup['name']:
                                Info_list[key]['name'].append(item.replace(';',',').capitalize())
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                
                ### Handle Function ###
                if lookup:
                    if 'pathway' in lookup.keys():
                        if 'reactome' in lookup['pathway']:
                            if 'name' in lookup['pathway']['reactome']:
                                Info_list[key]['pathway'].append(lookup['pathway']['reactome']['name'])
                            elif len(lookup['pathway']['reactome']) > 1:
                                for item in lookup['pathway']['reactome']:
                                    Info_list[key]['pathway'].append(item['name'])
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                
                ### Handle Go terms ###
                if lookup:
                    if 'go' in lookup.keys():
                        for category in lookup['go']:
                                if 'term' not in lookup['go'][category]:
                                    for item in lookup['go'][category]:
                                        if item['term'].lower() not in Info_list[key]['go']:
                                            Info_list[key]['go'].append(item['term'].lower())
                                        else:
                                            pass
                                else:
                                    Info_list[key]['go'].append(lookup['go'][category]['term'].lower())
                    else:
                        pass
                else:
                    pass
                ### Save to file ###
                if lookup:
                    out.write("{};{};{};{};{}\n".format(key,"||".join(Info_list[key]['symbol']),"||".join(Info_list[key]['name']),"||".join(Info_list[key]['pathway']),"||".join(Info_list[key]['go'])))
                else:
                    pass
            except:
                out2.write("{}\n".format(key))
                print("case 2")
    out.close
out2.close
