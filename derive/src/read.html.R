# 安装和加载必要的包
# install.packages("xml2")
# install.packages("rvest")
library(xml2)
library(rvest)
library(stringr)
library(tidyverse)

# HTML 内容

run_type = 'DBF'
nc_path = paste0("../..")
# 列举当前文件夹下所有满足 */Output/output*.nc 的文件
file_list <- list.files(nc_path, pattern = "table.html", recursive = TRUE, full.names = TRUE)

parameter_results <- data.frame()
parameter_results_full <- data.frame()

for (html_file in file_list){

    html <- read_html(html_file)

    site <- str_extract(html_file, "([A-Za-z]+-[A-Za-z]+)")

    table_data <- html_table(html, fill = TRUE)[[1]]
    colnames(table_data) <- table_data[1,]
    table_data <- table_data[c(2:nrow(table_data)),]
    table_data$type <- run_type
    table_data$site <- site
    table_data$PFT <- ifelse(run_type == 'DBF',6,4)

    parameter_results_full <- rbind(parameter_results_full,table_data)

    parameter_results <- rbind(parameter_results,subset(table_data,FG != ''))

}
# 将 HTML 解析为 XML 对象

# 提取表格数据

# 输出提取到的数据
# print(parameter_results)
parameter_results_range <- parameter_results %>% group_by(PARAMETER,type,sitePFT)  %>% summarize(
        FG = median(POST,na.rm=TRUE),
        MIN = min(POST,na.rm=TRUE),
        MIN = max(POST,na.rm=TRUE)
)

write.csv(parameter_results,
        paste0('./',run_type,'_parameters_all.csv'),row.names=FALSE)
write.csv(parameter_results_range,
        paste0('./',run_type,'_parameters.csv'),row.names=FALSE)
write.csv(parameter_results_full,
        paste0('./',run_type,'_simulation.csv'),row.names=FALSE)
