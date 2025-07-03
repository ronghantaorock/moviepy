import os
import cv2
from PIL.ImageOps import scale


def readDir(directory_path: str) -> list:
    """
    读取指定目录下所有的PNG、JPG和JPEG类型的文件名称

    参数:
        directory_path: 目录路径

    返回:
        包含所有PNG、JPG和JPEG文件名称的列表
    """
    # 检查目录是否存在
    if not os.path.isdir(directory_path):
        print(f"错误: 目录 '{directory_path}' 不存在")
        return []

    # 获取目录中的所有文件
    try:
        all_files = os.listdir(directory_path)
    except Exception as e:
        print(f"读取目录时出错: {e}")
        return []

    # 过滤出PNG、JPG和JPEG文件
    image_files = []
    for file in all_files:
        # 获取文件扩展名并转换为小写进行比较
        _, ext = os.path.splitext(file)
        ext = ext.lower()

        # 检查是否为目标图片格式
        if ext in ['.png', '.jpg', '.jpeg', '.webp']:
            image_files.append(os.path.join(directory_path, file))

    return image_files


def resizeImage(src_path: str, dest_dir: str, size: tuple) -> bool:
    """
    调整图片大小并保存到指定目录

    参数:
        src_path: 源图片的绝对路径
        dest_dir: 调整大小后图片要保存的目录路径
        size: 包含新宽度和高度的元组 (width, height)

    返回:
        bool: 操作成功返回True，失败返回False
    """
    try:
        # 检查源文件是否存在
        if not os.path.isfile(src_path):
            print(f"错误: 源文件 '{src_path}' 不存在")
            return False

        # 确保目标目录存在
        os.makedirs(dest_dir, exist_ok=True)

        # 获取原文件名
        file_name = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, file_name)

        # 读取图片
        img = cv2.imread(src_path)
        if img is None:
            print(f"错误: 无法读取图片 '{src_path}'")
            return False

        # 调整图片大小
        (ih, iw) = img.shape[:2]
        scale_size = min(size[0] / iw, size[1] / ih)
        new_size = (int(iw * scale_size), int(ih * scale_size))
        resized_img = cv2.resize(img, new_size)

        # 保存调整大小后的图片
        cv2.imwrite(dest_path, resized_img)

        return True

    except Exception as e:
        print(f"处理图片时出错: {e}")
        return False