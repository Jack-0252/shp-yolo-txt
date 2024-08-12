import geopandas as gpd
import os

def clip_shapes_and_save(shpA_path, shpB_path, output_dir):
    # 加载shapefile数据
    shpA = gpd.read_file(shpA_path)
    shpB = gpd.read_file(shpB_path)

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_files = 0

    # 遍历shpB中的每个大框
    for i, row in shpB.iterrows():
        big_box = row.geometry

        # 检查big_box是否有效
        if big_box is None or big_box.is_empty:
            print(f"Warning: shpB index {i} has invalid or empty geometry.")
            continue

        try:
            # 使用clip裁剪shpA，使其仅保留位于大框内的部分
            clipped_shapes = gpd.clip(shpA, big_box)
        except Exception as e:
            print(f"Error processing shpB index {i}: {e}")
            continue

        if not clipped_shapes.empty:
            subfolder_name = f"crop_{i}"
            subfolder_path = os.path.join(output_dir, subfolder_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

            output_path = os.path.join(subfolder_path, f"{subfolder_name}.shp")
            clipped_shapes.to_file(output_path)
            generated_files += 1
            print(f"Saved clipped shapefile for shpB index {i} to {output_path}")
        else:
            print(f"No shapes in shpA intersect with shpB index {i}")

    if generated_files == 0:
        print(f"No shapefiles were generated. Check the spatial relationship between shpA and shpB.")
    else:
        print(f"Generated {generated_files} shapefiles in {output_dir}")


# # 使用示例
# shpB_path = 'output\shapefiles\expanded_shapefile.shp'      # big
# shpA_path = 'biaozhu4/2_Output.shp'                         # small
# output_dir = 'output\more_shp'
# merge_shapes_and_save(shpA_path, shpB_path, output_dir)
