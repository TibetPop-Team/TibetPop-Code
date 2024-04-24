# _*_ coding:utf8 _*_
# python2.7.2
# 程序员：李艳成
# 编制时间：2022年04月20日
# 程序名称：process1.py
# 包含4个子模块。即：addField_Calcul_2()、spacejoin_3()、exportTable_4()
# 程序目的：获得qzgy_jiequ_spacejoin.txt
# 程序注释：刘劲松
# 注释时间：2022年07月06日

# 导入函数库
import arcpy
import sys
import time

# 利用赋值语句，接收批处理文件传进来的控制参数
# param是文件型地理数据库的名称，也是其存储的路径
param = sys.argv[1]
# name是研究区名称的缩写，可以是sjz、hb、xz等等，这个前缀与文件型地理数据库内部的数据集名称的前缀有关。
name = sys.argv[2]

# 将输出环境设为覆盖输出模式
arcpy.env.overwriteOutput = True
# 将当前的工作路径指定为param
arcpy.env.workspace = param
# 将qzgy_xiang_rk数据集的空间参考坐标作为当前环境输出的坐标系统
arcpy.env.outputCoordinateSystem = arcpy.Describe(str(name)+'_xiang_rk').spatialReference

# 计算村面积
def addField_Calcul_2():

    # 在qzgy_xiang_rk数据集中添加AREA字段，并计算村面积值
    # 输入数据集：qzgy_xiang_rk
    # 输出数据集：qzgy_xiang_rk
    
    # 添加AREA字段
    arcpy.AddField_management(str(name) + '_xiang_rk', 'XIANG_AREA', 'DOUBLE')
    arcpy.AddField_management(str(name) + '_jiequ', 'JIEQU_AREA', 'DOUBLE')
    # 为AREA字段赋值
    arcpy.CalculateField_management(str(name) + '_xiang_rk', 'XIANG_AREA', '!shape.geodesicArea@METERS!', 'PYTHON_9.3')
    arcpy.CalculateField_management(str(name) + '_jiequ', 'JIEQU_AREA', '!shape.geodesicArea@METERS!', 'PYTHON_9.3')
    print('面积字段添加并计算完毕!!!'.decode('utf-8'))

# 通过空间连接，使每个街区多边形获得对应的村编码
def spacejoin_3():
    
    # target_features：qzgy_jiequ,
    # join_features：qzgy_xiang_rk
    # 输入数据集：qzgy_jiequ、qzgy_xiang_rk
    # 输出数据集：qzgy_xiang_jiequ_spacejoin，即out_feature_class
    
    # 将qzgy_jiequ与qzgy_xiang_rk进行空间连接，以使每个街区多边形获得对应的村编码
    arcpy.SpatialJoin_analysis(str(name) + '_jiequ', str(name) + '_xiang_rk', str(name) + '_xiang_jiequ_spacejoin', match_option='WITHIN')
    print('获取街区所对应的乡编码!!!'.decode('utf-8'))

# 将qzgy_xiang_jiequ_spacejoin导出为qzgy_xiang_jiequ_spacejoin.txt
def exportTable_4():
    
    # 将qzgy_xiang_jiequ_spacejoin的属性表保存为txt文件
    # 输入数据集：qzgy_xiang_jiequ_spacejoin
    # 输出文件：qzgy_xiang_jiequ_spacejoin.txt
    
    # 以写模式打开文件通道
    txt = open(str(name) + '_xiang_jiequ_spacejoin.txt', 'w')
    # 写入文件头
    txt.write('XZQDM' + ',' + 'JIEQU_AREA' + ',' + 'XIANG_AREA' + ',' + 'XIANG_RK' + '\n')
    # 将qzgy_xiang_jiequ_spacejoin全部读入rows中
    rows = arcpy.SearchCursor(str(name) + '_xiang_jiequ_spacejoin', fields='XIANG_CODE;JIEQU_AREA;XIANG_AREA;pop2020')
    # 将rows全部写入名为qzgy_xiang_jiequ_spacejoin.txt的文本文件中
    for row in rows:
        context = str(row.getValue('XIANG_CODE')) + ',' + str(row.getValue('JIEQU_AREA')) + ',' + str(row.getValue('XIANG_AREA')) + ',' + str(row.getValue('pop2020')) + '\n'
        txt.write(context)
    print('空间连接文件创建完毕!!!'.decode('utf-8'))

# 执行函数
def execute():

    # 记录程序运行的开始时刻
    start_time = time.time()
    addField_Calcul_2()
    spacejoin_3()
    exportTable_4()
    print(time.time() - start_time)
    # 将此模块的运行时长输出到qzgy_process1.txt中
    txt = open(str(name)+'_process1.txt', 'w')
    txt.write('The RunTime of Process1.py is ' + str(time.time() - start_time) + '\n')

# 主调程序
execute()