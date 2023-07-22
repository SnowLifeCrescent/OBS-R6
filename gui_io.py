import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
import PIL.ImageGrab as ImageGrab
import time


def confirm_command():
    root.destroy()
    window2 = tk.Tk()
    window2.title("须知")
    highlight_font = tkfont.Font(family="Arial", size=16, weight="bold")
    lable1 = tk.Label(window2, text="\n\n重要！！！\n\n")
    lable1.pack()
    lable1.config(font=highlight_font)
    lable2 = tk.Label(window2, text="\n------------------------------------------------------------\n"
                                    "当程序正常运行时想要退出程序请\n"
                                    "同时长按键盘上的\n")
    lable2.pack()
    lable2.config(font=highlight_font)
    lable3 = tk.Label(window2, text="M P 4 9 键\n"
                                    "------------------------------------------------------------\n")
    lable3.pack()
    lable3.config(font=highlight_font)
    lable4 = tk.Label(window2, text="关闭当前窗口以继续")
    lable4.pack()


def countdown():
    global countdown_label, countdown_time
    countdown_label.config(text=str(countdown_time) + "秒后可点击")
    time.sleep(1)
    if countdown_time > 0:
        countdown_time -= 1
        countdown_label.after(250, countdown)
    else:
        countdown_label.pack_forget()
        confirm_button.config(state=tk.NORMAL)


def Gui_Io():
    global root, countdown_time, countdown_label, confirm_button
    # 创建主窗口
    root = tk.Tk()
    root.title("骗过超管")
    frame_pack = tk.Frame(root)
    frame_pack.pack(side=tk.TOP)
    highlight_font = tkfont.Font(family="Arial", size=16, weight="bold")

    Title_label = tk.Label(frame_pack, text="\n------------------------------------------------------------"
                                            "\n本项目为开源项目-作者-雪青月牙\n\n"
                                            "此种编解码十分低级，请勿将本项目用于违法犯罪\n\n"
                                            "天网恢恢疏而不漏，还请各自珍重\n"
                                            "------------------------------------------------------------\n\n")
    Title_label.config(font=highlight_font)
    Title_label.pack(side=tk.TOP)
    website_label = tk.Label(frame_pack, text="项目地址：https://github.com/SnowLifeCrescent/OBS-plugin-RS")
    website_label.pack()

    # 确认按钮
    confirm_button = tk.Button(root, text="已了解", command=confirm_command)
    confirm_button.pack(pady=13)
    confirm_button.config(state=tk.DISABLED)
    countdown_time = 0
    countdown_label = tk.Label(root, text="5秒后可点击")
    countdown_label.pack()
    countdown()
    root.mainloop()

    catch = tk.Tk()
    catch.title("window")
    frame_ = tk.Frame(catch)
    frame_.pack(side=tk.TOP)
    Label_0 = tk.Label(frame_, text="\n\n------------------------------------------------------------\n\n"
                                    "接下来将会对电脑屏幕进行一次截图\n\n"
                                    "该截图将作为载体图片混入游戏画面\n\n"
                                    "该截图将用于应付超管\n\n"
                                    "请根据个人喜好调整窗口，截图将在本窗口被关闭后进行"
                                    "\n\n------------------------------------------------------------\n\n")
    Label_0.config(font=highlight_font)
    Label_0.pack()
    catch.mainloop()

    time.sleep(0.6)
    carrier_shot = ImageGrab.grab()

    done = tk.Tk()
    done.title("window")
    done_label = tk.Label(done, text="\n\n------------------------------------------------------------\n\n"
                                     "截图完成\n\n"
                                     "关闭本窗口以继续\n\n"
                                     "------------------------------------------------------------\n\n")
    done_label.config(font=highlight_font)
    done_label.pack(side=tk.TOP)
    done.mainloop()

    return carrier_shot
