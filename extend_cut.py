import os
import geopandas as gpd
import rasterio
from shapely.geometry import box
from rasterio.windows import Window


def expand_box(geom, pixel_size, transform):
    if geom is None:
        return None

    minx, miny, maxx, maxy = geom.bounds

    # 将边界转换为像素坐标
    left, top = ~transform * (minx, maxy)
    right, bottom = ~transform * (maxx, miny)

    # 计算中心
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2

    # 扩展
    half_size = pixel_size // 2
    left = center_x - half_size
    right = center_x + half_size
    top = center_y - half_size
    bottom = center_y + half_size

    # 将新的像素边界转换回地理坐标
    new_minx, new_maxy = transform * (left, top)
    new_maxx, new_miny = transform * (right, bottom)

    return box(new_minx, new_miny, new_maxx, new_maxy)


def process_tiff_and_shapefile(tiff_path, shapefile_path, output_dir, pixel_size):
    # 创建子文件夹
    tiff_output_dir = os.path.join(output_dir, 'tif_folder')
    shp_output_dir = os.path.join(output_dir, 'shapefiles')
    os.makedirs(tiff_output_dir, exist_ok=True)
    os.makedirs(shp_output_dir, exist_ok=True)

    # 读取shp文件
    gdf = gpd.read_file(shapefile_path)

    # 读取tiff文件
    tiff = rasterio.open(tiff_path)

    # 获取transform
    transform = tiff.transform

    # 扩大每个框
    gdf['expanded_geom'] = gdf['geometry'].apply(lambda x: expand_box(x, pixel_size, transform))

    # 过滤掉无效的几何对象
    gdf = gdf[gdf['expanded_geom'].notnull()]

    # 仅保留扩展的几何列
    gdf = gdf[['expanded_geom']]
    gdf = gdf.rename(columns={'expanded_geom': 'geometry'})

    # 处理每个几何对象
    for idx, row in gdf.iterrows():
        geom = row['geometry']
        bounds = geom.bounds

        # 将边界转换为像素坐标
        window = rasterio.windows.from_bounds(*bounds, transform=transform)

        # 读取并裁剪图像
        cropped_image = tiff.read(window=window)

        # 保存裁剪的图像
        out_path = os.path.join(tiff_output_dir, f'crop_{idx}.tif')
        with rasterio.open(out_path, 'w', driver='GTiff',
                           height=cropped_image.shape[1],
                           width=cropped_image.shape[2],
                           count=cropped_image.shape[0],
                           dtype=cropped_image.dtype,
                           crs=tiff.crs,
                           transform=tiff.window_transform(window)) as dst:
            dst.write(cropped_image)

    # 保存扩展后的shp文件
    expanded_shapefile_path = os.path.join(shp_output_dir, 'expanded_shapefile.shp')
    gdf.to_file(expanded_shapefile_path)

    # 返回扩展后的shp文件路径
    return expanded_shapefile_path

# # 使用示例
# tiff_path = r'F:\sicktrees\biaozhu4\result.tif'
# shapefile_path = r'F:\sicktrees\biaozhu4\2_Output.shp'
# output_dir = 'F:\\sicktrees\\output'
# pixel_size = 800
#
# process_tiff_and_shapefile(tiff_path, shapefile_path, output_dir, pixel_size)