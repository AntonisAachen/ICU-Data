#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 08:37:51 2023

@author: administrator
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
#from definitions import render_mpl_table

#%%

SICdb_cases = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/cases.csv')
SICdb_d_references = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/d_references.csv', usecols=[0,1])
SICdb_data_range = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/data_range.csv')
SICdb_data_ref = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/data_ref.csv')
SICdb_lab = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/laboratory.csv')
SICdb_med = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/medication.csv')
SICdb_unitlog = pd.read_csv('/Users/administrator/Documents/SICdb/salzburg-intensive-care-database-sicdb-a-freely-accessible-intensive-care-database-1.0.6/unitlog.csv')
ref_dict = SICdb_d_references.set_index('ReferenceGlobalID').to_dict()
SICdb_cases['ReferringUnit'] = SICdb_cases['ReferringUnit'].map(ref_dict['ReferenceValue'])
SICdb_cases['Sex'] = SICdb_cases['Sex'].map(ref_dict['ReferenceValue'])
SICdb_cases['HospitalUnit'] = SICdb_cases['HospitalUnit'].map(ref_dict['ReferenceValue'])
SICdb_cases['WeightOnAdmission'] = SICdb_cases['WeightOnAdmission'].replace(0, np.nan)
SICdb_cases['HeightOnAdmission'] = SICdb_cases['HeightOnAdmission'].replace(0, np.nan)
SICdb_cases['BMI']= (SICdb_cases['WeightOnAdmission'].div(1000))/SICdb_cases['HeightOnAdmission'].div(100).pow(2)

#%%

SICdb_admissions_per_year = SICdb_cases.groupby(['AdmissionYear']).size()
SICdb_admission_year_sex = SICdb_cases.groupby(['AdmissionYear','Sex']).size()
SICdb_admission_year_sex_perc = SICdb_admission_year_sex / SICdb_admission_year_sex.groupby(level=[0]).transform('sum') # percentages of males, females, level refers to index level

#%%

SICdb_admission_year_age = pd.DataFrame([SICdb_cases['AdmissionYear'],SICdb_cases['AgeOnAdmission']]).transpose()
SICdb_admission_year_age =SICdb_admission_year_age.groupby('AdmissionYear').mean()
SICdb_admission_year_age = SICdb_admission_year_age.round(2)

#%%

SICdb_admission_year_weight = pd.DataFrame([SICdb_cases['AdmissionYear'],SICdb_cases['WeightOnAdmission']]).transpose()
SICdb_admission_year_weight = SICdb_admission_year_weight.groupby('AdmissionYear').mean()/1000
SICdb_admission_year_weight = SICdb_admission_year_weight.round(2)

#%%

SICdb_admission_year_height = pd.DataFrame([SICdb_cases['AdmissionYear'],SICdb_cases['HeightOnAdmission']]).transpose()
SICdb_admission_year_height = SICdb_admission_year_height.groupby('AdmissionYear').mean().round(2)

#%%

SICdb_admission_year_bmi = pd.DataFrame([SICdb_cases['AdmissionYear'],SICdb_cases['BMI']]).transpose()
SICdb_admission_year_bmi = SICdb_admission_year_bmi.groupby('AdmissionYear').mean()

#%%

SICdb_units = SICdb_cases.groupby(['ReferringUnit', 'AdmissionYear']).size().reset_index()
SICdb_units.columns = ['Referring Unit','Admission Year','No. Patients']
SICdb_units = SICdb_units.pivot(index = 'Referring Unit', columns = 'Admission Year', values = 'No. Patients')
SICdb_units = SICdb_units.fillna(0)
sns.heatmap(SICdb_units, annot=True)
plt.draw()

#%%

