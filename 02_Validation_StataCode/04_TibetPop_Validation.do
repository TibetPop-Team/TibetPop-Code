/*******************************************************************************
Program: 04_TibetPop_Validation.do
Author: Yicong Tian
Compiled: January 22, 2024
Purpose: 
* This code aims to assess the data quality of TibetPop. The evaluation method 
involves aggregating TibetPop data, with a resolution of 1km, to the township 
level, which is the fourth administrative level, and comparing it with census 
population data at this level. Evaluation metrics such as adjusted R-squared, 
MAE, and RMSE are calculated for this purpose.
* Using the aforementioned method, the code also assesses the quality of 
population grid data from other sources, including WorldPop, LandScan, and 
ChinaPop. By comparing the evaluation metrics of TibetPop with these datasets, 
it reflects the advantages of TibetPop's optimized random forest population 
disaggregation algorithm.
*******************************************************************************/

use "D:\data\TibetPop_Validation.dta", replace

label define proid ///
1 "Gansu" 2 "Qinghai" 3 "Sichuan" 4 "Tibet" 5 "Xinjiang" 6 "Yunnan" // provinces

**Adj R-squared
*TibetPop Group1's Adj R-squared
{
reg census_c2020 group1_c2020
*0.9657
reg census_d2020 group1_d2020
*0.9616
reg census_c2020 group1_c2020 if proid == 2
*0.9740
reg census_d2020 group1_d2020 if proid == 2
*0.9413
reg census_c2020 group1_c2020 if proid == 4
*0.8849
reg census_d2020 group1_d2020 if proid == 4
*0.9901
reg census_c2020 group1_c2020 if proid == 3
*0.7591
reg census_d2020 group1_d2020 if proid == 3
*0.8129
reg census_c2020 group1_c2020 if proid == 1
*0.9111
reg census_d2020 group1_d2020 if proid == 1
*0.9889
reg census_c2020 group1_c2020 if proid == 6
*0.9361
reg census_d2020 group1_d2020 if proid == 6
*0.9351
}

*TibetPop Group2's Adj R-squared
{
reg census_c2020 group2_c2020
*0.9638
reg census_d2020 group2_d2020
*0.9631
reg census_c2020 group2_c2020 if proid == 2
*0.9727
reg census_d2020 group2_d2020 if proid == 2
*0.9457
reg census_c2020 group2_c2020 if proid == 4
*0.8798
reg census_d2020 group2_d2020 if proid == 4
*0.9897
reg census_c2020 group2_c2020 if proid == 3
*0.7581
reg census_d2020 group2_d2020 if proid == 3
*0.8033
reg census_c2020 group2_c2020 if proid == 1
*0.8984
reg census_d2020 group2_d2020 if proid == 1
*0.9892
reg census_c2020 group2_c2020 if proid == 6
*0.9369
reg census_d2020 group2_d2020 if proid == 6
*0.9361
}

*WorldPop's Adj R-squared
{
reg census_c2020 worldpop_c2020
*0.9329
reg census_d2020 worldpop_d2020
*0.8656
reg census_c2020 worldpop_c2020 if proid == 2
*0.9499
reg census_d2020 worldpop_d2020 if proid == 2
*0.8204
reg census_c2020 worldpop_c2020 if proid == 4
*0.7729
reg census_d2020 worldpop_d2020 if proid == 4
*0.9703
reg census_c2020 worldpop_c2020 if proid == 3
*0.7140
reg census_d2020 worldpop_d2020 if proid == 3
*0.7588
reg census_c2020 worldpop_c2020 if proid == 1
*0.6086
reg census_d2020 worldpop_d2020 if proid == 1
*0.8793
reg census_c2020 worldpop_c2020 if proid == 6
*0.7415
reg census_d2020 worldpop_d2020 if proid == 6
*0.7219
}

