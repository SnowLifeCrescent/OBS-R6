import numpy as np
from numpy.fft import fft2, ifft2
from PIL import ImageGrab, Image
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
from gui_io import Gui_Io
import pyopencl as cl
import pyopencl.array as cl_array
from pyvkfft.opencl import VkFFTApp

def gpu_init():
    global queue
    platforms = cl.get_platforms()
    devices = platforms[0].get_devices(cl.device_type.GPU)
    print("GPU信息：", devices)
    ctx = cl.Context(devices)
    queue = cl.CommandQueue(ctx)

def carrier_grab():

    global carrier_fft, carrier_size, carrier_size_1, app, queue, carrier_image_array

    gpu_init()

    carrier_image = Gui_Io()                                                # 屏幕截图

    carrier_size = carrier_image.size                                       # 图像尺寸

    carrier_image_array = np.array(carrier_image)                            # 图转数组

    carrier_image_array = carrier_image_array.astype(np.float32)              # 转浮点数

    carrier_size_1 = carrier_image_array.shape
    carrier_image_Array = cl_array.Array(queue, shape=carrier_size_1, dtype=np.float32)  # Array cl数组
    carrier_image_Array.set(carrier_image_array)

    carrier_type = carrier_image_Array.dtype                                 # 数组类型

    app = VkFFTApp(carrier_size, carrier_type, queue, ndim=2, inplace=True) # FFT

    carrier_fft = gpu_compute(carrier_image_Array)
    print("载体图像已加载")
    return 1

def gpu_compute(input_array):
    global app
    return app.fft(input_array).get()

def gpu_icompute(input_array):
    global app
    return app.ifft(input_array).get()

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

def fft_(watermark_Array):
    watermark_fft = gpu_compute(watermark_Array)
    return watermark_fft

def ifft_transform(watermark_fft):
        global carrier_fft, queue
        alpha = 1
        output_image = carrier_fft + alpha * watermark_fft
        output_image_array = output_image.astype(np.float32)
        # 对得到的 FFT 结果进行逆变换
        output_image_size_1 = output_image.shape
        output_image_iArray = cl_array.Array(queue, shape=output_image_size_1, dtype=np.float32)
        output_image_iArray.set(output_image_array)
        return output_image_iArray

def ifft_(output_image_iArray):
        global output_image_ifft
        output_image_ifft = gpu_icompute(output_image_iArray)
        return output_image_ifft

def output_(output_image_ifft):
    # 获取实部数组
    real_part = np.abs(output_image_ifft)
    # 归一化
    normalized_real_part = normalize_(real_part)
    # output_image_array = np.reshape(normalized_real_part, carrier_image_array.shape)
    # 将数组转换为整数类型
    output_image_array = normalized_real_part.astype(np.uint8)
    return output_image_array

