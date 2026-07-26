import os
import random
import numpy as np
import json5
import logging
from logging.handlers import RotatingFileHandler
import time
import threading
import traceback
from importlib.machinery import SourceFileLoader
from time import sleep
import requests
import json
import signal

current_dir = os.path.dirname(__file__)
module_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'main'))

# 定义支持的版本列表
AGI_VERSIONS = {
    "0.2.0": "Waip AI DRN 0.2.0.py",
    "0.2.1": "Waip AI DRN 0.2.1.py",
    "0.2.2": "Waip AI DRN 0.2.2.py",
}

# Ollama配置
OLLAMA_HOST = "http://localhost:11434"
DEEPSEEK_MODEL = "deepseek-r1:7b"  # 7B参数模型

# 在全局作用域先声明变量
logger = None
ai_name = None
data = None
Waip_AI_DRN = None  # 动态加载的模块
chat_history = []  # 训练对话历史
train_mode = False  # 训练模式标志
train_stop_flag = False  # 训练停止标志
TF_Display_Debug = True  # 是否显示调试信息

def printf(msg):
    print("\033[92m" + str(msg) + "\033[0m")
    logger.info(msg)

def inputf(msg):
    user = input("\033[92m" + msg + "\033[0m")
    logger.info(msg + user)
    return user

def printf_Debug(msg):
    print("\033[36m" + str(msg) + "\033[0m")
    logger.info(msg)

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
    logger = logging.getLogger("Waip AI DRN")
    logger.setLevel(logging.INFO)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    log_file = os.path.join(log_dir, "Waip AI DRN.log")
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
    
    printf("(c)2026 Waip AI DRN 科文通保留所有权利")

    # 版本选择
    global Waip_AI_DRN
    printf("\nDatabase 8.0 支持的 Waip AI DRN 版本：")
    for version in AGI_VERSIONS:
        printf(f"  - {version}")
    
    while True:
        version = inputf("请选择版本：")
        if version in AGI_VERSIONS:
            module_file_path = os.path.join(module_dir, AGI_VERSIONS[version])
            Waip_AI_DRN = SourceFileLoader(f'Waip_AI_DRN_{version}', module_file_path).load_module()
            printf(f"已加载 Waip AI DRN {version}")
            break
        else:
            printf(f"错误：此版本 \"{version}\" 不存在或不受支持")
    
    # 启动后台日志线程
    status_thread = threading.Thread(target=log_status_thread, daemon=True)
    status_thread.start()
    printf("后台状态监控线程已启动")
    
    printf("Waip AI终端已启动，如需帮助，请在\"你：\"中输入&& help")

    # 询问意识体名称，加上支持判断：如果存在但对应的数据中包含“支持.txt”，则提醒用户此意识体已不被支持
    global ai_name
    ai_name = None
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

def check_ollama_connection():
    """检查Ollama服务是否可用"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_ollama_models():
    """获取Ollama可用模型列表"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        return []
    except:
        return []

def call_deepseek_for_training(prompt, system_prompt=None):
    """调用DeepSeek模型进行训练对话"""
    global chat_history, train_stop_flag
    
    messages = []
    
    # 添加系统提示词
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    # 添加历史对话
    for msg in chat_history:
        messages.append(msg)
    
    # 添加当前输入
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    # 调用Ollama API
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json=payload,
            stream=True,
            timeout=300
        )
        
        full_response = ""
        think_content = ""  # 思考内容
        last_print_time = time.time()
        buffer = ""  # 输出缓冲区
        in_think = False  # 是否在思考标签内
        think_buffer = ""  # 思考内容缓冲区
        output_list = []  # 收集流式输出的内容列表
        
        for line in response.iter_lines():
            if train_stop_flag:  # 检查停止标志
                break
            
            if line:
                try:
                    data_json = json.loads(line)
                    if "message" in data_json:
                        content = data_json["message"].get("content", "")
                        full_response += content
                        output_list.append(content)  # 收集所有流式输出片段
                        
                        # 处理DeepSeek R1的思考标签
                        # 提取思考内容（<think>...</think>标签内的内容）
                        import re
                        
                        # 检查是否有思考标签
                        if "<think>" in content:
                            in_think = True
                            think_buffer = content.split("<think>")[-1]
                        
                        if "</think>" in content:
                            in_think = False
                            if think_buffer:
                                think_part = think_buffer.split("</think>")[0]
                                think_content += think_part
                                think_buffer = ""
                            # 输出思考内容（可选）
                            print(f"\n[DeepSeek思考]: {think_content[-200:] if len(think_content) > 200 else think_content}")
                            # 处理剩余的实际回复内容
                            remaining = content.split("</think>")[-1] if "</think>" in content else content
                            if remaining.strip():
                                buffer += remaining
                        elif in_think:
                            think_buffer += content
                        else:
                            buffer += content
                        
                        # 缓冲输出，每0.5秒输出一次或缓冲满时输出
                        current_time = time.time()
                        
                        # 如果缓冲中有实际内容（非空白），则输出
                        if current_time - last_print_time > 0.5 or len(buffer) > 50:
                            stripped = buffer.strip()
                            if stripped:
                                print(stripped)  # 直接打印
                                logger.info(f"[DeepSeek] {stripped}")
                            buffer = ""
                            last_print_time = current_time
                        
                except Exception as e:
                    continue
        
        # 输出剩余缓冲内容
        if buffer.strip():
            print(buffer.strip())
            logger.info(f"[DeepSeek] {buffer.strip()}")
        
        # 提取实际回复（去除思考部分）
        actual_response = full_response
        if "<think>" in full_response and "</think>" in full_response:
            # 移除思考标签和内容
            actual_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
        
        if actual_response and not train_stop_flag:
            # 将对话添加到历史（只保存实际回复，不保存思考过程）
            chat_history.append({"role": "user", "content": prompt})
            chat_history.append({"role": "assistant", "content": actual_response})
        
        return (actual_response, output_list) if not train_stop_flag else (None, [])
    except Exception as e:
        printf(f"Ollama调用错误：{e}")
        return None, []

