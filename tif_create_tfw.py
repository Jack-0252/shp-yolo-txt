import os
import rasterio


def generate_tfw_files(tif_folder, tfw_folder):
    if not os.path.exists(tfw_folder):
        os.makedirs(tfw_folder)

    tif_files = [f for f in os.listdir(tif_folder) if f.lower().endswith('.tif')]

    for tif_file in tif_files:
        tif_path = os.path.join(tif_folder, tif_file)
        tfw_path = os.path.join(tfw_folder, os.path.splitext(tif_file)[0] + '.tfw')

        with rasterio.open(tif_path) as src:
            # Extract the affine transform parameters
            transform = src.transform
            with open(tfw_path, 'w') as tfw_file:
                tfw_file.write(f"{transform.a}\n")  # Pixel width
                tfw_file.write(f"{transform.b}\n")  # Rotation about y-axis
                tfw_file.write(f"{transform.d}\n")  # Rotation about x-axis
                tfw_file.write(f"{transform.e}\n")  # Pixel height (negative)
                tfw_file.write(f"{transform.xoff}\n")  # x-coordinate of the center of the upper-left pixel
                tfw_file.write(f"{transform.yoff}\n")  # y-coordinate of the center of the upper-left pixel


# 设置 TIFF 文件夹和 TFW 文件夹路径
# tif_folder = 'F:\\sicktrees\\output\\tif_folder'
# tfw_folder = 'F:\\sicktrees\\output\\tfw_folder'
#
# generate_tfw_files(tif_folder, tfw_folder)
