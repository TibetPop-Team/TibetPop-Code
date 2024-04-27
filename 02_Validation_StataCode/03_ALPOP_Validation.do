/*******************************************************************************
Program: 03_ALPOP_Validation.do
Author: Yicong Tian
Compiled: March 10, 2024
Purpose: 
* This do-file aims to assess the data quality of ALPOP, which refers to the 
conventional administrative unit-based modelling methodology used to generate 
gridded population datasets, specifically AL3-POP and AL4-POP derived from 
modelling at the third and fourth administrative levels, respectively. 
* The purpose is to later compare these results with gridded data outcomes 
like TibetPop, which are based on grid modelling.
* The assessment involves aggregating ALPOP data (including AL3-POP and AL4-POP) 
at the township level, which is the fourth administrative level, and comparing 
it with census population data at this level. Various evaluation metrics such as 
adjusted R-squared, MAE, RMSE, etc., are calculated for this purpose.
*******************************************************************************/

use "D:\data\ALPOP_Validation.dta", replace

label define proid ///
1 "Gansu" 2 "Qinghai" 3 "Sichuan" 4 "Tibet" 5 "Xinjiang" 6 "Yunnan" // provinces

*AL3-POP's Adj R-squared
{
reg census_c2020 al3_c2020
*0.5884
reg census_d2020 al3_d2020
*0.5261
reg census_c2020 al3_c2020 if proid == 2
*0.6441
reg census_d2020 al3_d2020 if proid == 2
*0.6896
reg census_c2020 al3_c2020 if proid == 4
*0.2016
reg census_d2020 al3_d2020 if proid == 4
*0.5024
reg census_c2020 al3_c2020 if proid == 3
*0.0398
reg census_d2020 al3_d2020 if proid == 3
*0.1951
reg census_c2020 al3_c2020 if proid == 1
*-0.0126
reg census_d2020 al3_d2020 if proid == 1
*0.1584
reg census_c2020 al3_c2020 if proid == 6
*0.1118
reg census_d2020 al3_d2020 if proid == 6
*0.4077
}

*AL4-POP's Adj R-squared
{
reg census_c2020 al4_c2020
*0.6141
reg census_d2020 al4_d2020
*0.5562
reg census_c2020 al4_c2020 if proid == 2
*0.6669
reg census_d2020 al4_d2020 if proid == 2
*0.7037
reg census_c2020 al4_c2020 if proid == 4
*0.2340
reg census_d2020 al4_d2020 if proid == 4
*0.5712
reg census_c2020 al4_c2020 if proid == 3
*0.0475
reg census_d2020 al4_d2020 if proid == 3
*0.2452
reg census_c2020 al4_c2020 if proid == 1
*-0.0100
reg census_d2020 al4_d2020 if proid == 1
*0.1982
reg census_c2020 al4_c2020 if proid == 6
*0.1155
reg census_d2020 al4_d2020 if proid == 6
*0.4206
}