*LandScan's Adj R-squared
{
reg census_c2020 landscan_c2020
*0.9171
reg census_d2020 landscan_d2020
*0.9377
reg census_c2020 landscan_c2020 if proid == 2
*0.9519
reg census_d2020 landscan_d2020 if proid == 2
*0.9225
reg census_c2020 landscan_c2020 if proid == 4
*0.6253
reg census_d2020 landscan_d2020 if proid == 4
*0.9734
reg census_c2020 landscan_c2020 if proid == 3
*0.3506
reg census_d2020 landscan_d2020 if proid == 3
*0.3352
reg census_c2020 landscan_c2020 if proid == 1
*0.5398
reg census_d2020 landscan_d2020 if proid == 1
*0.6711
reg census_c2020 landscan_c2020 if proid == 6
*0.5123
reg census_d2020 landscan_d2020 if proid == 6
*0.4990
}

*ChinaPop's Adj R-squared 
{
reg census_c2020 chinapop_c2020
*0.7762
reg census_d2020 chinapop_d2020
*0.7182
reg census_c2020 chinapop_c2020 if proid == 2
*0.8495
reg census_d2020 chinapop_d2020 if proid == 2
*0.7959
reg census_c2020 chinapop_c2020 if proid == 4
*0.2955
reg census_d2020 chinapop_d2020 if proid == 4
*0.9081
reg census_c2020 chinapop_c2020 if proid == 3
*0.0597
reg census_d2020 chinapop_d2020 if proid == 3
*0.0538
reg census_c2020 chinapop_c2020 if proid == 1
*-0.0135
reg census_d2020 chinapop_d2020 if proid == 1
*0.1904
reg census_c2020 chinapop_c2020 if proid == 6
*0.0467
reg census_d2020 chinapop_d2020 if proid == 6
*0.2561
}

**MAE
*TibetPop Group1's MAE
{
reg census_c2020 group1_c2020
predict yhat, xb 
*Save the fitted values of the model as variable yhat, same for the following
gen mae = abs(census_c2020 - yhat) 
*Calculate and create variable mae, same for the following
sum mae 
*The mean of mae serves as the result, 
*i.e., the value in the "mean" column in the results, same for the following
drop yhat mae
*2243.843

reg census_d2020 group1_d2020
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*15.24801

reg census_c2020 group1_c2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2575.05

reg census_d2020 group1_d2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*17.33383

*proid == 4
reg census_c2020 group1_c2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*2099.353

reg census_d2020 group1_d2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*15.41214

*proid == 3
reg census_c2020 group1_c2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2102.974

reg census_d2020 group1_d2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*14.17126

*proid == 1
reg census_c2020 group1_c2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*2223.719

reg census_d2020 group1_d2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_d2020 - yhat)
sum mae 
drop yhat mae
*16.12563

*proid == 6
reg census_c2020 group1_c2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*3196.004

reg census_d2020 group1_d2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*15.49341
}

*TibetPop Group2's MAE
{
reg census_c2020 group2_c2020
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2338.027

reg census_d2020 group2_d2020
predict yhat, xb 
gen mae = abs(census_d2020 - yhat)
sum mae 
drop yhat mae
*15.53127

*proid == 2
reg census_c2020 group2_c2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*2737.789

reg census_d2020 group2_d2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*16.98203

*proid == 4
reg census_c2020 group2_c2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2154.49

reg census_d2020 group2_d2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*15.91666

*proid == 3
reg census_c2020 group2_c2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2149.188

reg census_d2020 group2_d2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*14.1533

*proid == 1
reg census_c2020 group2_c2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2331.697

reg census_d2020 group2_d2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*17.6206

*proid == 6
reg census_c2020 group2_c2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*3285.542

reg census_d2020 group2_d2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*15.95772
}

