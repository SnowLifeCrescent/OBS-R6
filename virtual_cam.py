import cap_game
#import threading
import keyboard
import numpy as np
import pyvirtualcam
import cv2
import time
import FFT
import concurrent.futures

# 引入进程判定，彩六限定
Process_R6 = ""
#---------------------------#
# 捕获窗口，获得画面
window = cap_game.get_window("chro.*")
FFT.carrier_grab()
#---------------------------#

def virtual_cam():
    global output_image_array, height, width
    height, width,_ = output_image_array.shape
    time.sleep(1)
    # 创建虚拟摄像头
    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print(f"已创建虚拟摄像头：{width}x{height}")
        while True:
            cam.send(output_image_array)
            if breaking():
                print('virtual_cam closed')
                break
    return


def getting_Image():
    global window, output_image_array
    imagearray = get_image_array(window)
    watermark_Array = judgement(imagearray)
    watermark_fft = fft_(watermark_Array)
    output_image_iArray = ifft_transform(watermark_fft)
    output_image_ifft = ifft_(output_image_iArray)
    output_image_array = output_(output_image_ifft)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.submit(virtual_cam)
    #virtual_cam_thread.start()
        while True:
            imagearray = executor.submit(get_image_array, window).result()
            watermark_Array = executor.submit(judgement, imagearray).result()
            watermark_fft = executor.submit(fft_, watermark_Array).result()
            output_image_iArray = executor.submit(ifft_transform, watermark_fft).result()
            output_image_ifft = executor.submit(ifft_, output_image_iArray).result()
            output_image_array = executor.submit(output_, output_image_ifft).result()

            #executor.shutdown(wait=True)
            if breaking():
                break
    print('getting_Image closed')
    return

def get_image_array(window):
    return cap_game.get_image_array(window)

def judgement(imagearray):
    return FFT.judgement(imagearray)

def fft_(watermark_Array):
    return FFT.fft_(watermark_Array)

def ifft_transform(watermark_fft):
    return FFT.ifft_transform(watermark_fft)

def ifft_(output_image_iArray):
    return FFT.ifft_(output_image_iArray)

def output_(output_image_ifft):
    return FFT.output_(output_image_ifft)

def breaking():
    if keyboard.is_pressed('m') and keyboard.is_pressed('p') and keyboard.is_pressed('4') and keyboard.is_pressed("9"):
        return True
    return False

#getting_Image_thread = threading.Thread(target=getting_Image)
#virtual_cam_thread = threading.Thread(target=virtual_cam)

#getting_Image_thread.start()
getting_Image()

#getting_Image_thread.join()
#virtual_cam_thread.join()
print('0')
