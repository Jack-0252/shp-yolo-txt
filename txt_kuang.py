import os
import cv2
from tqdm import tqdm

def process_images(tif_folder, txt_folder, output_folder):
    """
    处理tif图像，根据对应的txt文件绘制边框，并将结果保存到输出文件夹中。

    Args:
        tif_folder (str): 包含tif图像的文件夹路径。
        txt_folder (str): 包含txt文件的文件夹路径。
        output_folder (str): 输出文件夹路径，绘制好的图像将保存到这里。
    """
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 获取tif图像文件名列表
    tif_files = [f for f in os.listdir(tif_folder) if f.endswith('.tif')]

    # 使用tqdm添加进度条
    for tif_file in tqdm(tif_files, desc="Processing Images"):
        # 读取图像
        img_path = os.path.join(tif_folder, tif_file)
        img = cv2.imread(img_path)

        # 获取图像的尺寸
        height, width = img.shape[:2]

        # 对应的txt文件路径
        txt_file = tif_file.replace('.tif', '.txt')
        txt_path = os.path.join(txt_folder, txt_file)

        # 如果txt文件存在，读取并绘制边框
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                for line in f:
                    # 读取每一行
                    parts = line.strip().split()
                    print(f"Debug: {txt_file} - Line content: {parts}")

                    try:
                        # 假设txt文件中的每一行格式为: 类别名称, x_center, y_center, box_width, box_height
                        if len(parts) == 5:
                            class_name, x_center, y_center, box_width, box_height = parts
                            x_center, y_center, box_width, box_height = map(float,
                                                                            [x_center, y_center, box_width, box_height])

                            # 将相对坐标转换为绝对坐标
                            x_min = int((x_center - box_width / 2) * width)
                            y_min = int((y_center - box_height / 2) * height)
                            x_max = int((x_center + box_width / 2) * width)
                            y_max = int((y_center + box_height / 2) * height)

                            # 绘制矩形框在图像上
                            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                            # 如果需要显示类名称，可以在框上添加文本
                            cv2.putText(img, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                        else:
                            print(f"Warning: {txt_file} - Invalid line format: {line.strip()}")
                    except ValueError as e:
                        print(f"Error: {txt_file} - Failed to parse line: {line.strip()}. Error: {e}")

        # 保存绘制好框的图像
        output_path = os.path.join(output_folder, tif_file)
        cv2.imwrite(output_path, img)

    print("所有图像已处理并保存。")

# # 调用示例
# tif_folder = 'output_multi/tif_folder'  # 替换为实际路径
# txt_folder = 'output_multi/txt_folder'  # 替换为实际路径
# output_folder = 'output_multi/huizhi_folder'  # 替换为输出文件夹路径
#
# process_images(tif_folder, txt_folder, output_folder)
