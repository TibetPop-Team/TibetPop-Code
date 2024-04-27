/*******************************************************************************
Program: 01_THSPOP_Vadilation.do
Author: Yicong Tian
Compiled: July 31, 2023
Purpose:
* This do-file is used to assess the data quality of THS-POP, which is the data 
source of the dependent variable modeled by the TibetPop random forest.
* THS-POP stands for Tibetan Human Settlement population grid, which is derived 
by spatially disaggregating the census population of the 2020 townships, i.e., 
the fourth-level administrative units, into built areas of ESRI land cover using
binary weighting.
* The assessment methodology here involves comparing THS-POP with GHS-POP, which 
is computed using a similar method. Both datasets are aggregated to the county 
level, i.e., the third-level administrative unit, and compared with census 
population data at that level. The R-squared of the regression is calculated.
*******************************************************************************/

graph set window fontface Arial

/******************************************************************
Comparison of the County-Level Population Count in 2020 (c2020/c20)
******************************************************************/
{
use "D:\data\POP1km_to_County.dta", replace

gen lgcen_c20 = log10(census_c2020)
gen lgths_c20 = log10(thspop_c2020)
gen lgghs_c20 = log10(ghspop_c2020)

reg thspop_c2020 census_c2020
*R² = 0.9925
reg ghspop_c2020 census_c2020
*R² = 0.4676

*thspop_c2020
{
graph tw ///
(lfit lgths_c20 lgcen_c20, range(4 6) lpattern(dash) lcolor(gs0) ///
 text(5.8 4.7 "{stSans: R² = 0.9925}", size(vhuge))) /// 
(scatter (lgths_c20 lgcen_c20) if lgths_c20 >= 1 & lgcen_c20 >= 1, ///
 msize(large) msymbol(Oh) mcolor(navy)) ///
, aspectratio(1) scale(1) legend(off) plotregion(lwidth(thin)) ///
xscale(noline) yscale(noline) ///
title("THS-POP", size(vhuge) margin(small)) ///
xlabel(4(1)6, labsize(vhuge)) xtitle("") ///
ylabel(4(1)6, angle(0) labsize(vhuge)) ///
graphregion(color(white)) plotregion(margin(zero)) 

graph save Graph D:\graph\thspop_c2020.gph, replace
graph export "D:\graph\thspop_c2020.png", as (png) replace
}

*ghspop_c2020
{
graph tw ///
(lfit lgghs_c20 lgcen_c20, range(4 6) lpattern(dash) lcolor(gs0) ///
 text(5.8 4.7 "{stSans: R² = 0.4676}", size(vhuge))) /// 
(scatter (lgghs_c20 lgcen_c20) if lgghs_c20 >= 1 & lgcen_c20 >= 1, ///
 msize(large) msymbol(Th) mcolor(navy)) ///
, aspectratio(1) scale(1) legend(off) plotregion(lwidth(thin)) ///
xscale(noline) yscale(noline) ///
title("GHS-POP", size(vhuge) margin(small)) ///
xlabel(4(1)6, labsize(vhuge)) xtitle("") ///
ylabel(4(1)6, angle(0) labsize(vhuge)) ///
graphregion(color(white)) plotregion(margin(zero)) 

graph save Graph D:\graph\ghspop_c2020.gph, replace
graph export "D:\graph\ghspop_c2020.png", as (png) replace
}

graph combine ///
    D:\graph\thspop_c2020.gph ///
	D:\graph\ghspop_c2020.gph ///
	, col(2) xsize(6) ysize(3.5) altshrink ///
	graphregion(color(white)) imargin(small) ///
	l2title("{stSans: Log predicted population count}", size(huge)) ///
	b2title("{stSans: Log census population count}", size(huge))
	
graph save Graph D:\graph\A_count_2020.gph, replace
graph export "D:\graph\A_count_2020.png", as (png) replace
}


/********************************************************************
Comparison of the County-Level Population Density in 2020 (d2020/d20)
********************************************************************/
{
use "D:\data\POP1km_to_County.dta", replace

gen lgcen_d20 = log10(census_d2020)
gen lgths_d20 = log10(thspop_d2020)
gen lgghs_d20 = log10(ghspop_d2020)

reg thspop_d2020 census_d2020
*R² = 0.9898
reg ghspop_d2020 census_d2020
*R² = 0.9011

*thspop_d2020
{
graph tw ///
(lfit lgths_d20 lgcen_d20, range(-0.8 3.8) lpattern(dash) lcolor(gs0) ///
 text(3.5 0.9 "{stSans: R² = 0.9898}", size(vhuge))) /// 
(scatter (lgths_d20 lgcen_d20) if lgths_d20 >= -2 & lgcen_d20 >= -2, ///
 msize(large) msymbol(Oh) mcolor(green*1.5)) ///
, aspectratio(1) scale(1) legend(off) plotregion(lwidth(thin)) ///
xscale(noline) yscale(noline) ///
title("THS-POP", size(vhuge) margin(small)) ///
xlabel(-1(1)4, labsize(vhuge)) xtitle("") ///
ylabel(-1(1)4, angle(0) labsize(vhuge)) ///
graphregion(color(white)) plotregion(margin(zero)) 

graph save Graph D:\graph\thspop_d2020.gph, replace
graph export "D:\graph\thspop_d2020.png", as (png) replace
}

*ghspop_d2020
{
graph tw ///
(lfit lgghs_d20 lgcen_d20, range(-0.8 3.8) lpattern(dash) lcolor(gs0) ///
 text(3.5 0.9 "{stSans: R² = 0.9011}", size(vhuge))) /// 
(scatter (lgghs_d20 lgcen_d20) if lgghs_d20 >= -2 & lgcen_d20 >= -2, ///
 msize(large) msymbol(Th) mcolor(green*1.5)) ///
, aspectratio(1) scale(1) legend(off) plotregion(lwidth(thin)) ///
xscale(noline) yscale(noline) ///
title("GHS-POP", size(vhuge) margin(small)) ///
xlabel(-1(1)4, labsize(vhuge)) xtitle("") ///
ylabel(-1(1)4, angle(0) labsize(vhuge)) ///
graphregion(color(white)) plotregion(margin(zero)) 

graph save Graph D:\graph\ghspop_d2020.gph, replace
graph export "D:\graph\ghspop_d2020.png", as (png) replace
}

graph combine ///
    D:\graph\thspop_d2020.gph ///
	D:\graph\ghspop_d2020.gph ///
	, col(2) xsize(6) ysize(3.5) altshrink ///
	graphregion(color(white)) imargin(small) ///
	l2title("{stSans: Log predicted population density}", size(huge)) ///
	b2title("{stSans: Log census population density}", size(huge))

graph save Graph D:\graph\B_density_2020.gph, replace
graph export "D:\graph\B_density_2020.png", as (png) replace
}

/*******************************
Comparison Results Visualization
*******************************/

graph combine ///
	D:\graph\A_count_2020.gph ///
	D:\graph\B_density_2020.gph ///
	, col(4) xsize(12) ysize(3.5) altshrink ///
	graphregion(color(white)) imargin(medium)

graph save Graph D:\graph\C_count_density.gph, replace
graph export "D:\graph\C_count_density.png", as (png) replace