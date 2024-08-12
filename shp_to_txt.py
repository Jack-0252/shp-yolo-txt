import os
import geopandas as gpd
import rasterio
from rasterio.transform import Affine
import numpy as np

def shp_to_yolo(shp_folder, tif_folder, tfw_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 递归遍历所有子文件夹
    for root, dirs, files in os.walk(shp_folder):
        for shp_file in files:
            if shp_file.endswith('.shp'):
                # 获取文件名（无扩展名）
                base_name = os.path.splitext(shp_file)[0]
                tif_file = os.path.join(tif_folder, base_name + '.tif')
                tfw_file = os.path.join(tfw_folder, base_name + '.tfw')
                shp_path = os.path.join(root, shp_file)

                # 检查 TIFF 文件是否存在
                if not os.path.exists(tif_file):
                    print(f"TIFF 文件不存在: {tif_file}, 跳过该文件")
                    continue

                # 读取shapefile和对应的tif图像
                gdf = gpd.read_file(shp_path)
                try:
                    with rasterio.open(tif_file) as src:
                        transform = src.transform
                        img_width, img_height = src.width, src.height
                except rasterio.errors.RasterioIOError as e:
                    print(f"无法打开 TIFF 文件: {tif_file}, 错误: {e}")
                    continue

                # 使用 tfw 文件更新 transform
                if os.path.exists(tfw_file):
                    with open(tfw_file) as tfw:
                        tfw_values = list(map(float, tfw.read().splitlines()))
                        try:
                            new_transform = Affine.from_gdal(*tfw_values)
                            # 如果新的变换是可逆的，则使用它
                            if new_transform.determinant != 0:
                                transform = new_transform
                        except Exception as e:
                            print(f"无法使用tfw文件更新变换矩阵，错误：{e}")

                # YOLO格式的txt文件保存路径
                txt_output_path = os.path.join(output_folder, base_name + '.txt')

                with open(txt_output_path, 'w') as txt_file:
                    for _, row in gdf.iterrows():
                        # 获取每个图形的外接矩形框
                        geom = row.geometry
                        minx, miny, maxx, maxy = geom.bounds
                        try:
                            # 坐标转换
                            minx_pixel, miny_pixel = ~transform * (minx, miny)
                            maxx_pixel, maxy_pixel = ~transform * (maxx, maxy)
                        except Exception as e:
                            print(f"无法转换坐标：{(minx, miny)} 至 {(maxx, maxy)}，错误：{e}，跳过该框。")
                            continue

                        # 确保坐标在图像范围内
                        minx_pixel = np.clip(minx_pixel, 0, img_width)
                        maxx_pixel = np.clip(maxx_pixel, 0, img_width)
                        miny_pixel = np.clip(miny_pixel, 0, img_height)
                        maxy_pixel = np.clip(maxy_pixel, 0, img_height)

                        # 计算中心点和宽高，并转换为YOLO格式
                        x_center = (minx_pixel + maxx_pixel) / 2.0 / img_width
                        y_center = (miny_pixel + maxy_pixel) / 2.0 / img_height
                        width = abs((maxx_pixel - minx_pixel) / img_width)
                        height = abs((maxy_pixel - miny_pixel) / img_height)

                        # 写入txt文件（class_id这里假设为0）
                        txt_file.write(f"0 {x_center} {y_center} {width} {height}\n")

    print("转换完成！")

# # 示例使用
# shp_folder = 'F:\\sicktrees\\output\\shp_folder'  # 替换为你的shp文件夹路径
# tif_folder = 'F:\\sicktrees\\output\\tif_folder'  # 替换为你的tif文件夹路径
# tfw_folder = "F:\\sicktrees\\output\\tfw_folder"
# output_folder = 'F:\\sicktrees\\output\\txt_folder'  # 替换为你希望保存txt文件的文件夹路径
#
# shp_to_yolo(shp_folder, tif_folder, tfw_folder, output_folder)