*WorldPop's MAE
{
reg census_c2020 worldpop_c2020
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2605.488

reg census_d2020 worldpop_d2020
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae
drop yhat mae
*26.90942

*proid == 2
reg census_c2020 worldpop_c2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*2746.605

reg census_d2020 worldpop_d2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*46.98446

*proid == 4
reg census_c2020 worldpop_c2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2929.07

reg census_d2020 worldpop_d2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*26.18669

*proid == 3
reg census_c2020 worldpop_c2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae
drop yhat mae
*2584.219

reg census_d2020 worldpop_d2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*25.57958

*proid == 1
reg census_c2020 worldpop_c2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*3741.778

reg census_d2020 worldpop_d2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_d2020 - yhat)
sum mae 
drop yhat mae
*55.95009

*proid == 6
reg census_c2020 worldpop_c2020 if proid == 6
predict yhat, xb
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*2794.564

reg census_d2020 worldpop_d2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*24.57171
}

*LandScan's MAE 
{
reg census_c2020 landscan_c2020
predict yhat, xb
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*3643.52

reg census_d2020 landscan_d2020
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*24.18643

*proid == 2
reg census_c2020 landscan_c2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*3675.593

reg census_d2020 landscan_d2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*28.40627

*proid == 4
reg census_c2020 landscan_c2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*3652.733

reg census_d2020 landscan_d2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_d2020 - yhat)
sum mae 
drop yhat mae
*26.20191

*proid == 3
reg census_c2020 landscan_c2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*3656.578

reg census_d2020 landscan_d2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_d2020 - yhat)
sum mae
drop yhat mae
*26.46258

*proid == 1
reg census_c2020 landscan_c2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*3533.047

reg census_d2020 landscan_d2020 if proid == 1
predict yhat, xb
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*39.95534

*proid == 6
reg census_c2020 landscan_c2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_c2020 - yhat)
sum mae 
drop yhat mae
*4766.87

reg census_d2020 landscan_d2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*30.62463
}

*ChinaPop's MAE 
{
reg census_c2020 chinapop_c2020
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*5149.387

reg census_d2020 chinapop_d2020
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*42.63043

*proid == 2
reg census_c2020 chinapop_c2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*5367.257

reg census_d2020 chinapop_d2020 if proid == 2
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*54.10742

*proid == 4
reg census_c2020 chinapop_c2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*4878.835

reg census_d2020 chinapop_d2020 if proid == 4
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae
drop yhat mae
*73.38987

*proid == 3
reg census_c2020 chinapop_c2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*4586.136

reg census_d2020 chinapop_d2020 if proid == 3
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*41.12768

*proid == 1
reg census_c2020 chinapop_c2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae 
drop yhat mae
*6447.48

reg census_d2020 chinapop_d2020 if proid == 1
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*96.74069

*proid == 6
reg census_c2020 chinapop_c2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_c2020 - yhat) 
sum mae
drop yhat mae
*6230.64

reg census_d2020 chinapop_d2020 if proid == 6
predict yhat, xb 
gen mae = abs(census_d2020 - yhat) 
sum mae 
drop yhat mae
*41.09563
}

**RMSE
*TibetPop Group1's RMSE
{
reg census_c2020 group1_c2020
predict yhat, xb  
// Save the fitted values of the model as variable yhat, same for the following
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
// Calculate and create variable mse, same for the following
sum mse  
// The "mean" column in the results represents MSE, same for the following
scalar mean_mse = r(mean)  
// Extract the mean of MSE, same for the following
dis sqrt(mean_mse)  
// Calculate the square root to obtain RMSE, same for the following
drop yhat mse
*4676.6052

reg census_d2020 group1_d2020
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*85.943856

*proid == 2
reg census_c2020 group1_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat) 
sum mse 
scalar mean_mse = r(mean)  
dis sqrt(mean_mse) 
drop yhat mse
*4752.979

reg census_d2020 group1_d2020 if proid == 2
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*87.273375

*proid == 4
reg census_c2020 group1_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*5030.3404

reg census_d2020 group1_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*88.938778

*proid == 3
reg census_c2020 group1_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse) 
drop yhat mse
*6578.5174

reg census_d2020 group1_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*87.937358

*proid == 1
reg census_c2020 group1_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*4684.3888

