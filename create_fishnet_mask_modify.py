# -*- coding: utf-8 -*-
# Purpose：创建研究区掩膜
# Name: creat_mask.py
# Version：Python2.7.3
# Author：李艳成、温佩璋、刘艺
# Date：2021年12月1日
# Revise：刘劲松（待阅）
# Revised date：2021年11月27日
# Description: 根据矢量边界建立fishnet渔网，添加字段后根据位置选择网格，然后进行矢栅转化，生成掩膜。
# Requirements: 需要先根据研究区的大致范围确定所建渔网的行块数


# 导入arcpy和sys（系统文件）模块
import arcpy
import sys

# 重置编码为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# 确定所创建渔网的块数是否符合，创建渔网超过2GB就会报错，所以要把一个大的研究区分为行块数。
def input_r_c(row, col, r, c):
    '''
    对整块渔网的行列数进行分块操作后，判断是否可以整除，以确保各分块渔网的边界是否可以重合且不压盖
    :param row: 经处理后的整块渔网的行数
    :param col: 经处理后的整块渔网的列数
    :param r: 人为划分的行块数
    :param c: 人为划分的列块数
    :return:
    '''	

    # 判断经处理后的整块渔网的行数是否可以整除人为划分的行块数
    if row % r == 0:

        # 判断经处理后的整块渔网的列数是否可以整除人为划分的列块数
        if col % c == 0:

            # 如果行列均可整除则划分的行列块数可以运行
            return '划分的块数合适!'

    # 实例化一个异常，若不满足上述条件就抛出该异常
    ex = Exception('划分的块数不合适!')

    # 如果不可以整除则报错，需要重新确定行列块
    raise ex


# 创建渔网（Creat Fishnet）
def create_fishnet(fishnet1, left1, right1, top1, bottom1):
    '''
    创建渔网
    :param fishnet1: 渔网保存的路径
    :param left1: 分块渔网的左至点
    :param right1: 分块渔网的右至点
    :param top1: 分块渔网的上至点
    :param bottom1: 分块渔网的下至点
    :return:
    '''

    # 渔网的输出要素
    outFeatureClass = fishnet1

    # 设置渔网的原点（Set the origin of the fishnet）
    originCoordinate = str(left1) + ' ' + str(bottom1)

    # 设置方向（Set the orientation）
    yAxisCoordinate = str(left1) + ' ' + str(bottom1 + 10)

    # 所创渔网的宽度和高度，即1000*1000（Enter 1000 for width and height）
    cellSizeWidth = '100'
    cellSizeHeight = '100'

    # 根据所建范围和像元大小自动计算需要建立多少行列号
    numRows = ''	
    numColumns = ''

    # 由 X 坐标和 Y 坐标值设置的渔网的对角。 如果使用模板范围，则会自动设置对角的值。 如果设置了原点、Y 轴、单元格大小以及行数和列数，则此参数将被禁用。
    oppositeCoorner = str(right1) + ' ' + str(top1)

    # 不创建点标注要素类（ Not Create a point label feature class）
    labels = 'NO_LABELS'

    # 范围由原点和对角设置
    templateExtent = ''

    # 定义每个输出单元格将是一个多边形（Each output cell will be a polygon）
    geometryType = 'POLYGON'

    # 创建渔网（）
    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns, oppositeCoorner, labels, templateExtent, geometryType)
    
    # 打印工作进度，即创建渔网成功
    print('success!!!')

# 定义创建渔网的四至点
def boundry_fishnet(fishnet, r, c):
    '''
    确定分块渔网的四至点
    :param fishnet: 存放渔网的文件夹
    :param r: 人为划分的行块数
    :param c: 人为划分的列块数
    :return:
    '''

    # 获取矢量数据的属性信息
    desc = arcpy.Describe(raw_input)

    # 对渔网的四至点进行处理，使其后四位数为0000
    left = int(desc.extent.XMin) / 100000 * 100000
    bottom = int(desc.extent.YMin) / 100000 * 100000
    right = int(desc.extent.XMax) / 100000 * 100000 + 100000
    top = int(desc.extent.YMax) / 100000 * 100000 + 100000

    # 打印每一个渔网的四至点
    print(left,right,top,bottom)

    # 输出渔网的行列是多少
    row = (top - bottom) / 100
    col = (right - left) / 100
    print(row,col)

    # 检查人为分的行块数和列块数是否可以被整块渔网的行列数整除
    try:
        res = input_r_c(row, col, r, c)
        print(res)

    # 若不满足上述条件，则打印设置好的信息，并退出程序
    except Exception as result:
        print(result)
        sys.exit()

    # 计算分块渔网的四至点
    row1 = (top - bottom) / r
    col1 = (right - left) / c
    count1 = left - col1
    count2 = top + row1
    num = 0
    for i in range(r):
        count2 -= row1
        for j in range(c):
            num += 1
            count1 += col1
            left1 = int(count1)
            right1 = int(count1 + col1)
            top1 = int(count2)
            bottom1 = int(count2 - row1)
            fishnet1 = fishnet + '/' + 'fishnet'+str(num) + '.shp'
            create_fishnet(fishnet1, left1, right1, top1, bottom1)
            # 打印计算好的分块渔网的四至点
            print(left1, right1, top1, bottom1)
        count1 = left - col1


