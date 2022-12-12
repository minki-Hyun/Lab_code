import numpy as np
import pandas as pd
import IO_Analysis_lib as ioa
#=============================================================================================================================================================================
#=============================================================================================================================================================================
# 변수정의

with open("C:\\PythonWorkspace\\Lab_code\\IO Analysis\\path.txt","r",encoding="UTF-8") as txtfile:
    string = txtfile.readlines()

url_base = string[0].strip()
url_excel_io = string[1].strip()
url_excel_sep = string[2].strip()
sh_name_rawio = string[3].strip()
sh_name_totalio = string[4].strip()
sh_name_distribution = string[5].strip()
sh_name_employ = string[6].strip()
part_category = string[7].strip()
part_code_sel = string[8].strip()
part_code_sel_lar = string[9].strip()

url = url_base+"\\"+url_excel_io # IO분석 파일 있는 위치
url1 = url_base+"\\"+url_excel_sep # 부문분류표 파일 있는 위치

#=============================================================================================================================================================================
#=============================================================================================================================================================================
#=============================================================================================================================================================================

# 부문 쪼개기
wd, sep_li, large_z_sizenum, small_z_sizenum, sel_business,sel_business_lar,file_raw  = ioa.func_sep(url1,sh_name_distribution,part_category,part_code_sel,part_code_sel_lar)

# io 엑셀 불러오기
io_mat, io_mat_raw, column_list, row_list = ioa.func_Load_excel(url,sh_name_rawio)

#통합 행렬 만들기
s_mat = ioa.func_integrated_matrix(url,sep_li,large_z_sizenum,small_z_sizenum,sel_business,sel_business_lar)
print("통합행렬\n\n",s_mat,"\n")

# 재통합된 산출표 만들기
z_mat = ioa.func_new_table(s_mat,io_mat)
print("재통합된 산출표\n\n",z_mat,"\n")
print()

# 총 수요 구하기 (=총 투입)
total_demand = ioa.func_total_demand(s_mat,io_mat_raw.loc[:,"최종수요계"],z_mat,large_z_sizenum)
print("총 수요 (= 총 투입)\n\n",total_demand,"\n")
# demand_in_iomat = io_mat_raw.loc[:,"최종수요계"] 이거 한번에 줄인거임

# # 부가가치계수 구하기
added_value = ioa.func_added_value(url,sh_name_totalio,s_mat,z_mat,total_demand)
print("부가가치계수\n",added_value,"\n\n")

# 생산유발계수 구하기
x_hat_mat_inv,prod_coeff, A_mat = ioa.func_prod_coeff(large_z_sizenum,z_mat,total_demand)
print("생산유발계수\n",prod_coeff,"\n\n")

#생산유발효과 구하기
prod_eff = ioa.func_prod_eff(prod_coeff,A_mat)
print("생산유발효과\n",prod_eff,"\n\n")

# 부가가치유발효과
add_eff = ioa.func_added_eff(large_z_sizenum, prod_eff, added_value)
print("부가가치유발효과\n", add_eff, "\n\n")

# 취업유발계수 구하기
employ_coeff = ioa.func_employ_coeff(wd, url, url1, s_mat, total_demand,sh_name_distribution,io_mat_raw,sh_name_employ,file_raw)
print("취업유발계수\n",employ_coeff,"\n\n")

# 취업유발효과 구하기
employ_eff = ioa.func_employ_eff(large_z_sizenum, prod_eff, employ_coeff)
print("취업유발효과\n",employ_eff,"\n\n")

# 수출유발계수 구하기
export_coeff = ioa.func_export(url, s_mat, total_demand,io_mat_raw)
print("수출유발계수\n",export_coeff,"\n\n")

# 수출유발효과 구하기
export_eff = ioa.func_export_eff(export_coeff, large_z_sizenum, prod_eff)
print("수출유발효과\n",export_eff,"\n\n")

# 공급지장유발계수 구하기
sup_disruptor_eff, priceripple_eff = ioa.func_priceripple_eff(x_hat_mat_inv, z_mat, large_z_sizenum,A_mat)
print("공급지장효과\n",sup_disruptor_eff,"\n\n")
print("물가파급효과\n",priceripple_eff,"\n\n")
