import xml.etree.ElementTree as ET
import os
import re

def read_txt_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def read_txt_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines

def append_line(filename, line):
    with open(filename, 'a') as file:
        file.write(line + '\n')

def copy_file(source, destination):
    with open(source, 'rb') as f_source:
        with open(destination, 'wb') as f_destination:
            # Read and write the file in chunks to conserve memory
            for chunk in iter(lambda: f_source.read(4096), b''):
                f_destination.write(chunk)
          
                
def create_task(run_type='optimize',methods = "L-BFGS-B",nodes = 1,ppn = 5,output_level = 0,
                site_id="FR_Fon2006",year = "", year_end="",pft=6, 
                traits = "VCMAX25, A1, B1",iter = 10, nspin="5y",
                run_path ='./',
                orchidas_src = '/home/orchidee02/quanpan/phd/orchidas/src/',
                parameter_def='config/parameters/paramdef.py', 
                driver_path='/home/orchidee02/quanpan/phd/drivers/ncdriver/yearly'):
    
    task_dir = run_path + site_id + '_' + run_type[0:2] + '_'+year+'_'+ year_end +'/'
    
    if not os.path.exists(task_dir):
        os.mkdir(task_dir)
    
        copy_file('./job_template.sh',task_dir+'./job.sh')
        
        with open(task_dir+'./job.sh', 'r+') as file:
            lines = file.readlines()
            
            lines.insert(1, '#PBS -N ' + site_id + '_' + run_type[0:2]  + '\n')
            lines.insert(2, '#PBS -l ' + 'nodes=' + str(nodes) + ':ppn=' + str(ppn)  + '\n')

            file.seek(0)
            
            file.writelines(lines)

        if year_end == "":
            year_end = year
        root = ET.Element("xml")

        # Task
        task = ET.SubElement(root, "task")
        task.set("id", run_type)
        task.set("path_output", task_dir + "Output")
        task.set("norc", str(nodes*ppn))
        task.set("param_opt", traits)
        task.set("loglevel", '2')
        task.set("save_history", 'y')
        
        if run_type == 'optimize':
            task.set("minimizer", methods)
            task.set("maxiter", str(iter))
            task.set("nspin", nspin)
            
        else:
            print('set as sensitivity analysis')
            task.set("analyzer", methods)
            
            # set analyzer
            analyzer = ET.SubElement(root, "analyzer")
            analyzer.set("id", methods)
            analyzer.set("n_levels", "10")
            analyzer.set("n_trajectories", "10")
            
        # Site
        site = ET.SubElement(root, "site")
        site.set("id", site_id)
        site.set("type", "flux")
        site.set("pft", str(pft))
        if run_type == 'optimize':
            site.set("obs_path", driver_path+ site_id+"_"+ year +"-"+ year_end+ ".nc")
            site.set("obs_name", "GPP")
            site.set("obs_coef", "48, 1")
            site.set("obs_filter", "flatten/mean/smooth") # 
        site.set("sim_name", "gppt")
        site.set("sim_filter", "flatten/smooth") # 
        site.set("forcing_path", driver_path+ site_id+"_"+ year +"-"+ year_end+ ".nc")
        site.set("path_inirundef", orchidas_src+"config/pft"+ str(pft) + "_run.def")

        # Orchidee
        orchidee = ET.SubElement(root, "orchidee")
        orchidee.set("path_orchidee", "/home/orchidee02/quanpan/phd/modipsl/bin/orchidee_ol_prod")
        orchidee.set("path_rundef", "/home/orchidee02/quanpan/phd/modipsl/config/ORCHIDEE_OL/OOL_SEC_STO_FG2/PARAM/run.def")
        orchidee.set("path_filedef", orchidas_src+"config/orc3_file.def")
        orchidee.set("path_vardef", orchidas_src+"config/vardef.py")
        orchidee.set("path_paramdef", parameter_def)
        orchidee.set("sechiba_step", "1d")
        if output_level > 0:
            orchidee.set("sechiba_level", "11")
            orchidee.set("stomate_level", "6")
            orchidee.set("stomate_ipcc_level", "1")
        else:
            orchidee.set("sechiba_level", "0")


        tree = ET.ElementTree(root)
        
        tree.write(task_dir+"task.xml", encoding="utf-8", xml_declaration=True)
        
        append_line(task_dir+'job.sh', 'python /home/orchidee02/quanpan/phd/orchidas/src/orchidas.py ' + task_dir +"task.xml")


if __name__ == '__main__':
        
    if not os.path.exists('../run.sh'):
        copy_file('./run.sh','../run.sh')

    orchidas_src = '/home/orchidee02/quanpan/phd/orchidas/src/'
    
    traits_file = 'traits.txt'
    site_info_file = 'siteinfo.txt'

    file_lines = read_txt_to_list(site_info_file)
    traits = read_txt_file(traits_file)  
    for line in file_lines:
        site_text = line.split("\t")
        print(site_text)
        # ['BE-Bra1996', '1996', '1996', '51.30761', '4.51984', '1', '0.5','6']
        create_task(
            run_type='optimize',
            methods = "L-BFGS-B", # L-BFGS-B  GA
            nodes = 1,
            ppn = 5,
            output_level = 0,
            site_id=site_text[0],
            year = site_text[1], 
            year_end=site_text[2],
            pft='6', 
            traits = traits,iter = 15, nspin="2x",
            orchidas_src = orchidas_src,
            run_path ='/home/orchidee02/quanpan/phd/orchidas/Timeseries_research/prior/DBF/',
            # parameter_def='/home/orchidee02/quanpan/phd/orchidas/config/parameters/paramdef.py', 
            parameter_def='/home/orchidee02/quanpan/phd/orchidas/src/parameters/' + 'DBF' + '_' + re.sub(r'\d+$', '', site_text[0]) + '.py',

            driver_path='/home/orchidee02/quanpan/phd/drivers/ncdriver/yearly/')