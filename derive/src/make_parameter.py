import os
import pandas as pd

def copy_file(source, destination):
    with open(source, 'rb') as f_source:
        with open(destination, 'wb') as f_destination:
            # Read and write the file in chunks to conserve memory
            for chunk in iter(lambda: f_source.read(4096), b''):
                f_destination.write(chunk)
                
                
def make_param(Name='NUE_OPT',pft_dependent='y',prior = 1,pft = 6,
               vmin_max = []):
    
    set_variable = 'p = paramdef.add("{}", pft= "{}")'.format(Name, pft_dependent)
    
    # if there are max and min value
    if len(vmin_max) == 2:
        if pft_dependent == 'y':
            set_value = 'p.set(vdef = {}, vmin = {}, vmax = {}, pft = {})'.format(prior,vmin_max[0],vmin_max[1], pft)
        else:
            set_value = 'p.set(vdef = {}, vmin = {}, vmax = {})'.format(prior,vmin_max[0],vmin_max[1])
    else:
        if pft_dependent == 'y':
            set_value = 'p.set(vdef = {}, fmin = fmin, fmax = fmax, pft = {})'.format(prior, pft)
        else:
            set_value = 'p.set(vdef = {}, fmin = fmin, fmax = fmax)'.format(prior)
            
    return [set_variable,set_value]


def make_K_LATOSA_MIN(K_LATOSA_prior = 1,K_LATOSA_vmin_max = [],pft = 6):
    
    str1 = 'p = paramdef.add("K_LATOSA_MIN", pft="y", units="1", desc="minimum leaf-to-sapwood area ratio")'
    str2 = 'p.set(vdef = {}, fmin = fmin, fmax = fmax, pft={})'.format(K_LATOSA_prior,pft)
    
    # if there are max and min value
    if len(K_LATOSA_vmin_max) ==2:
        str2 = 'p.set(vdef = {}, vmin = {}, vmax = {}, pft={})'.format(K_LATOSA_prior,K_LATOSA_vmin_max[0],K_LATOSA_vmin_max[1], pft)
     
    return [str1,str2]

def make_K_LATOSA_FRAC(K_LATOSA_FRAC_prior=1.3,K_LATOSA_FRAC_vmin_max = [],pft = 6):

    str3 = 'def latosa(K_LATOSA_MIN, K_LATOSA_FRAC): return dict(K_LATOSA_MAX = K_LATOSA_MIN * K_LATOSA_FRAC)'
    str4 = 'p = paramdef.add("K_LATOSA_FRAC", pft="y", units="1", func=latosa)'
    str5 = 'p.set(vdef = {}, fmin = 1, fmax = 3, pft={})'.format(K_LATOSA_FRAC_prior, pft)

    # if there are max and min value
    if len(K_LATOSA_FRAC_vmin_max) ==2:
        str5 = 'p.set(vdef = {}, vmin = {}, vmax = {}, pft={})'.format(K_LATOSA_FRAC_prior,K_LATOSA_FRAC_vmin_max[0],K_LATOSA_FRAC_vmin_max[1], pft)
    return [str3,str4,str5]

# print(make_param(),make_K_LATOSA())

parameter_df = pd.read_csv('./DBF_parameters.csv')

site_list = list(set(parameter_df['site'].tolist()))


for site in site_list:
    
    parameter_list_all =[]
    site_df = parameter_df[parameter_df['site']==site]
    forest_type = site_df['type'].tolist()[0]
    pft = site_df['PFT'].tolist()[0]
    
    parameter_list = site_df["PARAMETER"]
    
    for parameter_ in parameter_list:
        site_parameter_df = site_df[site_df['PARAMETER']==parameter_]
        
        parameter_NAME = parameter_.split('__')[0]
        parameter_value = site_parameter_df['POST'].tolist()[0]
        
        parameter_range = []
        
        if parameter_NAME in ['Wlim']:
            parameter_range = [parameter_value*0.25,0.95]
            
        if parameter_NAME in ['STRESS_GS',"STRESS_GM",'LAI_MAX_TO_HAPPY']:
            parameter_range = [parameter_value*0.25,1]
        
        if parameter_NAME in ['SLA']:
            if pft == 6:
                parameter_range = [0.013, 0.05]
            elif pft == 4:
                parameter_range = [0.004, 0.03]
            else:
                parameter_range = [0.004, 0.05]
        
        if parameter_NAME in ['LAI_MAX']:
            if pft == 6:
                parameter_range = [5.2, 6.8]
            elif pft == 4:
                parameter_range = [3, 8]
            else:
                parameter_range = [1.5, 10]
                
        ## write parameters
        
        if parameter_NAME == "K_LATOSA_MIN":
            parameter_list_all.append(make_K_LATOSA_MIN(
                K_LATOSA_prior = parameter_value,
                K_LATOSA_vmin_max = parameter_range,
                pft = pft))
        elif parameter_NAME == "K_LATOSA_FRAC":
            parameter_list_all.append(make_K_LATOSA_FRAC(
                K_LATOSA_FRAC_prior = parameter_value,
                K_LATOSA_FRAC_vmin_max = parameter_range,
                pft = pft))
        else:
            parameter_list_all.append(make_param(
                Name = parameter_NAME,
                pft_dependent = 'y',
                prior = parameter_value,
                vmin_max = parameter_range,
                pft = pft))
    
    current_directory = os.getcwd()

    if 'orchidee02' not in os.getcwd():
        parameter_file = '../Trash/' + forest_type + '_' + site + '.py'
    else:
        parameter_file = '/home/orchidee02/quanpan/phd/orchidas/src/parameters/' + forest_type + '_' + site + '.py'

    if not os.path.exists(parameter_file):
        copy_file('./example.py',parameter_file)

    with open(parameter_file, "a") as file:
        # 逐行写入列表内容
        for para_line in parameter_list_all:
            for line in para_line:
                file.write(line)
                file.write('\n')
            file.write('\n')

    # 关闭文件
    file.close()
                
