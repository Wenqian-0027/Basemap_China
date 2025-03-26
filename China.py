import geopandas as gpd
import numpy as np
import os
import pylab as plt
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patches as mpatches
from pyproj import CRS
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号


def plot_stacked_bar(data, colormap='jet_r', figsize=(10, 5), title='', width=0.9):
    """
    Plot a stacked bar chart for the given DataFrame.

    Parameters:
    - data: DataFrame to be plotted.
    - colormap: Colormap to use for different bars.
    - figsize: Tuple representing the figure size.
    - title: Title of the plot.
    - width: Width of the bars.
    """
    # Create a color map
    cmap = plt.get_cmap(colormap)
    colors = [cmap(i) for i in np.linspace(0, 1, len(data.columns))]

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    plt.title(title, fontsize=16)
    data.plot(ax=ax, kind='bar', stacked=True, width=width, color=colors)
    plt.show()




def add_north(ax, labelsize=18, loc_x=0.9, loc_y=0.9, width=0.04, height=0.13, pad=0):
    """
    画一个比例尺带'N'文字注释
    主要参数如下
    :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
    :param labelsize: 显示'N'文字的大小
    :param loc_x: 以文字下部为中心的占整个ax横向比例
    :param loc_y: 以文字下部为中心的占整个ax纵向比例
    :param width: 指南针占ax比例宽度
    :param height: 指南针占ax比例高度
    :param pad: 文字符号占ax比例间隙
    :return: None
    """
    minx, maxx = ax.get_xlim()
    miny, maxy = ax.get_ylim()
    ylen = maxy - miny
    xlen = maxx - minx
    left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
    right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
    top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
    center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
    triangle = mpatches.Polygon([left, top, right, center], color='k')
    ax.text(s='N',
            
            x=minx + xlen * loc_x,
            y=miny + ylen * (loc_y - pad + height),
            fontsize=labelsize,
            horizontalalignment='center',
            verticalalignment='bottom')
    ax.add_patch(triangle)

#颜色设置

def get_color(flag_value):
    
    color_map = {
        1: (255/255, 255/255, 255/255, 0),     # 海岸线蓝  
        2: (0/255, 0/255, 0/255),       # 黑色
        3: (158/255, 170/255, 215/255),     # d蓝色
        4: (194/255, 209/255, 255/255),     # q蓝色
    }
    return color_map.get(flag_value, (255/255, 255/255, 255/255))  # 默认灰色
   # return color_map.get(flag_value, (255/255, 255/255, 255/255)) if flag_value != 1 else None  # 白色部分返回 None



# -------------------------------地图数据
working_path = r'D:/A-HKU/WRI_Intern'
os.chdir(working_path)

#prjdir = os.path.join(os.getcwd(), 'project/')
mapdir = os.path.join(os.getcwd(), 'basemap_plate_carree/China/')
insetmapdir = os.path.join(os.getcwd(), 'basemap_plate_carree/Nanhai/')


# 投影坐标
prj_file_path = os.path.join(mapdir, '海岸线.prj')
with open(prj_file_path, 'r') as file:
    prj_txt = file.read()
    crs_string = prj_txt.strip()
    target_crs = CRS.from_wkt(crs_string)

# 国界线
bound_file_path = os.path.join(mapdir, '国界线.shp')
# 海岸线
sea_coastline = os.path.join(mapdir, '海岸线.shp')
# 省界底图_styleisempty
Baseprov = os.path.join(mapdir, '中国_省.geojson')
# 省界线
Provborder = os.path.join(mapdir, '中国省界line_final.shp')
# 南海诸岛
Island = os.path.join(insetmapdir,'南海诸岛new.shp')
# Basemap
#basemap = os.path.join(mapdir, 'adj_basemap.shp')

distance_meters = 1
# 国界线
bound_geo = gpd.read_file(bound_file_path).to_crs(target_crs)
# 海岸线
sea_geo = gpd.read_file(sea_coastline).to_crs(target_crs)
# sea_geo = adjust_geo(sea_geo,1057)  # 调整polygon
# 省界底图
Baseprov_geo = gpd.read_file(Baseprov).to_crs(target_crs)
#省界线
Provborder_geo = gpd.read_file(Provborder).to_crs(target_crs)
#岛屿
Island_geo = gpd.read_file(Island).to_crs(target_crs)
#nineLine_geo = gpd.read_file(nineLine).to_crs(target_crs)
# basemap
#basemap_geo = gpd.read_file(basemap).to_crs(target_crs)


# -------------------------------作图
fig, ax = plt.subplots(figsize=(15, 15), dpi=100)

# 生成一个颜色列表，基于 flag 字段的值
bound_geo['color'] = bound_geo['flag'].apply(get_color)

# 底图
#basemap_geo.plot(ax=ax, color='lightgrey')

