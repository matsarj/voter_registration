import pandas as pd
import os

def transform(rootdir, date_start, date_end):
    rootdir = r'C:\Users\ASUS\voter_registration\California Voter Registration'
    all_years = pd.DataFrame()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if 'politicalsub' in os.path.join(subdir, file):
                data = pd.read_excel(subdir + '\\' + file)
                date = subdir[subdir.rfind('\\') + 1:]
                fixed_path = rootdir + '\\fixed\\' + date + '_' + 'county_data.csv'
                os.makedirs(os.path.dirname(fixed_path), exist_ok=True)
                
                
                if data.index.nlevels == 3:
                    data.reset_index(level = 1, drop = True, inplace = True)                    
                
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
                
                types = ['County Supervisorial', 'US Congressional', 'State Senate', 
                         'State Assembly', 'State Board of Equalization']
                
                district_type = list()
                for place in data['district']:
                    check = [t for t in types if t in place]
                    district_type += check if check else ['City']
                    
                data['district_type'] = district_type
                                
                data['date'] = date
                data.columns = ['_'.join(col.split()) for col in data.columns]
                data.to_csv(fixed_path, index = False)
                
                all_years = pd.concat([all_years, data], sort = True)
                