# 定义给渔网添加字段函数
def addField(fishnet):

    # 工作环境为fishnet的路径，即生成渔网的路径
    arcpy.env.workspace = fishnet

    # point_list是采样点矢量数据集名称列表
    fishnet_list = arcpy.ListFeatureClasses()

    # 遍历矢量数据集名称列表，point是当前循环指针所指数据集名称
    for net in fishnet_list:

        # 给point数据集，添加mask字段
        arcpy.AddField_management(net, 'mask', 'FLOAT')

        # 统改point数据集中的mask字段值
        arcpy.CalculateField_management(net, 'mask', 1)

    # 打印工作进度，即成功添加字段
    print('addField success!!!')


# 定义矢栅转化函数
def polygontoraster(fishnet, mask):

    # 工作环境为fishnet的路径，即生成渔网的路径
    arcpy.env.workspace = fishnet
    fishnet_list = arcpy.ListFeatureClasses()
    for net in fishnet_list:
        arcpy.MakeFeatureLayer_management(net, 'fishnet_lyr')
        arcpy.SelectLayerByLocation_management('fishnet_lyr', 'intersect', raw_input)
        arcpy.CopyFeatures_management('fishnet_lyr', fishnet[:-4] + '2mask/' + net.split('.')[0][4:])
        inFeatures = 'fishnet_lyr'
        valField = 'mask'
        outRaster = mask + '/' + net.split('.')[0]
        assignmentType = 'CELL_CENTER'
        priorityField = 'NONE'
        cellSize = 100
        arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
        #arcpy.FeatureToRaster_conversion(inFeatures, valField, outRaster, cellSize)

    print('polygontoraster success!!!')


# 定义镶嵌函数
def mosic(mask, mask_name):

    # 工作环境为fishnet的路径，即生成掩膜的路径
    arcpy.env.workspace = mask
    list_label = []
    rasters = arcpy.ListRasters()
    for raster in rasters:
        list_label.append(raster)
    list_label = ';'.join(list_label)
    arcpy.MosaicToNewRaster_management(list_label, mask, mask_name, cellsize=1000, number_of_bands=1)
    print('mosic success!!!')


# 定义主调函数
def execute(fishnet, mask, r, c, mask_name):

    # 执行渔网四至点函数
    boundry_fishnet(fishnet, r, c)

    # 执行给渔网添加字段
    addField(fishnet)

    # 执行矢栅转化
    polygontoraster(fishnet, mask)

    # 执行镶嵌
    mosic(mask, mask_name)


# 主调程序
if __name__ == '__main__':

    # 设置覆盖模式环境参数（Set environment settings）
    arcpy.env.overwriteOutput = True

    # 原始矢量面相关数据
    raw_input = 'D:/QZGY/qzgy_zr.shp'
    raw_input_prj = 'D:/QZGY/qzgy_zr.prj'

    # 生成的渔网所保存的路径
    fishnet = 'D:/QZGY/mask/1net'

    # 生成的掩膜所保存的路径
    mask = 'D:/QZGY/mask/2mask'

    # 添加空间投影
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(raw_input_prj)

    # 分块的行列数（r行数为2，c列数为2，共创建4个渔网）
    r = 8
    c = 6

    # 合并的分块掩膜的名称
    mask_name = 'zr_mask'

    # 执行主调函数
    execute(fishnet, mask, r, c, mask_name)

    # 打印最终工作进度是否完成
    print('all success!!!')