*AL3-POP's MAE
{
reg census_c2020 al3_c2020
predict yhat_a3c, xb 
*Save the fitted values of the model as yhat_a3c, same for the following
gen mae_a3c = abs(census_c2020 - yhat_a3c) 
*Calculate and create variable mae, same for the following
sum mae_a3c
*The mean of mae serves as the result, 
*i.e., the value in the "mean" column in the results, same for the following
drop yhat_a3c mae_a3c
*5250.282

reg census_d2020 al3_d2020
predict yhat_a3d, xb
gen mae_a3d = abs(census_d2020 - yhat_a3d)
sum mae_a3d
drop yhat_a3d mae_a3d
*51.77788

reg census_c2020 al3_c2020 if proid == 2
predict yhat_a3c, xb 
gen mae_a3c = abs(census_c2020 - yhat_a3c) 
sum mae_a3c 
drop yhat_a3c mae_a3c
*5773.383

reg census_d2020 al3_d2020 if proid == 2
predict yhat_a3d, xb 
gen mae_a3d = abs(census_d2020 - yhat_a3d) 
sum mae_a3d 
drop yhat_a3d mae_a3d
*65.22344

*proid == 4
reg census_c2020 al3_c2020 if proid == 4
predict yhat_a3c, xb 
gen mae_a3c = abs(census_c2020 - yhat_a3c) 
sum mae_a3c 
drop yhat_a3c mae_a3c
*4606.889

reg census_d2020 al3_d2020 if proid == 4
predict yhat_a3d, xb 
gen mae_a3d = abs(census_d2020 - yhat_a3d) 
sum mae_a3d 
drop yhat_a3d mae_a3d
*84.41849

*proid == 3
reg census_c2020 al3_c2020 if proid == 3
predict yhat_a3c, xb 
gen mae_a3c = abs(census_c2020 - yhat_a3c) 
sum mae_a3c 
drop yhat_a3c mae_a3c
*4515.06

reg census_d2020 al3_d2020 if proid == 3
predict yhat_a3d, xb 
gen mae_a3d = abs(census_d2020 - yhat_a3d) 
sum mae_a3d 
drop yhat_a3d mae_a3d
*86.15022

*proid == 1
reg census_c2020 al3_c2020 if proid == 1
predict yhat_a3c, xb 
gen mae_a3c = abs(census_c2020 - yhat_a3c) 
sum mae_a3c 
drop yhat_a3c mae_a3c
*6268.056

reg census_d2020 al3_d2020 if proid == 1
predict yhat_a3d, xb 
gen mae_a3d = abs(census_d2020 - yhat_a3d) 
sum mae_a3d 
drop yhat_a3d mae_a3d
*163.0652

*proid == 6
reg census_c2020 al3_c2020 if proid == 6
predict yhat_a3c, xb 
gen mae_a3c = abs(census_c2020 - yhat_a3c) 
sum mae_a3c 
drop yhat_a3c mae_a3c
*7699.793

reg census_d2020 al3_d2020 if proid == 6
predict yhat_a3d, xb 
gen mae_a3d = abs(census_d2020 - yhat_a3d) 
sum mae_a3d 
drop yhat_a3d mae_a3d
*44.65148
}

*AL4-POP's MAE
{
reg census_c2020 al4_c2020
predict yhat_a4c, xb
*Save the fitted values of the model as yhat_a4c, same for the following
gen mae_a4c = abs(census_c2020 - yhat_a4c)
*Calculate and create variable mae, same for the following
sum mae_a4c
*The mean of mae serves as the result, 
*i.e., the value in the "mean" column in the results, same for the following
drop yhat_a4c mae_a4c
*5145.499

reg census_d2020 al4_d2020
predict yhat_a4d, xb 
gen mae_a4d = abs(census_d2020 - yhat_a4d) 
sum mae_a4d 
drop yhat_a4d mae_a4d
*49.91774

*proid == 2
reg census_c2020 al4_c2020 if proid == 2
predict yhat_a4c, xb 
gen mae_a4c = abs(census_c2020 - yhat_a4c) 
sum mae_a4c 
drop yhat_a4c mae_a4c
*5735.547

reg census_d2020 al4_d2020 if proid == 2
predict yhat_a4d, xb 
gen mae_a4d = abs(census_d2020 - yhat_a4d) 
sum mae_a4d 
drop yhat_a4d mae_a4d
*62.32093

*proid == 4
reg census_c2020 al4_c2020 if proid == 4
predict yhat_a4c, xb 
gen mae_a4c = abs(census_c2020 - yhat_a4c) 
sum mae_a4c 
drop yhat_a4c mae_a4c
*4508.439

reg census_d2020 al4_d2020 if proid == 4
predict yhat_a4d, xb 
gen mae_a4d = abs(census_d2020 - yhat_a4d) 
sum mae_a4d 
drop yhat_a4d mae_a4d
*81.79694

*proid == 3
reg census_c2020 al4_c2020 if proid == 3
predict yhat_a4c, xb 
gen mae_a4c = abs(census_c2020 - yhat_a4c) 
sum mae_a4c 
drop yhat_a4c mae_a4c
*4440.498

reg census_d2020 al4_d2020 if proid == 3
predict yhat_a4d, xb 
gen mae_a4d = abs(census_d2020 - yhat_a4d) 
sum mae_a4d 
drop yhat_a4d mae_a4d
*89.61485

*proid == 1
reg census_c2020 al4_c2020 if proid == 1
predict yhat_a4c, xb 
gen mae_a4c = abs(census_c2020 - yhat_a4c)
sum mae_a4c 
drop yhat_a4c mae_a4c
*6123.733

reg census_d2020 al4_d2020 if proid == 1
predict yhat_a4d, xb 
gen mae_a4d = abs(census_d2020 - yhat_a4d) 
sum mae_a4d 
drop yhat_a4d mae_a4d
*170.0577

*proid == 6
reg census_c2020 al4_c2020 if proid == 6
predict yhat_a4c, xb 
gen mae_a4c = abs(census_c2020 - yhat_a4c) 
sum mae_a4c 
drop yhat_a4c mae_a4c
*7768.844

reg census_d2020 al4_d2020 if proid == 6
predict yhat_a4d, xb 
gen mae_a4d = abs(census_d2020 - yhat_a4d) 
sum mae_a4d 
drop yhat_a4d mae_a4d
*43.83019
}

