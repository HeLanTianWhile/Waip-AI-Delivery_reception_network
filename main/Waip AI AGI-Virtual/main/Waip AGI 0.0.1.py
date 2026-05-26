import os
# import random # 你为什么导入了random模块
import numpy as np
import cv2
import pyaudio
import playsound
import json
import logging
from logging.handlers import RotatingFileHandler
import time
import threading

# 在全局作用域先声明logger变量
logger = None

def printf(msg):
    logger.info(msg)
    print(msg)

def os_data(path):
    return json.load(open(os.path.join(os.path.dirname(__file__), path)))

def os_library(path):
    # 获得文件夹的文件列表
    return os.listdir(os.path.join(os.path.dirname(__file__), path))

def for_super(list, dm):
    @np.vectorize
    def f(x):
        return dm(x)
    x = np.array(list)
    return f(x)

def log_status_thread():
    """后台线程，每分钟记录一次程序状态"""
    while True:
        time.sleep(60)  # 等待60秒
        printf("程序运行正常")


def into():
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(__file__), '../data/Database 1.0/log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志
    global logger
    logger = logging.getLogger("Waip AGI 0.0.1")
    logger.setLevel(logging.DEBUG)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    log_file = os.path.join(log_dir, "Waip AGI 0.0.1.log")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.info(f"意识体已启动，以下为输出内容：")
    
    # 启动后台日志线程
    status_thread = threading.Thread(target=log_status_thread, daemon=True)
    status_thread.start()
    printf("后台状态监控线程已启动")
    data = {
        "short-term memory": {},
        "long-term memory": {},
        "associative network": {},
        "control network": {},
        "activated memory": [],
        "inactive memory": []
    }
    printf("数据结构已初始化")

    short_list = os_library("../data/Database 1.0/短期记忆")
    printf(short_list)
    if len(short_list) != 0:
        short_list = for_super(short_list, lambda x :
            int(x[:-7])
        )
        printf(short_list)
        for i in short_list:
            data["short-term memory"][i] = os_data(f"../data/Database 1.0/短期记忆/{i}.memory")
        printf(data["short-term memory"])
        printf("短期记忆已加载")

    else:
        printf("没有短期记忆文件")

if __name__ == '__main__':
    try:
        into()
        printf("运行正常")
    except Exception as e:
        printf(f"错误：{e}")
        printf(f"错误类型：{type(e).__name__}")
