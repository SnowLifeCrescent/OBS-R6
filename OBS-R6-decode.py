import pyffmpeg
import cv2
import tkinter as tk
import threading

url = None

class VideoCapture:
    def __init__(self, url):
        self.vid = pyffmpeg.VideoStream(url)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", url)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def confirm():
    global url
    url = path_entry.get()
    window.destroy()

    image_path = "D:\Programing\Temp\Output.jpg"
    num_bits = 1  # 假设隐藏时使用的是1位LSB
    if url is "":
        window2 = tk.Tk()
        window2.title("错误")
        lable = tk.Label(window2, text="无效url，关闭窗口程序将自行退出")
        lable.pack()
        window2.mainloop()
        window2.destroy()
        exit(0)
    else:
        #cap_thread = threading.Thread(target=cap)
        #cap_thread.start()
        decode_thread = threading.Thread(target=decode(image_path, num_bits))
        decode_thread.start()

def cap():
    global url
    cap = VideoCapture(url)
    while True:
        ret, frame = cap.get_frame()
        if ret:
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == 27 :
                break
        else:
            break
    cap.__del__()
    cv2.destroyAllWindows()
    window2 = tk.Tk()
    window2.title("错误")
    lable = tk.Label(window2, text="该url无法获取视频信息，关闭窗口程序将自行退出")
    lable.pack()
    window2.mainloop()
    window2.destroy()
    exit(0)


def decode(image_path, num_bits):
    while True:
        # 读取图像
        image = cv2.imread(image_path)

        # 初始化提取的隐藏信息
        hidden_data = ""

        # 获取图像尺寸
        height, width, _ = image.shape

        # 遍历图像像素
        for y in range(width):
            for x in range(height):
                pixel = image[y, x]

                # 提取隐藏信息
                hidden_bits = bin(pixel[0])[-num_bits:]  # 提取蓝色通道的LSB
                hidden_data += hidden_bits

        # 将隐藏信息转换为字节
        byte_data = bytes([int(hidden_data[i:i + 8], 2) for i in range(0, len(hidden_data), 8)])

        return byte_data



window = tk.Tk()
window.title("OBS-R6-decode")

lable = tk.Label(window, text="请填入直播流url")
lable.pack()
path_entry = tk.Entry(window, width=50)
path_entry.pack()
confirm_button = tk.Button(window, text="确认", command=window.quit)
confirm_button.pack()

window.mainloop()
