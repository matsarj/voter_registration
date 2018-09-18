import pandas as pd
import os
import shutil


rootdir = r'C:\Users\ASUS\Documents\Data\Voter Registration\California Voter Registration'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        
        if 'county' in os.path.join(subdir, file):
            county = pd.read_excel(subdir + '\\' + file)
            
            fixed_path = rootdir + '\\fixed\\' + subdir[subdir.rfind('\\') + 1:] + '_' + file
            os.makedirs(os.path.dirname(fixed_path), exist_ok=True)
            
            if '2016-01-05' in subdir:
                county.rename(columns={ county.columns[0]: "County" }, inplace = True)
            
            if 'County' not in county.columns:
                county = county.reset_index().rename(columns={county.index.name:'County'})
            county.drop(county[county.isnull().all(axis = 1)].index, axis = 0, inplace = True)
            county.drop(county.columns[county.isnull().all(axis = 0)], axis = 1, inplace = True)
            fixed = county[::2]
                        
            #File on website has column listed *Eligible instead of Eligible
            #for 05-21-2018
            if '2018-05-21' in subdir:
                fixed.rename(columns={ fixed.columns[1]: "Eligible" }, inplace = True)
            
            #Sum is off by 2 for 12-7-2007
            if '2007-12-07' in subdir:
                fixed['Eligible'].values[-1] = fixed['Eligible'][:-1].sum()
                
            if fixed['Eligible'][:-1].sum() == fixed['Eligible'].values[-1]:
                fixed.to_csv(fixed_path)
            else:
                print(os.path.join(subdir, file))
                

       
                
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(subdir)
        if 'fixed' in subdir:
            os.remove(os.path.join(subdir, file))
            os.rmdir(subdir)


county = pd.read_excel(r"C:\Users\ASUS\Documents\Data\Voter Registration\California Voter Registration\2016-01-05\county.xls")