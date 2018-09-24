import pandas as pd
import os
import shutil


rootdir = r'C:\Users\ASUS\voter_registration\California Voter Registration'

data = pd.read_excel(r"C:\Users\ASUS\voter_registration\California Voter Registration\2012-04-06\politicalsub1.xls")
df2 = data.reset_index(level = 1)

counties = [(ind, county) for ind, (county, district, other) in enumerate(data.index)
             if county == county and ('Total' not in county)]
districts = [(ind, district) for ind, (county,district) in enumerate(data.index) 
            if district == district and all(x not in district for x in ['District', 'Cities', 'Percent'])] 
        

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if 'politicalsub' in os.path.join(subdir, file):
            data = pd.read_excel(subdir + '\\' + file)
            if data.index.nlevels == 3:
                data.reset_index(level = 1, drop = True, inplace = True)                    
            
            fixed_path = rootdir + '\\fixed\\' + subdir[subdir.rfind('\\') + 1:] + '_' + 'county_data.csv'
            os.makedirs(os.path.dirname(fixed_path), exist_ok=True)
            
            counties = [(ind, county) for ind, (county, district) in enumerate(data.index)
                         if county == county and 
                         all(x not in county for x in ['Total', 'District', 'Cities', 'Percent'])] 
            
            districts = [(ind, district) for ind, (county,district) in enumerate(data.index) 
                        if district == district and 
                        all(x not in district for x in ['District', 'Cities', 'Percent'])] 
            
            data = data.reset_index(drop = True)
            
            data = data.loc[[ind for (ind, district) in districts],]
            
            data['county'] = pd.cut(data.index, bins = [0] + [max(1, i) for i, x in counties] + [float('inf')], 
                   labels = ['none'] +  [x for i, x in counties], include_lowest = True).tolist()
            
            data['district'] = [district for (ind, district) in districts]
            data = data.reset_index(drop = True)
            
            data = data.set_index(['county', 'district']).unstack().reset_index().fillna(0)
            data.columns = [y + '_' + x  for x, y in data.columns]
            data.rename(columns={ data.columns[0]: 'county'}, inplace = True)
    
            data.to_csv(fixed_path, index = False)
