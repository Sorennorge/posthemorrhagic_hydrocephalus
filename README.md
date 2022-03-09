# MacAulayLab RNAseq2 - Posthemorrhagic hydrocephalus #
The work and scripts are done by the MacAulay Lab.\
All programs used are free and open-source.
In the interest of open science and reproducibility, all data and source code used in our research is provided here.\
Feel free to copy and use code, but make sure to cite: XXXXXXXX (coming soon)\
*Remember* rewrite file_names and folder_names suitable for your pipeline.\
Note: Many of the tables output have converted dot to comma for danish excel annotation.
## Raw data analysis - Library Build, Mapping and Quantification ##
*Remember* rewrite file_names and folder_names suitable for your pipeline.
### RNA-STAR and RSEM Library build and indexing ###
Use these two files:\
1.1.RNA_STAR_Indexing.sh\
2.1.RSEM_Indexing.sh

### RNA-STAR Mapping and RSEM quantification ###
Use:\
1.2.RNA_STAR_RNAseq2.sh\
2.2.RSEM_RNAseq2.sh

### Count Tables with gene information ###
Requirements:\
Biomart of Rnor6.0 with Attributes: Gene stable ID & Gene name\
Use:\
3.Create_count_tables.py

### Get overview tables - and differential expressed genes ###
Use:\
4.Create_overview_Table.py

### Collect immune information and seperate into receptors and non-receptors ###
Use:\
5.1.Information_table_list
5.2.Immune_analysis

### Create supplementary tables ###
Use:\
6.Create_supplementary_tables