reg census_d2020 group1_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat) 
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse) 
drop yhat mse
*86.524133

*proid == 6
reg census_c2020 group1_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*5607.7398

reg census_d2020 group1_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*86.972451
}

*TibetPop Group2's RMSE
{
reg census_c2020 group2_c2020
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat) 
sum mse 
scalar mean_mse = r(mean) 
dis sqrt(mean_mse)  
drop yhat mse
*4803.5204

reg census_d2020 group2_d2020
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*84.200588

*proid == 2
reg census_c2020 group2_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*4899.4044

reg census_d2020 group2_d2020 if proid == 2
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*86.001546

*proid == 4
reg census_c2020 group2_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*5265.358

reg census_d2020 group2_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*88.462675

*proid == 3
reg census_c2020 group2_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*6940.9272

reg census_d2020 group2_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*87.39101

*proid == 1
reg census_c2020 group2_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*4803.9947

reg census_d2020 group2_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*89.100268

*proid == 6
reg census_c2020 group2_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*5620.201

reg census_d2020 group2_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*86.032618
}

*Worldpop's RMSE
{
reg census_c2020 worldpop_c2020
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*6536.6916

reg census_d2020 worldpop_d2020
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*160.78268

*proid == 2
reg census_c2020 worldpop_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*6549.2473

reg census_d2020 worldpop_d2020 if proid == 2
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*167.72583

*proid == 4
reg census_c2020 worldpop_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*8360.3895

reg census_d2020 worldpop_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*182.84482

*proid == 3
reg census_c2020 worldpop_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*7623.9383

reg census_d2020 worldpop_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*194.26716

*proid == 1
reg census_c2020 worldpop_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*13936.128

reg census_d2020 worldpop_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*366.8778

*proid == 6
reg census_c2020 worldpop_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*8214.0278

reg census_d2020 worldpop_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*182.69501
}

*LandScan's RMSE
{
reg census_c2020 landscan_c2020
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*7267.1186

reg census_d2020 landscan_d2020
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*109.49026

*proid == 2
reg census_c2020 landscan_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*7278.0029

reg census_d2020 landscan_d2020 if proid == 2
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*109.86635

*proid == 4
reg census_c2020 landscan_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*7286.2841

reg census_d2020 landscan_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*111.39377

*proid == 3
reg census_c2020 landscan_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*13526.523

reg census_d2020 landscan_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*145.99653

*proid == 1
reg census_c2020 landscan_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*9644.0076

reg census_d2020 landscan_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*192.44857

*proid == 6
reg census_c2020 landscan_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*15534.466

reg census_d2020 landscan_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*196.45177
}

*ChinaPop's RMSE
{
reg census_c2020 chinapop_c2020
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*11939.147

reg census_d2020 chinapop_d2020
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*232.76757

*proid == 2
reg census_c2020 chinapop_c2020 if proid == 2
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*12024.075

reg census_d2020 chinapop_d2020 if proid == 2
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*239.80709

*proid == 4
reg census_c2020 chinapop_c2020 if proid == 4
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*13605.852

reg census_d2020 chinapop_d2020 if proid == 4
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*473.55014

*proid == 3
reg census_c2020 chinapop_c2020 if proid == 3
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*19803.835

reg census_d2020 chinapop_d2020 if proid == 3
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*289.84687

*proid == 1
reg census_c2020 chinapop_c2020 if proid == 1
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*25397.805

reg census_d2020 chinapop_d2020 if proid == 1
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*628.76307

*proid == 6
reg census_c2020 chinapop_c2020 if proid == 6
predict yhat, xb  
gen mse = (census_c2020-yhat)*(census_c2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*18942.947

reg census_d2020 chinapop_d2020 if proid == 6
predict yhat, xb  
gen mse = (census_d2020-yhat)*(census_d2020-yhat)  
sum mse  
scalar mean_mse = r(mean)  
dis sqrt(mean_mse)  
drop yhat mse
*305.17045
}