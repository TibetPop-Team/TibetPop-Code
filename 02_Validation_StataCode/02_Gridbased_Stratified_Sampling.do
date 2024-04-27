/*******************************************************************************
Program: 02_Gridbased_Stratified_Sampling.do
Author: Yicong Tian
Compiled: August 5, 2023
Purpose:
(a) Comparisons of grid-based samples and administrative unit-based samples for 
149 counties in the QTP. The maximum population per pixel in each county is 
significantly higher than the average population density, indicating that the 
grid-based samples exhibit higher variance and better discrimination ability 
for modelling the population distribution. The minimum population per pixel in 
each county is zero; 
(b) An example of stratified sampling intervals in urban areas, R01. 
R01 comprises nine sampling intervals, such as [0, 1525) and [1525, 4813); 
(c) The same as (b), but with a rural example, R05.
*******************************************************************************/

**Subplot (a)
{
use "D:\data\Samples_County.dta", replace

gsort -ths_max, gen(id) m // ths represents THS-POP
gen lgths_max = log10(ths_max)
gen lgcensus_d = log10(census_density)

graph tw connect lgths_max id, ///
lwidth(medium) lcolor(navy) msym(D) mcolor(navy) msize(small) ///
ytitle(Log population density, margin(medsmall) size(huge)) ///
yscale(lpattern(blank)) ///
ylabel(-1(1)5, labsize(huge) angle(horizontal) tlength(tiny) ///
tlwidth(vthin) tposition(outside)) ///
xtitle(Counties, size(huge) height(1)) ///
xlabel(1(148)149, labsize(huge) tposition(inside)) xmtick(, labels) ///
|| connect lgcensus_d id, ///
   lpattern(solid) lwidth(medium) lcolor(green*1.5) ///
   msym(+) mcolor(green*1.5) msize(large) ///
legend(pos(2) ring(0) cols(1) symx(10pt) size(23pt) ///
lab(1 "Maximum population per pixel ") ///
lab(2 "Average population density") order(1 2)) ///
xsize(7) ysize(2) graphregion(margin(vlarge) ///
lpattern(blank) ilpattern(blank)) plotregion(margin(medium)) ///
text(5.6 -8.5 "{bf:a}", size(vhuge))

graph save Graph D:\graph\Samples_County.gph, replace
graph export "D:\graph\Samples_County.png", as (png) replace
}

**Subplot (b) 
*si represents "sampling interval"
*sz represents "sampling size"
{
use "D:\data\Samples_R01.dta", replace
gen lgsz = log10(sz)

twoway (connected lgsz si, msymbol(none) lpattern(solid) lwidth(thick)) ///
, ytitle(Log sampling size, size(huge) margin(medsmall)) ///
yscale(lpattern(blank)) ///
ylabel(0(1)3, labsize(huge) angle(horizontal) tlength(tiny) tlwidth(vthin) ///
tposition(outside)) ///
xtitle(Population per pixel in R01, size(huge) height(17)) ///
||, xline(1525.12, lwidth(vthin) lpattern(shortdash) extend) ///
xline(4812.6, lwidth(vthin) lpattern(shortdash) extend) ///
xline(8100.08, lwidth(vthin) lpattern(shortdash) extend) ///
xline(11387.56, lwidth(vthin) lpattern(shortdash) extend) ///
xline(14675.04, lwidth(vthin) lpattern(shortdash) extend) ///
xline(17962.52, lwidth(vthin) lpattern(shortdash) extend) ///
xline(21250, lwidth(vthin) lpattern(shortdash) extend) ///
xline(24537.48, lwidth(vthin) lpattern(shortdash) extend) ///
xlabel(none, noticks) xmtick(, labels) ///
text(-0.171 1525.12 "1525", size(huge)) ///
text(-0.171 4812.6 "4813", size(huge)) ///
text(-0.171 8100.08 "8100", size(huge)) ///
text(-0.171 11387.56 "11388", size(huge)) ///
text(-0.171 14675.04 "14675", size(huge)) ///
text(-0.171 17962.52 "17963", size(huge)) ///
text(-0.171 21250 "21250", size(huge)) ///
text(-0.171 24537.48 "24537", size(huge)) ///
text(-0.171 27824.96 "27825", size(huge)) ///
xsize(7) ysize(2) graphregion(margin(vlarge) ///
lpattern(blank) ilpattern(blank)) plotregion(margin(zero)) ///
text(3.2 -1230 "{bf:b}", size(vhuge)) ///
text(0.7 3200 "AVE+1×STD", size(vlarge)) ///
title(Stratified sampling intervals, ///
size(huge) ring(0) place(2) margin(medsmall)) ///
|| (area lgsz si, fcolor(gs15%50)), legend(off)

graph save Graph D:\graph\Samples_R01.gph, replace
graph export "D:\graph\Samples_R01.png", as (png) replace
}

