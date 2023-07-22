import keyboard
import cv2
import threading
from pywt import dwt2, idwt2
import numpy as np
from PIL import ImageGrab
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
from obswebsocket import obsws, requests


def dwt2_encode(_carrier_image_path, _game_image_path, _output_image_path):
    # 读取载体图像和水印图像
    carrier_image = cv2.imread(_carrier_image_path)
    watermark_image = cv2.imread(_game_image_path)

    # 确保水印图像的尺寸与载体图像相同
    watermark_image = cv2.resize(watermark_image, (carrier_image.shape[1], carrier_image.shape[0]))

    # 使用2级小波变换进行嵌入
    coeffs_carrier = dwt2(carrier_image, 'haar')
    coeffs_watermark = dwt2(watermark_image, 'haar')

    # 将水印图像的小波系数嵌入到载体图像的小波系数中
    coeffs_combined = []
    for i in range(len(coeffs_carrier)):
        channel_coeffs_combined = []
        for j in range(len(coeffs_carrier[i])):
            channel_coeffs_combined.append(coeffs_carrier[i][j] + coeffs_watermark[i][j])
        coeffs_combined.append(tuple(channel_coeffs_combined))

    # 进行逆小波变换恢复水印嵌入后的载体图像
    watermarked_image = idwt2(coeffs_combined, 'haar')

    # 将像素值截断为0-255的范围
    watermarked_image = np.clip(watermarked_image, 0, 255).astype(np.uint8)

    # 保存嵌入水印后的图像
    cv2.imwrite(_output_image_path, watermarked_image)


def load_img():
    global Game_Img
    while True:
        with lock:
            ws.call(requests.SaveSourceScreenshot(sourceName="11025", imageFormat="jpg",
                                                  imageFilePath=_game_image_path,
                                                  imageWidth=3840, imageHeight=1600,
                                                  imageCompressionQuality=100))
            Game_Img = cv2.imread(_game_image_path)
            cv2.waitKey(1)
        if keyboard.is_pressed('m') and keyboard.is_pressed('p') and keyboard.is_pressed('4') \
                and keyboard.is_pressed("9"):
            break


def display_img():
    global Game_Img, _carrier_image_path, _game_image_path, _output_image_path, Output_Img
    while True:
        with lock:
            dwt2_encode(_carrier_image_path, _game_image_path, _output_image_path)

        if keyboard.is_pressed('m') and keyboard.is_pressed('p') and keyboard.is_pressed('4') \
                and keyboard.is_pressed("9"):
            break


Game_Img = None
Output_Img = None
folder_path = None
_carrier_image_path = None
_game_image_path = None
_output_image_path = None
port = None
password = None
lock = threading.Lock()


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder_path)


def confirm_selection():
    global folder_path, port, password
    folder_path = path_entry.get()
    port = port_entry.get()
    password = password_entry.get()
    window.destroy()
    if folder_path is not "" and port is not "" and password is not "":
        window2 = tk.Tk()
        window2.title("须知")
        highlight_font = tkfont.Font(family="Arial", size=16, weight="bold")
        lable1 = tk.Label(window2, text="重要！！！\n\n")
        lable1.pack()
        lable1.config(font=highlight_font)
        lable2 = tk.Label(window2, text="当程序正常运行时想要退出程序请\n"
                                        "同时长按键盘上的\n")
        lable2.pack()
        lable3 = tk.Label(window2, text="M P 4 9 键\n")
        lable3.pack()
        lable3.config(font=highlight_font)
        lable4 = tk.Label(window2, text="关闭当前窗口以继续")
        lable4.pack()
    else:
        window2 = tk.Tk()
        window2.title("错误")
        lable = tk.Label(window2, text="非法输入！请填写完整信息")
        lable.pack()


# 创建主窗口
window = tk.Tk()
window.title("骗过超管")
frame_pack = tk.Frame(window)
frame_pack.pack(side=tk.TOP)
frame_grid = tk.Frame(window)
frame_grid.pack()

title_label = tk.Label(frame_pack, text="\n------------------------------------------------------------"
                                        "\n该路径用于保存程序运行过程中产生的图片（只有三张）\n\n"
                                        "图片可随时删除而不会影响程序运行\n"
                                        "------------------------------------------------------------\n\n")
title_label.pack(side=tk.TOP)

# 创建路径输入框
path_label = tk.Label(frame_grid, text="文件夹路径：")
path_label.grid(row=0, column=0)
path_entry = tk.Entry(frame_grid, width=50)
path_entry.grid(row=0, column=1)

# 创建选择文件夹按钮
select_button = tk.Button(frame_grid, text="选择文件夹", command=select_folder)
select_button.grid(row=0, column=2)

# 端口输入框
port_label = tk.Label(frame_grid, text="端口号：")
port_label.grid(row=1, column=0)
port_entry = tk.Entry(frame_grid, width=50)
port_entry.grid(row=1, column=1)

# 密码输入框
password_label = tk.Label(frame_grid, text="密码：")
password_label.grid(row=2, column=0)
password_entry = tk.Entry(frame_grid, width=50)
password_entry.grid(row=2, column=1)

# 创建确认选择按钮
confirm_button = tk.Button(window, text="确认", command=confirm_selection)
confirm_button.pack()

window.mainloop()

if folder_path is not None and port is not None and password is not None:
    _carrier_image_path = folder_path + "/carrier.jpg"
    _game_image_path = folder_path + "/Gaming-screenshot.jpg"
    _output_image_path = folder_path + "/Output.jpg"

# 连接到 OBS WebSocket 服务器
ws = obsws("localhost", port, password)
ws.connect()

carrier_shot = ImageGrab.grab()
carrier_shot.save(_carrier_image_path)

# 创建线程
loading_thread = threading.Thread(target=load_img)
display_thread = threading.Thread(target=display_img)

loading_thread.start()
display_thread.start()

loading_thread.join()
display_thread.join()

ws.disconnect()