*AL3-POP's RMSE
{
reg census_c2020 al3_c2020
predict yhat, xb  
*Save the fitted values of the model as variable yhat, same for the following
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
*Calculate and create variable mse, same for the following
sum mse  
*The "mean" column in the results represents MSE, same for the following
scalar mean_mse = r(mean)  
*Extract the mean of MSE, same for the following
dis sqrt(mean_mse)  
*Calculate the square root to obtain RMSE, same for the following
drop yhat mse
*16190.499

reg census_d2020 al3_d2020
predict yhat, xb 
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*301.87333

*proid == 2
reg census_c2020 al3_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat) 
sum mse 
scalar mean_mse = r(mean) 
dis sqrt(mean_mse) 
drop yhat mse
*16358.749

reg census_d2020 al3_d2020 if proid == 2
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*304.06241

*proid == 4
reg census_c2020 al3_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat) 
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*19531.832

reg census_d2020 al3_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*574.99367

*proid == 3
reg census_c2020 al3_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*20816.536

reg census_d2020 al3_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean) 
dis sqrt(mean_mse)  
drop yhat mse
*590.3168

*proid == 1
reg census_c2020 al3_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*24490.183

reg census_d2020 al3_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*1100.3542

*proid == 6
reg census_c2020 al3_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*19001.58

reg census_d2020 al3_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*314.37927
}

*AL4-POP's RMSE
{
reg census_c2020 al4_c2020
predict yhat, xb  
*Save the fitted values of the model as variable yhat, same for the following
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
*Calculate and create variable mse, same for the following
sum mse  
*The "mean" column in the results represents MSE, same for the following
scalar mean_mse = r(mean)  
*Extract the mean of MSE, same for the following
dis sqrt(mean_mse)  
*Calculate the square root to obtain RMSE, same for the following
drop yhat mse
*15677.265

reg census_d2020 al4_d2020
predict yhat, xb 
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*292.12476

*proid == 2
reg census_c2020 al4_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat) 
sum mse 
scalar mean_mse = r(mean) 
dis sqrt(mean_mse) 
drop yhat mse
*15854.776

reg census_d2020 al4_d2020 if proid == 2
predict yhat, xb 
gen mse = (census_d2020-yhat)*(census_d2020-yhat) 
sum mse  
scalar mean_mse = r(mean) 
dis sqrt(mean_mse) 
drop yhat mse
*294.86734

*proid == 4
reg census_c2020 al4_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat) 
sum mse 
scalar mean_mse = r(mean) 
dis sqrt(mean_mse) 
drop yhat mse
*18816.342

reg census_d2020 al4_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*549.87378

*proid == 3
reg census_c2020 al4_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean) 
dis sqrt(mean_mse)  
drop yhat mse
*20364.355

reg census_d2020 al4_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*617.08134

*proid == 1
reg census_c2020 al4_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean) 
dis sqrt(mean_mse)  
drop yhat mse
*23715.39

reg census_d2020 al4_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*1171.4902

*proid == 6
reg census_c2020 al4_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*18864.656

reg census_d2020 al4_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse) 
drop yhat mse
*307.01525
}