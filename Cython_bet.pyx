import numpy as np
import pyopencl as cl
import pyopencl.array as cl_array
from PIL import Image

def judgement(image_array):
    global watermark_image_array, carrier_size, carrier_size_1, queue
    if carrier_size != image_array.shape:
        # 缩放尺寸
        image = Image.fromarray(image_array)
        image = image.resize((carrier_size[1], carrier_size[0]), Image.LANCZOS)
        watermark_image = np.array(image)

        # FFT前预处理
        watermark_image_array = np.array(watermark_image)
        watermark_image_array = watermark_image_array.astype(np.float32)
        watermark_Array = cl_array.Array(queue, shape=carrier_size_1, dtype=np.float32)
        watermark_Array.set(watermark_image_array)
    else:
        # FFT前预处理
        image_array = image_array.astype(np.float32)
        watermark_Array = cl_array.Array(queue, shape=carrier_size_1, dtype=np.float32)
        watermark_Array.set(image_array)
    return watermark_Array

def normalize_(data):
    # 确定数据的最小值和最大值
    min_val = np.min(data)
    max_val = np.max(data)
    # 对数或幂函数参数，可以根据需求调整
    a = 255.0 / (np.log(1 + max_val) - np.log(1 + min_val))
    # 对数据应用非线性均一化
    normalized_data = a * (np.log(1 + data) - np.log(1 + min_val))
    # 确保数据范围在 0-255 之间
    normalized_data = np.clip(normalized_data, 0, 255)
    # 将数据转换为整数类型（0-255的范围）
    normalized_data = normalized_data.astype(np.uint8)
    return normalized_data