**Subplot (c) 
*si represents "sampling interval"
*sz represents "sampling size"
{
use "D:\data\Samples_R05.dta", replace
gen lgsz = log10(sz)

twoway (connected lgsz si, msymbol(none) lpattern(solid) lwidth(thick)) ///
, ytitle(Log sampling size, size(huge) margin(medsmall)) ///
yscale(lpattern(blank)) ///
ylabel(0(1)4, labsize(huge) angle(horizontal) tlength(tiny) tlwidth(vthin) ///
tposition(outside)) ///
xtitle(Population per pixel in R05, size(huge) height(17)) ///
xline(14.22, lwidth(vthin) lpattern(shortdash) extend) ///
xline(113.44, lwidth(vthin) lpattern(shortdash) extend) ///
xline(212.66, lwidth(vthin) lpattern(shortdash) extend) ///
xline(311.88, lwidth(vthin) lpattern(shortdash) extend) ///
xline(411.1, lwidth(vthin) lpattern(shortdash) extend) ///
xline(510.32, lwidth(vthin) lpattern(shortdash) extend) ///
xline(609.54, lwidth(vthin) lpattern(shortdash) extend) ///
xline(708.76, lwidth(vthin) lpattern(shortdash) extend) ///
xline(807.98, lwidth(vthin) lpattern(shortdash) extend) ///
xline(907.2, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1006.42, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1105.64, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1204.86, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1304.08, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1403.3, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1502.52, lwidth(vthin) lpattern(shortdash) extend) ///
xline(1601.74, lwidth(vthin) lpattern(shortdash) extend) ///
xlabel(none, noticks) xmtick(, labels) ///
text(-0.23 14.22 "14", size(huge)) ///
text(-0.23 113.44 "113", size(huge)) ///
text(-0.23 212.66 "213", size(huge)) ///
text(-0.23 311.88 "312", size(huge)) ///
text(-0.23 411.1 "411", size(huge)) ///
text(-0.23 510.32 "510", size(huge)) ///
text(-0.23 609.54 "610", size(huge)) ///
text(-0.23 708.76 "709", size(huge)) ///
text(-0.23 807.98 "808", size(huge)) ///
text(-0.23 907.2 "907", size(huge)) ///
text(-0.23 1006.42 "1006", size(huge)) ///
text(-0.23 1105.64 "1106", size(huge)) ///
text(-0.23 1204.86 "1205", size(huge)) ///
text(-0.23 1304.08 "1304", size(huge)) ///
text(-0.23 1403.3 "1403", size(huge)) ///
text(-0.23 1502.52 "1503", size(huge)) ///
text(-0.23 1601.74 "1602", size(huge)) ///
xsize(7) ysize(2) graphregion(margin(vlarge) ///
lpattern(blank) ilpattern(blank)) plotregion(margin(zero)) ///
text(4.2 -70 "{bf:c}", size(vhuge)) ///
text(1.1 65 "AVE+" "1×STD", size(vlarge)) ///
title(Stratified sampling intervals, ///
size(huge) ring(0) place(2) margin(medsmall)) ///
|| (area lgsz si, fcolor(gs15%50)), legend(off)

graph save Graph D:\graph\Samples_R05.gph, replace
graph export "D:\graph\Samples_R05.png", as (png) replace
}

**Visualization
graph combine ///
    D:\graph\Samples_County.gph ///
	D:\graph\Samples_R01.gph ///
	D:\graph\Samples_R05.gph ///
	, col(1) xsize(7) ysize(6) altshrink ///
	graphregion(color(white)) imargin(medium)
	
graph save Graph D:\graph\Gridbased_Stratified_Sampling.gph, replace
graph export "D:\graph\Gridbased_Stratified_Sampling.png", as (png) replace