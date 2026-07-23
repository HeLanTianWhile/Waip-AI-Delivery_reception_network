import sys
import os
import json5
import importlib.util
import threading
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel,
    QTextEdit, QSplitter, QMessageBox, QInputDialog, QFrame,
    QScrollArea, QSizePolicy, QDialog, QFormLayout, QComboBox, QMenu
)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor, QCursor
from PyQt5.QtCore import Qt, QSize, QTimer

def get_dpi_scale():
    screen = QApplication.primaryScreen()
    dpi = screen.logicalDotsPerInch()
    scale = dpi / 96.0
    return min(scale, 1.0)

class CreateAgentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        scale = get_dpi_scale()
        self.setWindowTitle("创建意识体")
        self.setFixedSize(int(300 * scale), int(200 * scale))
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        layout.addRow("意识体名称:", self.name_edit)
        
        self.ok_btn = QPushButton("创建")
        self.ok_btn.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        scale = get_dpi_scale()
        self.setWindowTitle("关于 Waip AI DRN")
        self.setFixedSize(int(400 * scale), int(500 * scale))
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "Waip AI.png")
        if os.path.exists(logo_path):
            logo_size = int(80 * scale)
            logo_pixmap = QPixmap(logo_path).scaled(logo_size, logo_size, Qt.KeepAspectRatio)
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        title_label = QLabel("Waip AI DRN")
        title_label.setStyleSheet(f"font-size: {int(24 * scale)}px; font-weight: bold; color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        version_label = QLabel("版本 5.0")
        version_label.setStyleSheet(f"font-size: {int(14 * scale)}px; color: #7f8c8d;")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        layout.addSpacing(int(20 * scale))
        
        info_text = QLabel("""
            <p style='font-size:14px; color:#34495e;'>
            Waip AI DRN 是一个基于认知科学原理构建的人工智能系统。<br><br>
            核心特性：<br>
            - 神经递质状态系统<br>
            - 关联网络扩散激活<br>
            - 短期/长期记忆机制<br>
            版本：Database 5.0<br>
            支持版本：0.0.7重制版<br>
            开发团队：WarpWhile（部分成员）<br>
            实际参与者：科文通<br>
            邮箱：3992124100@qq.com<br><br>
            (c) 2026 WarpWhile 科文通所有
            </p>
        """)
        info_text.setAlignment(Qt.AlignCenter)
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        close_btn = QPushButton("关闭")
        close_btn.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: {int(5 * scale)}px;
                padding: {int(10 * scale)}px {int(30 * scale)}px;
                font-size: {int(14 * scale)}px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class ChatListWidget(QListWidget):
    def __init__(self, parent_gui):
        super().__init__()
        self.parent_gui = parent_gui
        scale = get_dpi_scale()
        self.setStyleSheet(f"""
            QListWidget {{
                border: none;
                background-color: #f0f0f0;
                font-size: {int(16 * scale)}px;
            }}
            QListWidget::item {{
                padding: {int(15 * scale)}px;
                border-bottom: 1px solid #e0e0e0;
            }}
            QListWidget::item:hover {{
                background-color: #e8e8e8;
            }}
            QListWidget::item:selected {{
                background-color: #4a90d9;
                color: white;
            }}
        """)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        item = self.itemAt(position)
        if not item:
            return
        
        menu = QMenu()
        rename_action = menu.addAction("重命名")
        delete_action = menu.addAction("删除")
        
        action = menu.exec_(self.mapToGlobal(position))
        
        if action == rename_action:
            self.parent_gui.rename_agent(item)
        elif action == delete_action:
            self.parent_gui.delete_agent(item)

class ChatArea(QTextEdit):
    def __init__(self):
        super().__init__()
        scale = get_dpi_scale()
        self.setReadOnly(True)
        self.setFont(QFont("Microsoft YaHei", int(16 * scale)))
        self.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: white;
                padding: {int(15 * scale)}px;
            }}
        """)
    
    def append_thinking(self, text):
        self.append(f"<span style='color: #7f8c8d; font-style: italic;'>[思考] {text}</span>")
    
    def append_response(self, text):
        self.append(f"<span style='color: #2c3e50;'>{text}</span>")

class StopButton(QPushButton):
    def __init__(self, parent_gui):
        super().__init__()
        self.parent_gui = parent_gui
        scale = get_dpi_scale()
        self.setText("●")
        self.setFont(QFont("Microsoft YaHei", int(16 * scale)))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: {int(20 * scale)}px;
                padding: {int(10 * scale)}px;
                font-size: {int(16 * scale)}px;
                min-width: {int(40 * scale)}px;
                min-height: {int(40 * scale)}px;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        self.clicked.connect(self.parent_gui.stop_generation)

class WaipAIGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waip AI DRN")
        
        if getattr(sys, 'frozen', False):
            self.current_dir = os.path.dirname(sys.executable)
        else:
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.agent_db_path = os.path.join(self.current_dir, "意识体")
        self.main_dir = os.path.join(self.current_dir, "main")
        self.sessions_file = os.path.join(self.agent_db_path, "聊天会话.json")
        
        self.is_generating = False
        self.stop_requested = False
        self.current_generator = None
        self.current_agent_name = None
        self.current_thinking_list = []
        self.current_response = ""
        
        logo_path = os.path.join(self.current_dir, "img", "Waip AI.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        
        self.init_sessions_file()
        self.init_ui()
        self.load_agents()
        self.load_drn_files()
    
    def init_sessions_file(self):
        if not os.path.exists(self.agent_db_path):
            os.makedirs(self.agent_db_path)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, "w", encoding="utf-8") as f:
                json5.dump({}, f)
    
    def load_sessions(self):
        try:
            with open(self.sessions_file, "r", encoding="utf-8") as f:
                return json5.load(f)
        except Exception:
            return {}
    
    def save_sessions(self, sessions):
        try:
            with open(self.sessions_file, "w", encoding="utf-8") as f:
                json5.dump(sessions, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存聊天会话失败: {str(e)}")
    
    def init_ui(self):
        scale = get_dpi_scale()
        
        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()
        window_width = int(screen_size.width() * 0.9)
        window_height = int(screen_size.height() * 0.9)
        self.setGeometry(
            int((screen_size.width() - window_width) / 2),
            int((screen_size.height() - window_height) / 2),
            window_width,
            window_height
        )
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_header = QFrame()
        logo_header.setStyleSheet("background-color: #2c3e50;")
        logo_layout = QHBoxLayout(logo_header)
        
        logo_path = os.path.join(self.current_dir, "img", "Waip AI.png")
        if os.path.exists(logo_path):
            logo_size = int(50 * scale)
            logo_pixmap = QPixmap(logo_path).scaled(logo_size, logo_size, Qt.KeepAspectRatio)
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap)
            logo_layout.addWidget(logo_label)
        
        title_label = QLabel("Waip AI DRN")
        title_label.setStyleSheet(f"color: white; font-size: {int(22 * scale)}px; font-weight: bold;")
        logo_layout.addWidget(title_label)
        
        logo_layout.addStretch()
        
        about_btn = QPushButton("关于")
        about_btn.setFont(QFont("Microsoft YaHei", int(12 * scale)))
        about_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                font-size: {int(12 * scale)}px;
                padding: {int(5 * scale)}px {int(10 * scale)}px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: {int(3 * scale)}px;
            }}
        """)
        about_btn.clicked.connect(self.show_about)
        logo_layout.addWidget(about_btn)
        
        logo_header.setFixedHeight(int(60 * scale))
        left_layout.addWidget(logo_header)
        
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: #34495e;")
        search_layout = QHBoxLayout(search_frame)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索意识体...")
        self.search_edit.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        self.search_edit.setStyleSheet(f"""
            QLineEdit {{
                padding: {int(8 * scale)}px;
                border-radius: {int(5 * scale)}px;
                border: none;
                font-size: {int(14 * scale)}px;
            }}
        """)
        self.search_edit.textChanged.connect(self.filter_agents)
        
        add_btn = QPushButton("+")
        add_btn.setFont(QFont("Microsoft YaHei", int(18 * scale), QFont.Bold))
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: {int(5 * scale)}px;
                padding: {int(8 * scale)}px {int(15 * scale)}px;
                font-size: {int(18 * scale)}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        add_btn.clicked.connect(self.show_create_dialog)
        
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(add_btn)
        
        search_frame.setFixedHeight(int(50 * scale))
        left_layout.addWidget(search_frame)
        
        self.chat_list = ChatListWidget(self)
        self.chat_list.itemClicked.connect(self.on_agent_click)
        left_layout.addWidget(self.chat_list)
        
        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 1)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        chat_header = QFrame()
        chat_header.setStyleSheet("background-color: #ecf0f1;")
        chat_header_layout = QHBoxLayout(chat_header)
        
        self.chat_title = QLabel("选择一个意识体开始聊天")
        self.chat_title.setFont(QFont("Microsoft YaHei", int(18 * scale), QFont.Bold))
        self.chat_title.setStyleSheet("color: #2c3e50;")
        chat_header_layout.addWidget(self.chat_title)
        
        chat_header_layout.addStretch()
        
        version_label = QLabel("DRN版本:")
        version_label.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        version_label.setStyleSheet("color: #34495e;")
        chat_header_layout.addWidget(version_label)
        
        self.drn_combo = QComboBox()
        self.drn_combo.setFont(QFont("Microsoft YaHei", int(14 * scale)))
        self.drn_combo.setStyleSheet(f"""
            QComboBox {{
                padding: {int(6 * scale)}px {int(10 * scale)}px;
                border-radius: {int(4 * scale)}px;
                border: 1px solid #bdc3c7;
                font-size: {int(14 * scale)}px;
                min-width: {int(200 * scale)}px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        chat_header_layout.addWidget(self.drn_combo)
        
        chat_header.setFixedHeight(int(55 * scale))
        right_layout.addWidget(chat_header)
        
        self.chat_area = ChatArea()
        right_layout.addWidget(self.chat_area)
        
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #ecf0f1;")
        input_layout = QHBoxLayout(input_frame)
        
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("输入消息...")
        self.input_edit.setFont(QFont("Microsoft YaHei", int(16 * scale)))
        self.input_edit.setStyleSheet(f"""
            QLineEdit {{
                padding: {int(10 * scale)}px;
                border-radius: {int(5 * scale)}px;
                border: 1px solid #bdc3c7;
                font-size: {int(16 * scale)}px;
            }}
        """)
        
        self.send_btn = QPushButton("发送")
        self.send_btn.setFont(QFont("Microsoft YaHei", int(16 * scale)))
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: {int(5 * scale)}px;
                padding: {int(10 * scale)}px {int(25 * scale)}px;
                font-size: {int(16 * scale)}px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        self.send_btn.clicked.connect(self.send_message)
        self.input_edit.returnPressed.connect(self.send_message)
        
        self.stop_btn = StopButton(self)
        self.stop_btn.hide()
        
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.send_btn)
        input_layout.addWidget(self.stop_btn)
        
        input_frame.setFixedHeight(int(60 * scale))
        right_layout.addWidget(input_frame)
        
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(splitter)
    
    def load_agents(self):
        self.chat_list.clear()
        
        if not os.path.exists(self.agent_db_path):
            os.makedirs(self.agent_db_path)
        
        try:
            agents = os.listdir(self.agent_db_path)
            for agent in agents:
                if agent == "支持.txt" or agent == "聊天会话.json":
                    continue
                agent_path = os.path.join(self.agent_db_path, agent)
                if os.path.isdir(agent_path):
                    item = QListWidgetItem(agent)
                    scale = get_dpi_scale()
                    item.setFont(QFont("Microsoft YaHei", int(16 * scale)))
                    self.chat_list.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载意识体列表失败: {str(e)}")
    
    def load_drn_files(self):
        self.drn_combo.clear()
        
        if not os.path.exists(self.main_dir):
            return
        
        try:
            files = os.listdir(self.main_dir)
            drn_files = []
            
            for filename in files:
                if filename.endswith(".py") and "Waip AI DRN" in filename:
                    drn_files.append(filename)
            
            drn_files.sort()
            
            if drn_files:
                for drn_file in drn_files:
                    self.drn_combo.addItem(drn_file)
            else:
                self.drn_combo.addItem("未找到DRN文件")
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载DRN文件列表失败: {str(e)}")
    
    def filter_agents(self, text):
        for i in range(self.chat_list.count()):
            item = self.chat_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
    
    def show_create_dialog(self):
        dialog = CreateAgentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            agent_name = dialog.name_edit.text().strip()
            if agent_name:
                self.create_agent(agent_name)
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def create_agent(self, agent_name):
        agent_path = os.path.join(self.agent_db_path, agent_name)
        
        if os.path.exists(agent_path):
            QMessageBox.warning(self, "错误", "此意识体已存在")
            return
        
        try:
            os.makedirs(agent_path)
            
            template_dir = os.path.join(self.current_dir, "..", "..", "意识体数据库", "测试体3号")
            if os.path.exists(template_dir):
                for item in os.listdir(template_dir):
                    s = os.path.join(template_dir, item)
                    d = os.path.join(agent_path, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
            else:
                default_cognitive_database = {
                    "1": {
                        "content": "你好",
                        "权重": "0",
                        "IP": ["combination", 1]
                    },
                    "2": {
                        "content": "你",
                        "IP": ["basic", 1]
                    },
                    "3": {
                        "content": "好",
                        "IP": ["basic", 2]
                    },
                    "4": {
                        "content": "是",
                        "IP": ["basic", 3]
                    },
                    "5": {
                        "content": "谁",
                        "IP": ["basic", 4]
                    },
                    "6": {
                        "content": "是谁",
                        "权重": "0",
                        "IP": ["combination", 2]
                    },
                    "7": {
                        "content": "你是",
                        "权重": "0",
                        "IP": ["combination", 3]
                    },
                    "8": {
                        "content": "<speak>",
                        "IP": ["<token>", 1]
                    }
                }
                
                default_activated_memory = {
                    "0": {
                        "IP": ["cognitive database", "combination", 1],
                        "权重": 50000
                    },
                    "1": {
                        "IP": ["associative network", "line", "two-way line", 1],
                        "权重": 21760
                    },
                    "2": {
                        "IP": ["short-term memory", "user", 1],
                        "权重": 76456
                    },
                    "3": {
                        "IP": ["short-term memory", "ai", "external actions", 1],
                        "权重": 78121
                    },
                    "4": {
                        "IP": ["cognitive database", "<token>", 1],
                        "权重": 93021
                    },
                    "5": {
                        "IP": ["cognitive database", "basic", 1],
                        "权重": 45093
                    }
                }
                
                default_status_database = {
                    "多巴胺dopamine": 35000,
                    "乙酰胆碱acetylcholine": 25000,
                    "血清素serotonin": 50000,
                    "内啡肽endorphin": 40000,
                    "P物质substance P": 15000,
                    "肾上腺素epinephrine": 20000,
                    "GABA": 30000,
                    "去肾上腺素Noradrenaline": 22000,
                    "谷氨酸Glutamic acid": 25000
                }
                
                default_short_term_memory = {}
                default_long_term_memory = {}
                
                default_associative_network = {
                    "0": {
                        "IP": ["line", "two-way line", 0],
                        "content": [
                            ["cognitive database", "basic", 1],
                            ["cognitive database", "basic", 4]
                        ],
                        "type": "two-way line",
                        "权重": 142
                    },
                    "1": {
                        "IP": ["line", "one-way line", 0],
                        "content": [
                            {
                                "type": "forward head",
                                "IP": ["cognitive database", "combination", 3]
                            },
                            {
                                "type": "reverse head",
                                "IP": ["cognitive database", "combination", 2]
                            }
                        ],
                        "type": "one-way line",
                        "权重": 4863
                    }
                }
                
                files = [
                    ("短期记忆数据库.txt", default_short_term_memory),
                    ("长期记忆数据库.txt", default_long_term_memory),
                    ("联想知识网络.txt", default_associative_network),
                    ("认知数据库.txt", default_cognitive_database),
                    ("已激活记忆.txt", default_activated_memory),
                    ("状态数据库.txt", default_status_database)
                ]
                
                for filename, data in files:
                    with open(os.path.join(agent_path, filename), "w", encoding="utf-8") as f:
                        f.write(json5.dumps(data, ensure_ascii=False, indent=4))
            
            sessions = self.load_sessions()
            sessions[agent_name] = []
            self.save_sessions(sessions)
            
            QMessageBox.information(self, "成功", f"意识体 '{agent_name}' 创建成功")
            self.load_agents()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建意识体失败: {str(e)}")
    
    def rename_agent(self, item):
        old_name = item.text()
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新的意识体名称:", QLineEdit.Normal, old_name)
        
        if ok and new_name.strip():
            new_name = new_name.strip()
            if new_name == old_name:
                return
            
            old_path = os.path.join(self.agent_db_path, old_name)
            new_path = os.path.join(self.agent_db_path, new_name)
            
            if os.path.exists(new_path):
                QMessageBox.warning(self, "错误", "此意识体名称已存在")
                return
            
            try:
                os.rename(old_path, new_path)
                
                sessions = self.load_sessions()
                if old_name in sessions:
                    sessions[new_name] = sessions.pop(old_name)
                    self.save_sessions(sessions)
                
                self.load_agents()
                QMessageBox.information(self, "成功", f"意识体已重命名为 '{new_name}'")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"重命名失败: {str(e)}")
    
    def delete_agent(self, item):
        agent_name = item.text()
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除意识体 '{agent_name}' 吗？\n所有相关数据将被永久删除！",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            agent_path = os.path.join(self.agent_db_path, agent_name)
            
            try:
                shutil.rmtree(agent_path)
                
                sessions = self.load_sessions()
                if agent_name in sessions:
                    del sessions[agent_name]
                    self.save_sessions(sessions)
                
                self.load_agents()
                self.chat_title.setText("选择一个意识体开始聊天")
                self.chat_area.clear()
                QMessageBox.information(self, "成功", f"意识体 '{agent_name}' 已删除")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")
    
    def on_agent_click(self, item):
        agent_name = item.text()
        self.current_agent_name = agent_name
        self.chat_title.setText(f"与 {agent_name} 的对话")
        self.chat_area.clear()
        
        sessions = self.load_sessions()
        if agent_name in sessions and sessions[agent_name]:
            for msg in sessions[agent_name]:
                if msg["type"] == "thinking":
                    self.chat_area.append_thinking(msg["content"])
                elif msg["type"] == "response":
                    self.chat_area.append_response(msg["content"])
                elif msg["type"] == "user":
                    self.chat_area.append(f"你: {msg['content']}")
        else:
            self.chat_area.append(f"已连接到意识体: {agent_name}")
            self.chat_area.append("")
            self.chat_area.append("欢迎使用 Waip AI DRN")
            self.chat_area.append("----------------------")
    
    def send_message(self):
        if self.is_generating:
            return
        
        message = self.input_edit.text().strip()
        if not message:
            return
        
        current_item = self.chat_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个意识体")
            return
        
        drn_file = self.drn_combo.currentText()
        if drn_file == "未找到DRN文件":
            QMessageBox.warning(self, "提示", "请先选择DRN版本")
            return
        
        agent_name = current_item.text()
        self.current_agent_name = agent_name
        self.current_user_message = message
        
        self.chat_area.append(f"你: {message}")
        self.chat_area.append("")
        self.input_edit.clear()
        
        self.current_thinking_list = []
        self.current_response = ""
        
        self.send_btn.hide()
        self.stop_btn.show()
        self.is_generating = True
        self.stop_requested = False
        
        thread = threading.Thread(target=self.run_drn, args=(agent_name, drn_file, message))
        thread.start()
        
        QTimer.singleShot(100, lambda: self.check_generator_output())
    
    def run_drn(self, agent_name, drn_file, message):
        try:
            drn_path = os.path.join(self.main_dir, drn_file)
            agent_path = os.path.join(self.agent_db_path, agent_name)
            
            spec = importlib.util.spec_from_file_location("drn_module", drn_path)
            drn_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(drn_module)
            
            data = {}
            data_files = [
                ("短期记忆数据库.txt", "short-term memory"),
                ("长期记忆数据库.txt", "long-term memory"),
                ("联想知识网络.txt", "associative network"),
                ("认知数据库.txt", "cognitive database"),
                ("已激活记忆.txt", "activated memory"),
                ("状态数据库.txt", "status database")
            ]
            
            for filename, key in data_files:
                file_path = os.path.join(agent_path, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data[key] = json5.load(f)
                else:
                    data[key] = {}
            
            if hasattr(drn_module, 'Waip_AI_DRN'):
                self.current_generator = drn_module.Waip_AI_DRN(message, data)
            else:
                self.current_generator = None
                
        except Exception as e:
            self.current_generator = None
            QTimer.singleShot(0, lambda: self.on_run_error(str(e)))
    
    def check_generator_output(self):
        if not self.is_generating:
            return
        
        if self.stop_requested:
            self.finish_generation(cancelled=True)
            return
        
        if self.current_generator:
            try:
                output = next(self.current_generator)
                
                if isinstance(output, dict):
                    if output.get("type") == "thinking":
                        self.chat_area.append_thinking(output.get("content", ""))
                        self.current_thinking_list.append(output.get("content", ""))
                    elif output.get("type") == "response":
                        self.chat_area.append_response(output.get("content", ""))
                        self.current_response = output.get("content", "")
                    elif output.get("type") == "data":
                        self.updated_data = output.get("data", {})
                else:
                    self.chat_area.append_thinking(str(output))
                    self.current_thinking_list.append(str(output))
                
                QTimer.singleShot(50, lambda: self.check_generator_output())
                
            except StopIteration as e:
                if e.value is not None:
                    try:
                        ai_reply, updated_data = e.value
                        if ai_reply:
                            self.current_response = ai_reply
                            self.chat_area.append_response(ai_reply)
                        if updated_data:
                            self.updated_data = updated_data
                    except ValueError:
                        pass
                self.finish_generation(cancelled=False)
            except Exception as e:
                self.on_run_error(str(e))
        else:
            QTimer.singleShot(100, lambda: self.check_generator_output())
    
    def on_run_error(self, error_msg):
        self.chat_area.append(f"<span style='color: #e74c3c;'>错误: {error_msg}</span>")
        self.finish_generation(cancelled=True)
    
    def stop_generation(self):
        self.stop_requested = True
    
    def finish_generation(self, cancelled=False):
        self.is_generating = False
        self.stop_requested = False
        self.current_generator = None
        
        self.send_btn.show()
        self.stop_btn.hide()
        
        if not cancelled and self.current_agent_name:
            sessions = self.load_sessions()
            if self.current_agent_name not in sessions:
                sessions[self.current_agent_name] = []
            
            if hasattr(self, 'current_user_message') and self.current_user_message:
                sessions[self.current_agent_name].append({
                    "type": "user",
                    "content": self.current_user_message
                })
            
            for thinking in self.current_thinking_list:
                sessions[self.current_agent_name].append({
                    "type": "thinking",
                    "content": thinking
                })
            
            if self.current_response:
                sessions[self.current_agent_name].append({
                    "type": "response",
                    "content": self.current_response
                })
            
            self.save_sessions(sessions)
            
            if hasattr(self, 'updated_data') and self.updated_data:
                self.update_agent_database(self.current_agent_name, self.updated_data)
        
        self.current_user_message = ""
        self.current_thinking_list = []
        self.current_response = ""
        if hasattr(self, 'updated_data'):
            del self.updated_data
    
    def update_agent_database(self, agent_name, data):
        agent_path = os.path.join(self.agent_db_path, agent_name)
        
        data_files = [
            ("短期记忆数据库.txt", "short-term memory"),
            ("长期记忆数据库.txt", "long-term memory"),
            ("联想知识网络.txt", "associative network"),
            ("认知数据库.txt", "cognitive database"),
            ("已激活记忆.txt", "activated memory"),
            ("状态数据库.txt", "status database")
        ]
        
        for filename, key in data_files:
            if key in data:
                file_path = os.path.join(agent_path, filename)
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json5.dump(data[key], f, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"更新 {filename} 失败: {str(e)}")

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#ffffff"))
    app.setPalette(palette)
    
    window = WaipAIGUI()
    window.show()
    
    sys.exit(app.exec_())