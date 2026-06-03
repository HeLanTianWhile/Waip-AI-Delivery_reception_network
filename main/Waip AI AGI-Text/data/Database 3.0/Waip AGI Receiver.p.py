import os
# import random # 你为什么导入了random模块
import numpy as np
import json5
import logging
from logging.handlers import RotatingFileHandler
import time
import threading
import traceback  # 添加 traceback 模块
from importlib.machinery import SourceFileLoader

current_dir = os.path.dirname(__file__)
module_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'main'))
module_file_path = os.path.join(module_dir, 'Waip AGI 0.0.3.py')

Waip_AGI_0_0_3 = SourceFileLoader('Waip_AGI_0_0_3', module_file_path).load_module()

# 在全局作用域先声明变量
logger = None
ai_name = None
data = None

def printf(msg):
    print("\033[92m" + str(msg) + "\033[0m")
    logger.info(msg)

def inputf(msg):
    user = input("\033[92m" + msg + "\033[0m")
    logger.info(msg + user)
    return user

def os_data(path):
    return json5.load(open(os.path.join(os.path.dirname(__file__), path), "r", encoding="utf-8"))

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
    """后台线程，记录程序状态（不干扰用户输入）"""
    import threading
    
    def safe_printf(msg):
        """安全的输出函数，避免干扰用户输入"""
        # 只在没有用户输入时输出
        if not threading.current_thread().name == "MainThread":
            logger.info(msg)
            # 不在控制台输出，避免干扰用户输入
    
    while True:
        time.sleep(60)  # 等待60秒
        safe_printf("程序运行正常")


def into():
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(__file__), 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志
    global logger
    logger = logging.getLogger("Waip AGI 0.0.1")
    logger.setLevel(logging.INFO)
    
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
    # console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.info(f"意识体已启动，以下为输出内容：")
    
    # 启动后台日志线程
    status_thread = threading.Thread(target=log_status_thread, daemon=True)
    status_thread.start()
    printf("后台状态监控线程已启动")
    
    printf("Waip AI终端已启动，如需帮助，请在\"你：\"中输入&& help")

    # 询问意识体名称，加上支持判断：如果存在但对应的数据中包含“支持.txt”，则提醒用户此意识体已不被支持
    global ai_name
    while str(ai_name) not in os_library("意识体数据库") or "支持.txt" in os_library(f"意识体数据库/{ai_name}"):
        if ai_name != None:
            printf("此意识体已不被支持或不存在，请重新输入意识体名称")
        ai_name = inputf("请输入意识体名称：")

    # 加载数据
    global data
    data = {
        "short-term memory": {},
        "long-term memory": {},
        "associative network": {},
        "cognitive database": {},
        "activated memory": {},
        "status database": {}
    }
    printf("数据结构已初始化")

    # 加载短期记忆数据库
    data["short-term memory"] = os_data(f"意识体数据库/{ai_name}/短期记忆数据库.txt")
    printf("短期记忆已加载")

    # 加载长期记忆数据库
    data["long-term memory"] = os_data(f"意识体数据库/{ai_name}/长期记忆数据库.txt")
    printf("长期记忆已加载")

    # 加载联想知识网络数据库
    data["associative network"] = os_data(f"意识体数据库/{ai_name}/联想知识网络.txt")
    printf("联想知识网络已加载")

    # 加载认知数据库
    data["cognitive database"] = os_data(f"意识体数据库/{ai_name}/认知数据库.txt")
    printf("认知数据库已加载")

    # 加载已激活记忆数据库
    data["activated memory"] = os_data(f"意识体数据库/{ai_name}/已激活记忆.txt")
    printf("已激活记忆数据库已加载")

    # 加载意识体配置文件
    data["status database"] = os_data(f"意识体数据库/{ai_name}/状态数据库.txt")
    printf("状态数据库已加载")

def update_database(data,ai_name):
    # 更新数据库
    with open(os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/短期记忆数据库.txt"), "w", encoding="utf-8") as f:
        f.write(json5.dumps(data["short-term memory"], ensure_ascii=False, indent=4))
    with open(os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/长期记忆数据库.txt"), "w", encoding="utf-8") as f:
        f.write(json5.dumps(data["long-term memory"], ensure_ascii=False, indent=4))
    with open(os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/联想知识网络.txt"), "w", encoding="utf-8") as f:
        f.write(json5.dumps(data["associative network"], ensure_ascii=False, indent=4))
    with open(os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/认知数据库.txt"), "w", encoding="utf-8") as f:
        f.write(json5.dumps(data["cognitive database"], ensure_ascii=False, indent=4))
    with open(os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/已激活记忆.txt"), "w", encoding="utf-8") as f:
        f.write(json5.dumps(data["activated memory"], ensure_ascii=False, indent=4))
    with open(os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/状态数据库.txt"), "w", encoding="utf-8") as f:
        f.write(json5.dumps(data["status database"], ensure_ascii=False, indent=4))

def main():
    # 主处理函数
    # 接收用户输入
    global data
    user = inputf("你：")

    if "&&" in user:
        if user == "&& help":
            printf("帮助菜单：")
            printf("&& help - 显示帮助菜单")
            printf("&& exit - 退出程序")
            printf("&& restart - 重启程序")
        elif user == "&& exit":
            printf("程序已退出")
            exit()
        elif user == "&& restart":
            printf("程序已重启")
            into()
        elif user == "&& create":
            # printf("意识体已创建")
            # create()
            pass
    else:
        printf("\n")
        ai_reply, data, msg = Waip_AGI_0_0_3.Waip_AGI(user, data)
        for message in msg:
            printf(message)
        printf("\n")
        printf(f"{ai_name}回复：{ai_reply}")
        update_database(data,ai_name)
        printf("数据已更新")

    

if __name__ == '__main__':
    try:
        into()
        printf("运行正常")
        while True:
            main()
    except Exception as e:
        printf(f"错误：{e}")
        printf(f"错误类型：{type(e).__name__}")
        # 添加详细的错误栈信息，包括行号
        error_traceback = traceback.format_exc()
        printf(f"错误详情：\n{error_traceback}")