# 国家边界
bound_geo.plot(ax=ax, color=bound_geo['color'], linewidth=1)
#bound_geo.plot(ax=ax, color='black', linewidth=1)
# 省界底图
Baseprov_geo.plot(ax=ax, color='none', edgecolor='none', linewidth=1)
# 省界线
Provborder_geo.plot(ax=ax, color='#686868', edgecolor='none', linewidth=1)

# 海岸线
sea_geo.plot(ax=ax, color='#73B2FF',  edgecolor='#73B2FF',linewidth=1)

#海岸线
Island_geo.plot(ax=ax, color='#73B2FF', edgecolor='none',linewidth=1)

#nineLine_geo.plot(ax=ax, color='black', linewidth=0.5)
# 添加指南针
add_north(ax, labelsize=15, loc_x=1.05, loc_y=1, width=0.01, height=0.04, pad=0.1)

# 在地图中添加比例尺和像素尺寸 https://www.cnblogs.com/luohenyueji/p/17485432.html
scalebar = ScaleBar(dx=distance_meters,
                    box_color="grey",
                    box_alpha=0.0,
                    length_fraction=0.3,
                    dimension="si-length",
                    location="lower left",
                    units="m",
                    scale_formatter=lambda value, _: f"{value*1000:} km")
ax.add_artist(scalebar)

ax.set_xticks([])
ax.set_yticks([])
ymin, ymax = ax.get_ylim()
#ax.set_ylim(ymin + 1500000, ymax - 500000)

ax.set_ylim(ymin + 1760000 , ymax)
xmin, xmax = ax.get_xlim()
#ax.set_xlim(xmin + 2000000, xmax - 2000000)
ax.set_xlim(xmin - 300000, xmax + 700000)
# 添加标题
plt.title('图名', fontsize=16)


# -------------------------------海南诸岛作图


# 南海诸岛省界
Nanhai_v1_path = os.path.join(insetmapdir, '南海诸岛v1_new.shp')
# 南海诸岛九段线
Nanhai_v2_path = os.path.join(insetmapdir, '南海诸岛v2_new.shp')
# 南海诸岛岛屿:Island_geo已建立
#Nanhai_island = os.path.join(insetmapdir,'南海诸岛_7kmBuffer.shp')

# 南海诸岛省界
Nanhai_v1_geo = gpd.read_file(Nanhai_v1_path).to_crs(target_crs)
# 南海诸岛九段线
Nanhai_v2_geo = gpd.read_file(Nanhai_v2_path).to_crs(target_crs)

# 计算边界范围（bounding box）
bounds1 = Nanhai_v1_geo.total_bounds  # (minx, miny, maxx, maxy)
bounds2 = Nanhai_v2_geo.total_bounds

# 合并边界范围
min_x = min(bounds1[0], bounds2[0])
min_y = min(bounds1[1], bounds2[1])
max_x = max(bounds1[2], bounds2[2])
max_y = max(bounds1[3], bounds2[3])

# 计算 padding，使图形不贴边
padding_x = (max_x - min_x) * 0.02  # 5% padding
padding_y = (max_y - min_y) * 0.02

# 创建 inset_axes
ax_inset = inset_axes(ax, width="15%", height="30%", loc="lower right")

# 隐藏子图的坐标轴
ax_inset.set_xticks([])
ax_inset.set_yticks([])

# 设置子图边界范围，使数据适配
#ax_inset.set_xlim(min_x-30000, max_x - 2200000)
#ax_inset.set_ylim(min_y, max_y - 800000)

ax_inset.set_xlim(min_x - padding_x, max_x + padding_x)
ax_inset.set_ylim(min_y - padding_y, max_y + padding_y)

# 使地图比例适配数据
ax_inset.set_aspect('auto')

# 生成一个颜色列表，基于 flag 字段的值
Nanhai_v2_geo['color'] = Nanhai_v2_geo['flag'].apply(get_color)

# 在子图中绘制 shapefile 数据
#Nanhai_v1_geo.plot(ax=ax_inset, color='#6E6E6E', alpha=0.7)
Nanhai_v1_geo.plot(ax=ax_inset, 
                   color=Nanhai_v1_geo['flag'].apply(lambda x: '#73B2FF' if x == 1 else '#686868'),
                   edgecolor=Nanhai_v1_geo['flag'].apply(lambda x: '#73B2FF' if x == 1 else '#686868'),
                   alpha=0.7, 
                   linewidth=1)
Nanhai_v2_geo.plot(ax=ax_inset, color=Nanhai_v2_geo['color'] , alpha=0.7)
Island_geo.plot(ax=ax_inset, color='#73B2FF', edgecolor='#73B2FF',linewidth=1)


# 在右下角添加文本框 变小
ax_inset.text(0.80, 0.05, '南海诸岛', transform=ax_inset.transAxes, fontsize=9, ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.6, boxstyle='square,pad=0.5'))

# 显示图形
plt.show()
