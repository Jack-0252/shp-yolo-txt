import geopandas as gpd
from extend_cut import process_tiff_and_shapefile
from tif_create_tfw import generate_tfw_files
from txt_kuang import process_images
from shp_to_moreshp import clip_shapes_and_save
from shp_to_txt import shp_to_yolo

def main():

    # step1:扩展并裁图
    tiff_path = '7/1.tif'
    shapefile_path = '7/Output.shp'
    output_dir = 'output_multi'
    pixel_size = 800

    process_tiff_and_shapefile(tiff_path, shapefile_path, output_dir, pixel_size)
    print("Step1--extend&cut completed.")

    # step2：tif生成tfw
    tif_folder = 'output_multi/tif_folder'
    tfw_folder = 'output_multi/tfw_folder'

    generate_tfw_files(tif_folder, tfw_folder)
    print("Step2--tif_to_tfw completed.")

    # step3: shp转为小shp
    shpB_path = 'output_multi\shapefiles\expanded_shapefile.shp'  # big
    shpA_path = shapefile_path                  # small
    output_dir = 'output_multi\shp_folder'
    clip_shapes_and_save(shpA_path, shpB_path, output_dir)
    print("Step3--shp_to_more_shp completed.")

    # step4: 生成对应txt
    shp_folder = 'output_multi/shp_folder'
    tif_folder = 'output_multi/tif_folder'
    tfw_folder = "output_multi/tfw_folder"
    output_folder = 'output_multi/txt_folder'

    shp_to_yolo(shp_folder, tif_folder, tfw_folder, output_folder)
    print("Step4--shp_to_yolo_txt completed.")

    # step5: 验证
    tif_folder = 'output_multi/tif_folder'
    txt_folder = 'output_multi/txt_folder'
    output_folder = 'output_multi/verify'
    process_images(tif_folder, txt_folder, output_folder)

if __name__ == "__main__":
    main()
