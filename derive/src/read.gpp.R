
#* Sensitivity analysis is used to to test the impact of a given parameter on a given output. 
#* This is an important first step one should do before launching an optimization study. 
#* Sensitivity analysis also helps to:
#*      1) check that the model is doing what we want
#*      2) reduce the number of parameters by removing non-sensitivite parameters (cost of optimization scales with number of parameters)
#*      3) avoid changing non-sensitive parameters since it may result in degrading the fit to fluxes not used in optimization

#* Morris methods
#*     Morris method is good for ranking parameters, selecting parameters to be included in optimization 
#* and eliminating parameters with no sensitivity. It is a good 'express' method which requires few runs. 
#*   
#* Important setting for Morris methods:
#*     1) n_levels — 设置参数采样的数量
#*        number of grid levels (should be even), corresponds to the number of tested values for each parameter within 
#*        its min/max-range, e.g. if a parameter is distributed in [0,1] and n_levels=4, the grid levels will be defined 
#*        as (0, 0.33, 0.66, 1);
#*     2) n_trajectories — 组合数量
#*        number of trajectories to generate, corresponds to the number of randomly selected combinations 
#*        constructered from different parameters and its associated grid levels. The number of iterations to be performed 
#*        by ORCHIDAS is equal to n_trajectories * (n_parameters + 1).

#* Morris Outputs
#* The Morris method provides few output metrics: 
#*      1) µ (the mean of the distribution), 
#*      2) µ* (the mean of the distribution of absolute values) 参数的µ*_norm越高,模型对该参数的变化越敏感
#*      3) σ (the standard deviation of the distribution). σ被用作参数之间相互作用的指标(参数的σ越高,参数对其他参数的依赖性越大)
#*      4) σ/µ: 比的幅度反映变量与其他变量相互作用的强度:
#*          简单的加性效应(不具有相互作用):σ/µ<0.1 are assumed to have linear effect, 
#*          单独的 0.5<σ/µ<0.1 - monotonous effect, 
#*          几乎是单独的 0.1<σ/µ<0.5 - almost monotonous effect, 
#*          σ/µ>1 - non-linear effect or interactions with other parameters
#*  To remind: in ORCHIDAS we consider distribution of RMSD between model simulations at different parameter values 
#*  and prior model simulations (at default parameter values). 
library(ncdf4)
library(ggplot2)
library(dplyr)


retrive_sensitivity <- function(ncfname = 'output_20240426_170017.nc') {
  
  sensitivity_results <- data.frame()
  ncin <- nc_open(ncfname)
  
  # var_names <- names(ncin$var)
  # print(var_names)
  # [1] "site_id"                 "site_type"               "site_pft"                "site_simname"           
  # [5] "site_obsname"            "site_error"              "param_id"                "param_scale"            
  # [9] "param_type"              "param_prior"             "param_min"               "param_max"              
  # [13] "param_error"             "param_eps"               "J"                       "Jo"                     
  # [17] "Jb"                      "RMSD"                    "data_id"                 "time"                   
  # [21] "data_site0_var0"         "mu_global"               "mu_star_global"          "mu_star_conf_global"    
  # [25] "sigma_global"            "mu_site0_var0"           "mu_star_site0_var0"      "mu_star_conf_site0_var0"
  # [29] "sigma_site0_var0"       
  
  # site_id
  site_id = ncvar_get(ncin,'site_id')
  site_type = ncvar_get(ncin,'site_type')
  site_pft = ncvar_get(ncin,'site_pft')
  site_simname = ncvar_get(ncin,'site_simname')
  
  param_id = ncvar_get(ncin,'param_id')
  mu_star = ncvar_get(ncin,'mu_star_global')
  sigma = ncvar_get(ncin,'sigma_global')
  mu_star_normal = mu_star/max(mu_star)
  
  for (i in c(1:length(param_id))) {
    
    one_sensitivity_result <- data.frame(
      site_id = site_id,
      site_type = site_type,
      site_pft = site_pft,
      site_simname = site_simname,
      param = param_id[i],
      mu_star = mu_star[i],
      sigma = sigma[i],
      mu_star_normal = mu_star_normal[i]
    )
    
    sensitivity_results <- rbind(sensitivity_results,one_sensitivity_result)
  }
  
  return(sensitivity_results)
}

# retrive_sensitivity(ncpath = './Simulations/FR-Fon2005_sa_2005_2005/Output/',ncname = 'output_20240426_170017.nc')


# if(!"ncdf4" %in% rownames(installed.packages())){
#     install.packages("ncdf4")
#     }



run_type = 'DBF'

nc_path = paste0("/home/orchidee02/quanpan/phd/orchidas/Timeseries_research/priori/",run_type,'_1')
# 列举当前文件夹下所有满足 */Output/output*.nc 的文件
file_list <- list.files(nc_path, pattern = "^output.*\\.nc", recursive = TRUE, full.names = TRUE)

ncfname <- "/home/orchidee02/quanpan/phd/orchidas/Timeseries_research/priori/DBF_1/CA-Cbo1995_op_1995_1995/Output/output_20240503_125630.nc"
sensitivity_results <- data.frame()
ncin <- nc_open(ncfname)

# var_names <- names(ncin$var)
# print(var_names)
# [1] "site_id"         "site_type"       "site_pft"        "site_simname"   
# [5] "site_obsname"    "site_error"      "param_id"        "param_scale"    
# [9] "param_type"      "param_prior"     "param_min"       "param_max"      
# [13] "param_error"     "param_eps"       "J"               "Jo"             
# [17] "Jb"              "RMSD"            "data_id"         "time"           
# [21] "data_site0_var0" (模拟结果GPP)    

# site_id ncvar_get(ncin,'data_id')
site_id = ncvar_get(ncin,'site_id')
site_type = ncvar_get(ncin,'site_type')
site_pft = ncvar_get(ncin,'site_pft')
site_simname = ncvar_get(ncin,'site_simname')

param_id = ncvar_get(ncin,'param_id')
mu_star = ncvar_get(ncin,'mu_star_global')
sigma = ncvar_get(ncin,'sigma_global')
mu_star_normal = mu_star/max(mu_star)

for (i in c(1:length(param_id))) {

one_sensitivity_result <- data.frame(
    site_id = site_id,
    site_type = site_type,
    site_pft = site_pft,
    site_simname = site_simname,
    param = param_id[i],
    mu_star = mu_star[i],
    sigma = sigma[i],
    mu_star_normal = mu_star_normal[i]
)

sensitivity_results <- rbind(sensitivity_results,one_sensitivity_result)
}

return(sensitivity_results)


all_sensitivity <- data.frame()

for (ncfile in file_list){
    one_site_sensitvity = retrive_sensitivity(ncfile)
    all_sensitivity <- rbind(all_sensitivity,one_site_sensitvity)
}

write.csv(all_sensitivity,
        paste0('./',run_type,'_sensitivity_summary.csv'),row.names=FALSE)