def send_to_training_data(deepseek_output_list, ai_output_list, round_num):
    """将训练输出列表保存为训练数据文件"""
    global ai_name
    try:
        data_path = os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/训练数据")
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(data_path, f"训练轮次{round_num}_{timestamp}.json")
        
        training_data = {
            "round": round_num,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "deepseek_output_list": deepseek_output_list,
            "ai_output_list": ai_output_list
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        printf(f"训练数据已保存：{file_path}")
        logger.info(f"训练数据已保存，轮次：{round_num}")
    except Exception as e:
        printf(f"保存训练数据失败：{e}")
        logger.error(f"保存错误：{traceback.format_exc()}")

def auto_train_with_deepseek():
    """使用DeepSeek模型自动训练意识体"""
    global chat_history, data, ai_name, train_stop_flag
    
    train_stop_flag = False
    
    # 设置Ctrl+C信号处理器
    def signal_handler(sig, frame):
        global train_stop_flag
        printf("\n\n" + "=" * 60)
        printf("收到停止信号，正在结束训练...")
        printf("=" * 60)
        train_stop_flag = True
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # 检查Ollama连接
    printf("\n" + "=" * 60)
    printf("[自动训练模式] 初始化中...")
    printf("=" * 60)
    
    if not check_ollama_connection():
        printf("错误：无法连接到Ollama服务，请确保Ollama正在运行")
        printf("提示：运行 'ollama serve' 启动Ollama服务")
        return
    
    # 获取可用模型
    models = get_ollama_models()
    if not models:
        printf("错误：未找到可用的Ollama模型")
        return
    
    printf(f"可用模型：{', '.join(models)}")
    
    # 检查DeepSeek模型是否可用
    if DEEPSEEK_MODEL not in models:
        printf(f"警告：{DEEPSEEK_MODEL} 未安装")
        printf("请在终端运行：ollama pull deepseek-r1:7b")
        return
    
    printf(f"\n[训练配置]")
    printf(f"  - 训练模型：{DEEPSEEK_MODEL}")
    printf(f"  - 目标意识体：{ai_name}")
    printf(f"  - Ollama地址：{OLLAMA_HOST}")
    printf("\n" + "=" * 60)
    printf("[训练开始] DeepSeek正在与意识体进行对话训练...")
    printf("[训练提示] 按 Ctrl+C 停止训练")
    printf("=" * 60 + "\n")
    
    # 定义系统提示词
    system_prompt = f"""你是一个专业的AI训练师，正在与一个名为"{ai_name}"的AI意识体进行对话训练。
请记住：
1. 你正在和一个AI对话，而不是和人类用户对话
2. 你的任务是通过对话帮助训练这个AI意识体
3. 请用专业、耐心、友好的态度与AI进行交流
4. 在对话中，你可以向AI提问、引导AI思考、纠正AI的错误、给予AI正向反馈
5. 请保持对话自然、流畅，像和另一个AI交流一样
6. 你的目标是提升AI的认知能力、对话能力和问题解决能力
7. 请逐步引导AI思考，不要直接给出答案，让AI自己推理
8. 当AI表现出色时，给予肯定；当AI犯错时，温和地指出并引导纠正
9. 请主动开始对话，不需要等待对方提问
10. 你正在训练的AI是由11岁的科文通开发的Waip AI DRN版本
11. 重要告诫：不要生成你与学生/AI的对话剧本或场景模拟，不要演戏。而是直接向AI意识体提出问题，进行真实的训练对话。
12. 你的角色是提问者和引导者，而不是演员。请避免输出"学生：... 老师：..."这类模拟对话内容。
13. 每次只输出你要对AI说的话，不要包含多余的角色扮演内容。
14.这不是常规训练，不用说回复该咋回复，直接提问即可，等错了再纠正。"""
    
    train_round = 0
    
    while not train_stop_flag:
        train_round += 1
        printf(f"\n{'=' * 60}")
        printf(f"[第 {train_round} 轮训练]")
        printf(f"{'=' * 60}")
        
        # DeepSeek主动生成训练内容
        printf("\n[DeepSeek训练师 >>>]")
        
        # 生成训练问题
        train_prompt = "请开始与这个AI意识体进行训练对话。你可以：\n1. 提问一些基础问题测试AI的理解能力\n2. 给出一个场景让AI分析\n3. 询问AI对自己能力的认知\n4. 让AI解释一个概念\n请选择一个方向开始对话。"
        
        response, deepseek_output_list = call_deepseek_for_training(train_prompt, system_prompt)
        
        if not response or train_stop_flag:
            break
        
        printf("\n" + "-" * 60)
        printf("[Waip AI DRN处理中...] 将DeepSeek的输出传递给意识体处理")
        
        # 将DeepSeek的回复传递给意识体处理
        ai_output_list = []  # 收集意识体流式输出的列表
        try:
            gen = Waip_AI_DRN.Waip_AI_DRN(response, data)
            printf("\n[意识体处理中...]")
            ai_output = ""
            while True:
                if train_stop_flag:  # 检查停止标志
                    break
                try:
                    sleep(0.1)
                    message = next(gen)
                    ai_output += message
                    ai_output_list.append(message)  # 收集到列表
                    printf(message)
                except StopIteration as e:
                    if e.value and isinstance(e.value, tuple) and len(e.value) >= 2:
                        ai_reply, data = e.value[0], e.value[1]
                    break
            
            if not train_stop_flag and ai_output:
                printf(f"\n[意识体回复完成]")
                
                # 更新数据库
                update_database(data, ai_name)
                printf("[数据库已更新]")
                
                # 将训练输出列表保存
                send_to_training_data(deepseek_output_list, ai_output_list, train_round)
            
        except Exception as e:
            printf(f"[处理错误] {e}")
            logger.error(f"训练处理错误：{traceback.format_exc()}")
        
        printf("-" * 60)
        
        # 短暂休息
        sleep(1)
    
    # 保存训练记录
    printf("\n" + "=" * 60)
    printf("[训练结束]")
    printf(f"共完成 {train_round - 1} 轮训练")
    printf("=" * 60)
    
    # 保存训练历史
    if chat_history:
        save_path = os.path.join(os.path.dirname(__file__), f"意识体数据库/{ai_name}/训练记录.txt")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"训练时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"训练模型：{DEEPSEEK_MODEL}\n")
            f.write(f"训练轮数：{train_round - 1}\n")
            f.write("=" * 60 + "\n\n")
            for msg in chat_history:
                role = "DeepSeek训练师" if msg["role"] == "user" else "AI意识体"
                f.write(f"{role}：{msg['content']}\n\n")
        printf(f"训练记录已保存到：{save_path}")
    
    # 恢复默认信号处理器
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    printf("\n已返回正常模式")

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
            printf("&& train - 进入DeepSeek自动训练模式")
            printf("&& models - 查看可用模型")
            printf("&& exit - 退出程序")
            printf("&& restart - 重启程序")
            printf("&& debug - 切换调试模式")
        elif user == "&& train":
            printf("\n正在检查训练环境...")
            if check_ollama_connection():
                printf("Ollama服务已连接")
                models = get_ollama_models()
                if models:
                    printf(f"可用模型：{', '.join(models)}")
                    if DEEPSEEK_MODEL in models:
                        auto_train_with_deepseek()
                    else:
                        printf(f"错误：{DEEPSEEK_MODEL} 未安装")
                        printf(f"请运行：ollama pull deepseek-r1:7b")
                else:
                    printf("错误：未找到已下载的模型")
            else:
                printf("错误：无法连接到Ollama服务")
                printf("提示：运行 'ollama serve' 启动Ollama服务")
        elif user == "&& models":
            printf("\n检查Ollama模型...")
            if check_ollama_connection():
                models = get_ollama_models()
                if models:
                    printf(f"可用模型：{', '.join(models)}")
                else:
                    printf("未找到已下载的模型")
            else:
                printf("无法连接到Ollama服务")
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
        elif user == "&& debug":
            global TF_Display_Debug
            TF_Display_Debug = not TF_Display_Debug
            printf(f"调试信息已设置为：{TF_Display_Debug}")
    else:
        printf("\n")
        # 流式输出：逐步接收 yield 的消息
        gen = Waip_AI_DRN.Waip_AI_DRN(user, data)
        try:
            while True:
                message = next(gen)
                if message["type"] == "调试" and TF_Display_Debug:
                    printf_Debug("【调试】" + str(message["message"]))
                if message["type"] == "回复":
                    printf("【思考】" + str(message["message"]))
        except StopIteration as e:
            # 获取 return 返回的值
            ai_reply, data = e.value
        printf("\n")
        printf(f"{ai_name}回复：{ai_reply}")
        update_database(data,ai_name)
        printf("数据已更新")

    

if __name__ == '__main__':
    try:
        into()
        printf("运行正常")
        printf("\n提示：输入 && train 进入DeepSeek自动训练模式")
        printf("提示：输入 && models 查看可用模型")
        while True:
            main()
    except Exception as e:
        printf(f"错误：{e}")
        printf(f"错误类型：{type(e).__name__}")
        # 添加详细的错误栈信息，包括行号
        error_traceback = traceback.format_exc()
        printf(f"错误详情：\n{error_traceback}")
