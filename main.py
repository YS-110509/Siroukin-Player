import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog, colorchooser
import os
import pygame
import time
import threading
import json
from datetime import datetime, timedelta
import random

class SplashScreen:
    """启动画面类，显示GIF图片"""
    def __init__(self, root, gif_path):
        self.root = root
        self.root.title("Ciallo～(∠・ω< )⌒☆ 站娘樱岛琥夏感谢您使用Siroukin播放器！")
        self.root.geometry("1000x700")
        self.root.overrideredirect(False)
        
        # 居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"1000x700+{x}+{y}")
        
        # 加载GIF图片
        try:
            self.splash_image = tk.PhotoImage(file=gif_path)
            # 创建标签显示图片
            self.label = tk.Label(root, image=self.splash_image, bg="black")
            self.label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"无法加载启动图片: {e}")
            # 如果图片加载失败，显示默认文本
            self.label = tk.Label(root, text="Siroukin播放器", font=("Arial", 24), bg="black", fg="white")
            self.label.pack(fill=tk.BOTH, expand=True)
        
        # _秒后关闭启动画面
        self.root.after(1000, self.close)
    
    def close(self):
        self.root.destroy()
        
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("白忻制作 ver1.0.0 支持格式.mp3 .flac .ogg 感谢您的使用！")
        self.root.geometry("1000x700")
        self.root.overrideredirect(False)

        # 居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"1000x700+{x}+{y}")

        # 配色方案
        self.colors = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "control_bg": "#2d2d2d",
                "list_bg": "#333333",
                "highlight": "#4CAF50",
                "text": "#aaaaaa",
                "button": "#333",
                "progress": "#4CAF50"
            },
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "control_bg": "#e0e0e0",
                "list_bg": "#ffffff",
                "highlight": "#2196F3",
                "text": "#555555",
                "button": "#e0e0e0",
                "progress": "#2196F3"
            },
            "custom": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "control_bg": "#2d2d2d",
                "list_bg": "#333333",
                "highlight": "#4CAF50",
                "text": "#aaaaaa",
                "button": "#333",
                "progress": "#4CAF50"
            },
            # 二次元角色主题
            "rikka": {
                "bg": "#1a0a2e",
                "fg": "#e0d6eb",
                "control_bg": "#3c1361",
                "list_bg": "#52307c",
                "highlight": "#b491c8",
                "text": "#c5b3d6",
                "button": "#52307c",
                "progress": "#ff6ad5"
            },
            "marin": {
                "bg": "#fff0f5",
                "fg": "#e75480",
                "control_bg": "#ffd1dc",
                "list_bg": "#ffe4e1",
                "highlight": "#ff69b4",
                "text": "#f08080",
                "button": "#ffb6c1",
                "progress": "#ff1493"
            },
            "rem": {
                "bg": "#e6f7ff",
                "fg": "#4169e1",
                "control_bg": "#b0e0e6",
                "list_bg": "#d1e8e2",
                "highlight": "#87cefa",
                "text": "#4682b4",
                "button": "#add8e6",
                "progress": "#1e90ff"
            },
            "elaina": {
                "bg": "#fffaf0",
                "fg": "#52307c",
                "control_bg": "#f5f5dc",
                "list_bg": "#D4E0F0",
                "highlight": "#d2b48c",
                "text": "#52307c",
                "button": "#deb887",
                "progress": "#a89fcc"
            },
            "kuroneko": {
                "bg": "#0a0a0a",
                "fg": "#e6e6fa",
                "control_bg": "#2a2a2a",
                "list_bg": "#363636",
                "highlight": "#9370db",
                "text": "#a9a9a9",
                "button": "#4b0082",
                "progress": "#ba55d3"
            },
            "chitanda": {
                "bg": "#f0f8ff",
                "fg": "#2e8b57",
                "control_bg": "#e0ffff",
                "list_bg": "#afeeee",
                "highlight": "#20b2aa",
                "text": "#3cb371",
                "button": "#7fffd4",
                "progress": "#00fa9a"
            },
            "hitagi": {
                "bg": "#f8f8ff",
                "fg": "#b22222",
                "control_bg": "#ffe4e1",
                "list_bg": "#ffebee",
                "highlight": "#ff4500",
                "text": "#cd5c5c",
                "button": "#ffb6c1",
                "progress": "#dc143c"
            },
            "2b": {
                "bg": "#0a0c10",
                "fg": "#e0e7ff",
                "control_bg": "#1e2329",
                "list_bg": "#2a313a",
                "highlight": "#4fc3ff",
                "text": "#8a9ba8",
                "button": "#3a4552",
                "progress": "#8a9ba8"
            },
            "jingyuan": {
                "bg": "#f8f4e8",
                "fg": "#5a4a3a",
                "control_bg": "#fff9e6",
                "list_bg": "#fff2cc",
                "highlight": "#c91f37",
                "text": "#b8860b",
                "button": "#e6c88c",
                "progress": "#d4a017"
            },
            "mai": {
                "bg": "#f5f0fa",
                "fg": "#4a3c5c",
                "control_bg": "#f0e8ff",
                "list_bg": "#e8e0f5",
                "highlight": "#e75480",
                "text": "#9c89b8",
                "button": "#d4c2e8",
                "progress": "#c5b3d6"
            },
        }

        # 获取脚本所在目录
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 当前主题
        self.theme = "dark"
        self.current_colors = self.colors[self.theme]
        
        # 初始化pygame mixer
        pygame.mixer.init()
        
        # 初始化变量
        self.playlist = []
        self.current_index = 0
        self.playing = False
        self.paused = False
        self.volume = 0.7
        pygame.mixer.music.set_volume(self.volume)
        self.sleep_timer = None
        self.lyrics = []  # 存储歌词数据 [(时间(秒), 歌词内容)]
        self.current_lyric_index = -1  # 当前歌词索引
        self.lyrics_window = None
        self.play_mode = "sequential"  # sequential, loop, random
        self.subtitle_text = self.generate_subtitle()
        
        # 应用初始主题
        self.root.configure(bg=self.current_colors["bg"])
        
        # 加载设置
        self.load_settings()
        
        # 创建UI
        self.create_widgets()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # 绑定快捷键
        self.root.bind("<space>", lambda e: self.toggle_play())
        self.root.bind("<Left>", lambda e: self.prev_song())
        self.root.bind("<Right>", lambda e: self.next_song())
        self.root.bind("p", lambda e: self.toggle_pause())
        self.root.bind("s", lambda e: self.stop_song())
        self.root.bind("+", lambda e: self.increase_volume())
        self.root.bind("-", lambda e: self.decrease_volume())
        self.root.bind("l", lambda e: self.show_lyrics_window())  # L键打开歌词窗口
    
    def generate_subtitle(self):
        """生成与当前主题对应的副标题"""
        theme_subtitles = {
            "rikka": "爆裂吧现实！粉碎吧精神！邪王真眼是最强的！",
            "marin": "今天也要用120%的热情享受音乐！Cosplay开始！",
            "rem": "无论重来多少次，都会选择这首歌。因为...是雷姆选的",
            "elaina": "灰之魔女的音乐之旅~在旋律中遇见另一个自己",
            "kuroneko": "夜之眷属的暗夜奏鸣曲...凡人，沉醉其中吧",
            "chitanda": "わくわく！这首曲子...我很好奇！",
            "hitagi": "用音符编织的陷阱...你已无处可逃",
            "2b": "音乐是机械生命体最后的救赎",
            "jingyuan": "“煌煌威灵，尊吾敕命，斩无赦”",
            "mai": "「君のことが好きだ。好き以外の何者でもない」",
        }
        
        # 如果当前主题有对应的副标题，则使用它
        if self.theme in theme_subtitles:
            return theme_subtitles[self.theme]
        
        # 默认随机副标题
        music_quotes = [
            "音乐是灵魂的语言",
            "音乐是唯一的世界语",
            "音乐是人类的通用语言",
            "音乐是医治思想疾病的良药"
        ]
        
        anime_recommendations = [
            "推荐番剧：《轻音少女》 - 音乐与友情的青春故事",
            "推荐番剧：《四月是你的谎言》 - 钢琴与小提琴的动人旋律 穿越10年的爱恋",
            "推荐番剧：《吹响吧！上低音号》 - 吹奏乐部的青春奋斗",
            "推荐番剧：《卡罗尔与星期二》 - 火星上的音乐梦想",
            "推荐番剧：《坂道上的阿波罗》 - 爵士乐与青春的故事"
        ]
        
        return random.choice(music_quotes + anime_recommendations)
    
    def load_settings(self):
        # 尝试从文件加载设置
        try:
            if os.path.exists("player_settings.json"):
                with open("player_settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.theme = settings.get("theme", "dark")
                    self.playlist = settings.get("playlist", [])
                    self.play_mode = settings.get("play_mode", "sequential")
                    
                    # 加载自定义配色
                    if "custom_colors" in settings:
                        self.colors["custom"] = settings["custom_colors"]
                    
                    # 应用主题
                    self.current_colors = self.colors[self.theme]
                    self.root.configure(bg=self.current_colors["bg"])
        except Exception as e:
            print(f"加载设置错误: {e}")
    
    def save_settings(self):
        # 保存设置到文件
        settings = {
            "theme": self.theme,
            "playlist": self.playlist,
            "play_mode": self.play_mode,
            "custom_colors": self.colors["custom"]
        }
        try:
            with open("player_settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存设置错误: {e}")
    
    def create_widgets(self):
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=self.current_colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 标题栏
        title_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 主标题 (保存为实例变量)
        self.title_label = tk.Label(
            title_frame, 
            text="Siroukin播放器", 
            font=("Arial", 24, "bold"),
            fg=self.current_colors["highlight"],
            bg=self.current_colors["bg"]
        )
        self.title_label.pack(side=tk.LEFT)
        
        # 副标题 (保存为实例变量)
        
        self.subtitle_label = tk.Label(
            title_frame, 
            text=self.subtitle_text, 
            font=("Arial", 10, "italic"),
            fg=self.current_colors["text"],
            bg=self.current_colors["bg"]
        )
        self.subtitle_label.pack(side=tk.LEFT, padx=10)
        
        # 设置按钮
        self.settings_btn = tk.Button(
            title_frame, text="⚙️", font=("Arial", 14),
            command=self.open_settings, 
            bg=self.current_colors["button"], 
            fg=self.current_colors["fg"], 
            relief=tk.FLAT
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=5)
        
        # 歌词按钮
        self.lyrics_btn = tk.Button(
            title_frame, text="📝", font=("Arial", 14),
            command=self.show_lyrics_window, 
            bg=self.current_colors["button"], 
            fg=self.current_colors["fg"], 
            relief=tk.FLAT
        )
        self.lyrics_btn.pack(side=tk.RIGHT, padx=5)
        
        # 睡眠定时器按钮
        self.sleep_btn = tk.Button(
            title_frame, text="⏱️", font=("Arial", 14),
            command=self.set_sleep_timer, 
            bg=self.current_colors["button"], 
            fg=self.current_colors["fg"], 
            relief=tk.FLAT
        )
        self.sleep_btn.pack(side=tk.RIGHT, padx=5)
        
        # 创建控制面板
        control_frame = tk.Frame(main_frame, bg=self.current_colors["control_bg"], bd=2, relief=tk.RIDGE)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 控制按钮框架
        btn_frame = tk.Frame(control_frame, bg=self.current_colors["control_bg"])
        btn_frame.pack(pady=10)
        
        # 控制按钮 (全部保存为实例变量)
        self.prev_btn = tk.Button(
            btn_frame, text="⏮", font=("Arial", 16), width=3, 
            command=self.prev_song, 
            bg=self.current_colors["button"], 
            fg=self.current_colors["fg"], 
            relief=tk.FLAT
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_btn = tk.Button(
            btn_frame, text="▶", font=("Arial", 16), width=3, 
            command=self.toggle_play, 
            bg=self.current_colors["highlight"], 
            fg="white", 
            relief=tk.FLAT
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(
            btn_frame, text="⏸", font=("Arial", 16), width=3, 
            command=self.toggle_pause, 
            bg="#FFC107", 
            fg="black", 
            relief=tk.FLAT
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            btn_frame, text="⏹", font=("Arial", 16), width=3, 
            command=self.stop_song, 
            bg="#F44336", 
            fg="white", 
            relief=tk.FLAT
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(
            btn_frame, text="⏭", font=("Arial", 16), width=3, 
            command=self.next_song, 
            bg=self.current_colors["button"], 
            fg=self.current_colors["fg"], 
            relief=tk.FLAT
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # 播放模式选择框架 (保存为实例变量)
        self.mode_frame = tk.Frame(btn_frame, bg=self.current_colors["control_bg"])
        self.mode_frame.pack(side=tk.LEFT, padx=10)
        
        # 播放模式标签 (保存为实例变量)
        self.mode_label = tk.Label(
            self.mode_frame, text="播放模式:", 
            font=("Arial", 10), 
            fg=self.current_colors["text"], 
            bg=self.current_colors["control_bg"]
        )
        self.mode_label.pack(side=tk.LEFT)
        
        # 播放模式单选按钮 (保存到列表)
        self.mode_var = tk.StringVar(value=self.play_mode)
        modes = [("顺序播放", "sequential"), ("单曲循环", "loop"), ("随机播放", "random")]
        self.mode_buttons = []
        
        for text, mode in modes:
            btn = tk.Radiobutton(
                self.mode_frame, 
                text=text, 
                variable=self.mode_var, 
                value=mode,
                command=self.change_play_mode,
                bg=self.current_colors["control_bg"], 
                fg=self.current_colors["fg"], 
                selectcolor="#333"  # 选中状态颜色
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.mode_buttons.append(btn)
        
        # 进度条框架
        progress_frame = tk.Frame(control_frame, bg=self.current_colors["control_bg"])
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 时间标签 (保存为实例变量)
        self.time_label = tk.Label(
            progress_frame, 
            text="00:00 / 00:00", 
            font=("Arial", 10), 
            fg=self.current_colors["text"], 
            bg=self.current_colors["control_bg"]
        )
        self.time_label.pack(anchor=tk.W)
        
        # 可拖动进度条 (保存为实例变量)
        self.progress = ttk.Scale(
            progress_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL,
            command=self.on_progress_drag, 
            length=500
        )
        self.progress.pack(fill=tk.X, pady=5)
        self.progress.set(0)
        
        # 音量控制框架
        volume_frame = tk.Frame(control_frame, bg=self.current_colors["control_bg"])
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 音量标签 (保存为实例变量)
        self.volume_label = tk.Label(
            volume_frame, 
            text="音量:", 
            font=("Arial", 10), 
            fg=self.current_colors["text"], 
            bg=self.current_colors["control_bg"]
        )
        self.volume_label.pack(side=tk.LEFT)
        
        # 音量条 (保存为实例变量)
        self.volume_scale = ttk.Scale(
            volume_frame, 
            from_=0, 
            to=1, 
            orient=tk.HORIZONTAL,
            command=self.set_volume, 
            length=100, 
            value=self.volume
        )
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        
        # 当前播放标签 (保存为实例变量)
        self.current_song_label = tk.Label(
            control_frame, 
            text="当前播放: 无", 
            font=("Arial", 10), 
            fg=self.current_colors["highlight"], 
            bg=self.current_colors["control_bg"], 
            anchor=tk.W
        )
        self.current_song_label.pack(fill=tk.X, padx=10, pady=5)
        
        # 按钮框架（移到主内容区域上方）
        button_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 功能按钮 (全部保存为实例变量)
        self.add_btn = tk.Button(
            button_frame, 
            text="添加音乐", 
            command=self.add_music, 
            bg="#2196F3", 
            fg="white", 
            relief=tk.FLAT
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_add_btn = tk.Button(
            button_frame, 
            text="自动搜索", 
            command=self.auto_add_music, 
            bg="#9C27B0", 
            fg="white", 
            relief=tk.FLAT
        )
        self.auto_add_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_btn = tk.Button(
            button_frame, 
            text="移除选中", 
            command=self.remove_selected, 
            bg="#F44336", 
            fg="white", 
            relief=tk.FLAT
        )
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame, 
            text="清空列表", 
            command=self.clear_playlist, 
            bg="#FF9800", 
            fg="white", 
            relief=tk.FLAT
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态栏 (保存为实例变量)
        self.status_bar = tk.Label(
            self.root, 
            text="就绪", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg=self.current_colors["control_bg"], 
            fg=self.current_colors["text"], 
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 主内容区域（播放列表和歌词）
        content_frame = tk.Frame(main_frame, bg=self.current_colors["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 分割窗口（左侧播放列表，右侧歌词）
        self.paned_window = tk.PanedWindow(
            content_frame, 
            orient=tk.HORIZONTAL, 
            bg=self.current_colors["bg"], 
            sashwidth=5
        )
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 播放列表框架
        playlist_frame = tk.LabelFrame(
            self.paned_window, 
            text="播放列表", 
            font=("Arial", 12, "bold"), 
            fg=self.current_colors["highlight"], 
            bg=self.current_colors["control_bg"], 
            relief=tk.RIDGE
        )
        
        # 播放列表和滚动条
        playlist_scroll_frame = tk.Frame(playlist_frame, bg=self.current_colors["control_bg"])
        playlist_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 垂直滚动条
        scrollbar_y = tk.Scrollbar(playlist_scroll_frame, orient=tk.VERTICAL)
        
        # 播放列表框 (保存为实例变量)
        self.playlist_box = tk.Listbox(
            playlist_scroll_frame, 
            bg=self.current_colors["list_bg"], 
            fg=self.current_colors["fg"], 
            selectbackground=self.current_colors["highlight"], 
            selectforeground="white",
            font=("Arial", 10), 
            relief=tk.FLAT,
            yscrollcommand=scrollbar_y.set
        )
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar_y.config(command=self.playlist_box.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击播放事件
        self.playlist_box.bind("<Double-Button-1>", self.play_selected)
        
        # 添加已保存的播放列表
        for path in self.playlist:
            self.playlist_box.insert(tk.END, os.path.basename(path))
        
        # 歌词显示区域（右侧）
        lyrics_frame = tk.LabelFrame(
            self.paned_window, 
            text="歌词", 
            font=("Arial", 12, "bold"), 
            fg=self.current_colors["highlight"], 
            bg=self.current_colors["control_bg"], 
            relief=tk.RIDGE
        )
        
        # 歌词显示控件 (保存为实例变量)
        self.lyrics_display = tk.Text(
            lyrics_frame, 
            wrap=tk.WORD, 
            bg=self.current_colors["list_bg"], 
            fg=self.current_colors["fg"],
            font=("Arial", 12),
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.lyrics_display.pack(fill=tk.BOTH, expand=True)
        
        # 添加框架到分割窗口
        self.paned_window.add(playlist_frame, minsize=300, stretch="always")
        self.paned_window.add(lyrics_frame, minsize=300, stretch="always")
        
        # 设置窗格属性
        self.paned_window.paneconfig(playlist_frame, stretch="always")
        self.paned_window.paneconfig(lyrics_frame, stretch="always")
        
        # 设置初始分割比例
        self.root.after(100, self.set_paned_position)
        
        # 初始化比例尺样式
        self.update_scale_styles()
        
        # 启动进度更新线程
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()
    
    def set_paned_position(self):
        """设置分割窗口的位置"""
        try:
            # 获取分割窗口的宽度
            total_width = self.paned_window.winfo_width()
            
            # 仅在宽度有效时设置分割条位置
            if total_width > 100:
                # 使用 sash_place 方法设置分割条位置
                self.paned_window.sash_place(0, int(total_width * 0.6), 0)
        except Exception as e:
            print(f"设置分割条位置错误: {e}")
    
    def show_tooltip(self, message):
        """显示悬停提示"""
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)  # 移除窗口边框
        
        # 获取鼠标位置
        x = self.root.winfo_pointerx() + 10
        y = self.root.winfo_pointery() + 10
        
        self.tooltip.geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip,
            text=message,
            bg="#FFFFE0",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            padx=5,
            pady=2
        )
        label.pack()
        
        # 设置短暂延迟后关闭提示
        self.root.after(2000, self.hide_tooltip)
    
    def hide_tooltip(self):
        """隐藏悬停提示"""
        if hasattr(self, 'tooltip') and self.tooltip:
            try:
                self.tooltip.destroy()
            except tk.TclError:
                pass
            self.tooltip = None
    
    def apply_theme(self, theme=None):
        if theme:
            self.theme = theme
            self.current_colors = self.colors[theme]
        
        # 应用主题到所有组件
        self.root.configure(bg=self.current_colors["bg"])
        self.status_bar.configure(bg=self.current_colors["control_bg"], fg=self.current_colors["text"])
        
        # 显式更新播放列表和歌词显示区域
        if hasattr(self, 'playlist_box'):
            self.playlist_box.config(
                bg=self.current_colors["list_bg"], 
                fg=self.current_colors["fg"],
                selectbackground=self.current_colors["highlight"]
            )
        
        if hasattr(self, 'lyrics_display'):
            self.lyrics_display.config(
                bg=self.current_colors["list_bg"], 
                fg=self.current_colors["fg"]
            )
        
        # 更新paned_window的背景色
        if hasattr(self, 'paned_window'):
            self.paned_window.config(bg=self.current_colors["bg"])
        
        # 更新歌词窗口
        if hasattr(self, 'lyrics_window') and self.lyrics_window is not None:
            try:
                if self.lyrics_window.winfo_exists():
                    self.lyrics_window.configure(bg=self.current_colors["bg"])
                    if hasattr(self, 'current_lyric_label'):
                        self.current_lyric_label.config(
                            bg=self.current_colors["bg"], 
                            fg=self.current_colors["highlight"]
                        )
                    if hasattr(self, 'next_lyric_label'):
                        self.next_lyric_label.config(
                            bg=self.current_colors["bg"], 
                            fg=self.current_colors["fg"]
                        )
            except tk.TclError:
                self.lyrics_window = None
        
        # 更新播放模式相关组件
        if hasattr(self, 'mode_frame'):
            self.mode_frame.config(bg=self.current_colors["control_bg"])
        
        if hasattr(self, 'mode_label'):
            self.mode_label.config(
                bg=self.current_colors["control_bg"],
                fg=self.current_colors["text"]
            )
        
        if hasattr(self, 'mode_buttons'):
            for btn in self.mode_buttons:
                btn.config(
                    bg=self.current_colors["control_bg"],
                    fg=self.current_colors["fg"],
                    selectcolor="#333"  # 选中状态颜色
                )
        
        # 更新控制面板框架
        if hasattr(self, 'control_frame'):
            self.control_frame.config(bg=self.current_colors["control_bg"])
        
        # 更新按钮框架
        if hasattr(self, 'btn_frame'):
            self.btn_frame.config(bg=self.current_colors["control_bg"])
        
        # 更新控制按钮
        if hasattr(self, 'prev_btn'):
            self.prev_btn.config(
                bg=self.current_colors["button"],
                fg=self.current_colors["fg"]
            )
        
        if hasattr(self, 'play_btn'):
            self.play_btn.config(
                bg=self.current_colors["highlight"],
                fg="white"
            )
        
        if hasattr(self, 'pause_btn'):
            self.pause_btn.config(
                bg="#FFC107",
                fg="black"
            )
        
        if hasattr(self, 'stop_btn'):
            self.stop_btn.config(
                bg="#F44336",
                fg="white"
            )
        
        if hasattr(self, 'next_btn'):
            self.next_btn.config(
                bg=self.current_colors["button"],
                fg=self.current_colors["fg"]
            )
        
        # 更新功能按钮
        if hasattr(self, 'add_btn'):
            self.add_btn.config(
                bg="#2196F3",
                fg="white"
            )
        
        if hasattr(self, 'auto_add_btn'):
            self.auto_add_btn.config(
                bg="#9C27B0",
                fg="white"
            )
        
        if hasattr(self, 'remove_btn'):
            self.remove_btn.config(
                bg="#F44336",
                fg="white"
            )
        
        if hasattr(self, 'clear_btn'):
            self.clear_btn.config(
                bg="#FF9800",
                fg="white"
            )
        
        # 更新标题栏按钮
        if hasattr(self, 'settings_btn'):
            self.settings_btn.config(
                bg=self.current_colors["button"],
                fg=self.current_colors["fg"]
            )
        
        if hasattr(self, 'lyrics_btn'):
            self.lyrics_btn.config(
                bg=self.current_colors["button"],
                fg=self.current_colors["fg"]
            )
        
        if hasattr(self, 'sleep_btn'):
            self.sleep_btn.config(
                bg=self.current_colors["button"],
                fg=self.current_colors["fg"]
            )
        
        # 更新主标题 - 添加显式配置
        if hasattr(self, 'title_label'):
            self.title_label.config(
                fg=self.current_colors["highlight"],
                bg=self.current_colors["bg"]
            )
        
        # 更新副标题
        self.subtitle_text = self.generate_subtitle()
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.config(
                text=self.subtitle_text,
                fg=self.current_colors["text"],
                bg=self.current_colors["bg"]
            )
        
        # 更新当前播放标签
        if hasattr(self, 'current_song_label'):
            self.current_song_label.config(
                fg=self.current_colors["highlight"],
                bg=self.current_colors["control_bg"]
            )
        
        # 更新时间标签
        if hasattr(self, 'time_label'):
            self.time_label.config(
                fg=self.current_colors["text"],
                bg=self.current_colors["control_bg"]
            )
        
        # 更新音量标签
        if hasattr(self, 'volume_label'):
            self.volume_label.config(
                fg=self.current_colors["text"],
                bg=self.current_colors["control_bg"]
            )

        # 更新比例尺样式
        self.update_scale_styles()
        
        # 递归更新所有子组件
        self.update_theme_recursive(self.root)

    def update_theme_recursive(self, widget):
        # 跳过已经单独处理的主标题和副标题
        if widget == self.title_label or widget == self.subtitle_label:
            return
        
        # 更新当前组件
        if isinstance(widget, tk.PanedWindow):
            widget.configure(bg=self.current_colors["bg"])
        elif isinstance(widget, tk.Frame):
            widget.configure(bg=self.current_colors["bg"])
        elif isinstance(widget, tk.Label):
            # 主标题特殊处理（防止被覆盖）
            if widget == self.title_label:
                widget.configure(fg=self.current_colors["highlight"])
            elif widget.cget("text") == self.subtitle_text:  # 副标题标签
                widget.configure(fg=self.current_colors["text"])
            elif "highlight" in widget.cget("fg"):  # 高亮标签
                widget.configure(fg=self.current_colors["highlight"])
            else:  # 普通标签
                widget.configure(fg=self.current_colors["fg"])
        elif isinstance(widget, tk.Button):
            if widget.cget("text") in ["▶", "⏮", "⏭"]:  # 控制按钮
                widget.configure(bg=self.current_colors["button"], fg=self.current_colors["fg"])
            elif widget.cget("text") == "⏸":  # 暂停按钮
                widget.configure(bg="#FFC107", fg="black")
            elif widget.cget("text") == "⏹":  # 停止按钮
                widget.configure(bg="#F44336", fg="white")
            else:  # 其他按钮
                widget.configure(bg=self.current_colors["button"], fg=self.current_colors["fg"])
        elif isinstance(widget, tk.Listbox):  # 播放列表
            widget.configure(
                bg=self.current_colors["list_bg"], 
                fg=self.current_colors["fg"],
                selectbackground=self.current_colors["highlight"]
            )
        elif isinstance(widget, tk.LabelFrame):  # 标签框架
            widget.configure(
                bg=self.current_colors["control_bg"], 
                fg=self.current_colors["highlight"]
            )
        elif isinstance(widget, tk.Text):  # 歌词文本框
            widget.configure(
                bg=self.current_colors["list_bg"], 
                fg=self.current_colors["fg"]
            )
        
        # 递归更新子组件
        for child in widget.winfo_children():
            self.update_theme_recursive(child)

        # 添加对Radiobutton的处理
        if isinstance(widget, tk.Radiobutton):
            widget.configure(
                bg=self.current_colors["control_bg"],
                fg=self.current_colors["fg"],
                selectcolor="#333"
            )
    
    # 设置功能
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("500x500")
        settings_window.resizable(False, False)
        settings_window.configure(bg=self.current_colors["bg"])
        
        # 创建带滚动条的Canvas
        canvas = tk.Canvas(settings_window, bg=self.current_colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(settings_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.current_colors["bg"])  # 确保背景色一致
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 主题设置
        theme_frame = tk.LabelFrame(
            scrollable_frame, text="主题设置", 
            font=("Arial", 12), 
            bg=self.current_colors["control_bg"],  # 使用控制面板背景色
            fg=self.current_colors["highlight"],  # 使用高亮色
            padx=10,  # 添加内边距
            pady=10
        )
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        theme_var = tk.StringVar(value=self.theme)
        
        # 所有主题列表
        themes = [
            ("深色主题", "dark"),
            ("浅色主题", "light"),
            ("自定义主题", "custom"),
            ("六花", "rikka"),
            ("海梦", "marin"),
            ("雷姆", "rem"),
            ("伊蕾娜", "elaina"),
            ("黑猫", "kuroneko"),
            ("爱瑠", "chitanda"),
            ("黑仪", "hitagi"),
            ("寄叶2B", "2b"),
            ("景元","jingyuan"),
            ("麻衣", "mai")
        ]
        
        # 创建主题选择按钮
        for text, theme in themes:
            btn = tk.Radiobutton(
                theme_frame, text=text, variable=theme_var, value=theme,
                command=lambda t=theme: self.change_theme(t), 
                bg=self.current_colors["control_bg"],  # 使用控制面板背景色
                fg=self.current_colors["fg"],  # 使用前景色
                selectcolor="#333"  # 选中状态颜色
            )
            btn.pack(anchor=tk.W, padx=10, pady=2)
        
        # 自定义颜色设置
        color_frame = tk.LabelFrame(
            scrollable_frame, text="自定义颜色", 
            font=("Arial", 12), 
            bg=self.current_colors["control_bg"],  # 使用控制面板背景色
            fg=self.current_colors["highlight"],  # 使用高亮色
            padx=10,  # 添加内边距
            pady=10
        )
        color_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 颜色选择按钮
        color_options = [
            ("背景色", "bg"),
            ("文本色", "fg"),
            ("控制面板色", "control_bg"),
            ("高亮色", "highlight"),
            ("列表背景色", "list_bg")
        ]
        
        for text, key in color_options:
            btn = tk.Button(
                color_frame, text=text, 
                command=lambda k=key: self.choose_color(k),
                bg=self.current_colors["button"],  # 使用按钮背景色
                fg=self.current_colors["fg"],  # 使用前景色
                relief=tk.FLAT
            )
            btn.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        # 快捷键设置
        shortcut_frame = tk.LabelFrame(
            scrollable_frame, text="快捷键设置", 
            font=("Arial", 12), 
            bg=self.current_colors["control_bg"],  # 使用控制面板背景色
            fg=self.current_colors["highlight"],  # 使用高亮色
            padx=10,  # 添加内边距
            pady=10
        )
        shortcut_frame.pack(fill=tk.X, padx=10, pady=10)
        
        shortcuts = [
            "空格键: 播放/暂停",
            "左箭头: 上一首",
            "右箭头: 下一首",
            "P: 暂停",
            "S: 停止",
            "+: 增加音量",
            "-: 减小音量",
            "L: 打开歌词窗口"
        ]
        
        for shortcut in shortcuts:
            tk.Label(
                shortcut_frame, text=shortcut, 
                bg=self.current_colors["control_bg"],  # 使用控制面板背景色
                fg=self.current_colors["fg"],  # 使用前景色
                anchor=tk.W
            ).pack(fill=tk.X, padx=10, pady=2)
        
        # 睡眠定时器设置
        sleep_frame = tk.LabelFrame(
            scrollable_frame, text="睡眠定时器", 
            font=("Arial", 12), 
            bg=self.current_colors["control_bg"],  # 使用控制面板背景色
            fg=self.current_colors["highlight"],  # 使用高亮色
            padx=10,  # 添加内边距
            pady=10
        )
        sleep_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            sleep_frame, text="当前状态: " + (f"已设置 ({self.sleep_timer.strftime('%H:%M')})" if self.sleep_timer else "未设置"), 
            bg=self.current_colors["control_bg"],  # 使用控制面板背景色
            fg=self.current_colors["fg"]  # 使用前景色
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Button(
            sleep_frame, text="设置睡眠定时器", 
            command=self.set_sleep_timer, 
            bg="#2196F3",  # 蓝色按钮
            fg="white"  # 白色文字
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # 反馈信息 - 添加在底部
        feedback_frame = tk.Frame(
            scrollable_frame, 
            bg=self.current_colors["bg"]  # 使用主背景色
        )
        feedback_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            feedback_frame, 
            text="Siroukin工作室\n反馈&交流：858927351\n非常希望大家加入我们\n感谢对Siroukin的支持\n\n\nCiallo～(∠・ω< )⌒☆\n私は桜島琥夏と申します。\nはじめまして、\nお会いできて嬉しいです！\n私たちはアマチュア制作チームにすぎません。\nもしあなたも自分の作品に参加/発表する興味があれば、\nSiroukinへようこそ！\n私はSiroukinで待っていますよ～\n\n“据说你发现了站娘の留言？\n就在上面！一定要仔细阅读哦！”", 
            font=("Arial", 10, "bold"), 
            fg="#FF5722",  # 醒目的橙色
            bg=self.current_colors["bg"]  # 使用主背景色
        ).pack(pady=5)
        
        # 关闭按钮
        close_btn = tk.Button(
            scrollable_frame, text="关闭", 
            command=settings_window.destroy, 
            bg="#F44336",  # 红色按钮
            fg="white",  # 白色文字
            width=10
        )
        close_btn.pack(pady=10)
        
        # 更新Canvas滚动区域
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def change_theme(self, theme):
        self.theme = theme
        self.current_colors = self.colors[theme]
        self.apply_theme()
        self.save_settings()
    
    def change_play_mode(self):
        self.play_mode = self.mode_var.get()
        self.save_settings()
        self.status_bar.config(text=f"播放模式已切换: {'顺序播放' if self.play_mode == 'sequential' else '单曲循环' if self.play_mode == 'loop' else '随机播放'}")
    
    def choose_color(self, color_key):
        # 打开颜色选择器
        color = colorchooser.askcolor(
            title=f"选择{color_key}颜色", 
            initialcolor=self.colors["custom"][color_key]
        )[1]
        
        if color:
            self.colors["custom"][color_key] = color
            if self.theme == "custom":
                self.current_colors[color_key] = color
                self.apply_theme()
            self.save_settings()
    
    # 睡眠定时器功能
    def set_sleep_timer(self):
        minutes = simpledialog.askinteger(
            "睡眠定时器", 
            "设置播放多少分钟后停止:", 
            parent=self.root,
            minvalue=1,
            maxvalue=180
        )
        
        if minutes:
            self.sleep_timer = datetime.now() + timedelta(minutes=minutes)
            self.status_bar.config(text=f"已设置睡眠定时器: {minutes}分钟后停止播放")
            self.sleep_btn.config(bg="#4CAF50")
            # 启动定时器检查线程
            threading.Thread(target=self.check_sleep_timer, daemon=True).start()
    
    def check_sleep_timer(self):
        while self.sleep_timer and datetime.now() < self.sleep_timer:
            time.sleep(10)
            remaining = (self.sleep_timer - datetime.now()).seconds // 60
            self.status_bar.config(text=f"睡眠定时器: {remaining}分钟后停止播放")
        
        if self.sleep_timer and datetime.now() >= self.sleep_timer:
            self.stop_song()
            self.sleep_timer = None
            self.sleep_btn.config(bg=self.current_colors["button"])
            self.status_bar.config(text="睡眠定时器已触发，播放已停止")
    
    # 音量控制
    def increase_volume(self):
        new_volume = min(1.0, self.volume + 0.1)
        self.set_volume(new_volume)
        self.volume_scale.set(new_volume)
    
    def decrease_volume(self):
        new_volume = max(0.0, self.volume - 0.1)
        self.set_volume(new_volume)
        self.volume_scale.set(new_volume)
    
    # 歌词功能实现
    def load_lyrics(self, song_path):
        """加载与歌曲同名的歌词文件，支持多种编码"""
        self.lyrics = []  # 重置歌词
        self.current_lyric_index = -1
        
        # 获取歌词文件路径（与歌曲同名，扩展名为.lrc）
        base_path = os.path.splitext(song_path)[0]
        lrc_path = base_path + ".lrc"
        
        if not os.path.exists(lrc_path):
            # 更新歌词显示区域
            self.lyrics_display.config(state=tk.NORMAL)
            self.lyrics_display.delete(1.0, tk.END)
            self.lyrics_display.insert(tk.END, "未找到歌词文件")
            self.lyrics_display.config(state=tk.DISABLED)
            return False
        
        try:
            # 尝试多种编码格式
            encodings = ['utf-8', 'gbk', 'big5', 'latin-1', 'cp1252', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(lrc_path, "r", encoding=encoding) as f:
                        content = f.read()
                    break  # 成功读取，跳出循环
                except UnicodeDecodeError:
                    continue  # 尝试下一种编码
                except Exception as e:
                    print(f"尝试编码 {encoding} 失败: {e}")
                    continue
            
            if content is None:
                # 所有编码都失败，尝试用错误处理方式读取
                try:
                    with open(lrc_path, "r", encoding='utf-8', errors='replace') as f:
                        content = f.read()
                except Exception as e:
                    print(f"使用错误处理读取失败: {e}")
                    content = ""
            
            # 解析歌词内容
            lines = content.splitlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 解析时间标签 [mm:ss.xx]
                time_tags = []
                while line.startswith("["):
                    end_index = line.find("]")
                    if end_index == -1:
                        break
                        
                    time_str = line[1:end_index]
                    line = line[end_index+1:]
                    
                    # 处理时间格式
                    try:
                        # 尝试解析 [mm:ss.xx] 格式
                        if "." in time_str:
                            min_sec, ms = time_str.split(".")
                            minutes, seconds = min_sec.split(":")
                            total_seconds = int(minutes) * 60 + int(seconds) + int(ms) / 100.0
                        # 尝试解析 [mm:ss] 格式
                        elif ":" in time_str:
                            minutes, seconds = time_str.split(":")
                            total_seconds = int(minutes) * 60 + float(seconds)
                        # 尝试解析 [mm:ss:ms] 格式
                        elif ":" in time_str:
                            parts = time_str.split(":")
                            if len(parts) == 3:
                                minutes, seconds, ms = parts
                                total_seconds = int(minutes) * 60 + int(seconds) + int(ms) / 1000.0
                            else:
                                continue
                        else:
                            continue
                        
                        time_tags.append(total_seconds)
                    except:
                        continue
                
                # 添加歌词
                lyric_text = line.strip()
                if lyric_text and time_tags:
                    for time_stamp in time_tags:
                        self.lyrics.append((time_stamp, lyric_text))
            
            # 按时间排序歌词
            self.lyrics.sort(key=lambda x: x[0])
            
            # 更新歌词显示区域
            self.lyrics_display.config(state=tk.NORMAL)
            self.lyrics_display.delete(1.0, tk.END)
            if self.lyrics:
                self.lyrics_display.insert(tk.END, "歌词加载成功，播放时同步显示")
            else:
                self.lyrics_display.insert(tk.END, "未找到有效的歌词内容")
            self.lyrics_display.config(state=tk.DISABLED)
            
            return True
        except Exception as e:
            # 更新歌词显示区域
            self.lyrics_display.config(state=tk.NORMAL)
            self.lyrics_display.delete(1.0, tk.END)
            self.lyrics_display.insert(tk.END, f"歌词解析错误: {str(e)}")
            self.lyrics_display.config(state=tk.DISABLED)
            return False
    
    def show_lyrics_window(self):
        """显示歌词窗口（只显示当前和下一句歌词）"""
        if not self.playlist or not self.playing:
            messagebox.showinfo("提示", "当前没有正在播放的歌曲")
            return
        
        if not self.lyrics:
            messagebox.showinfo("提示", "未找到歌词文件")
            return
        
        # 创建歌词窗口 - 修复了检查窗口是否存在的逻辑
        if hasattr(self, "lyrics_window") and self.lyrics_window is not None:
            try:
                if self.lyrics_window.winfo_exists():
                    self.lyrics_window.lift()
                    return
            except tk.TclError:
                # 如果窗口已被销毁，但引用未清除
                self.lyrics_window = None
        
        # 如果窗口不存在，则创建新窗口
        self.lyrics_window = tk.Toplevel(self.root)
        self.lyrics_window.title("歌词")
        self.lyrics_window.geometry("500x150")
        self.lyrics_window.configure(bg=self.current_colors["bg"])
        self.lyrics_window.attributes("-topmost", True)  # 保持窗口在最前
        self.lyrics_window.protocol("WM_DELETE_WINDOW", self.on_lyrics_window_close)
        
        # 当前歌词标签
        self.current_lyric_label = tk.Label(
            self.lyrics_window, 
            text="", 
            font=("Arial", 16, "bold"),
            fg=self.current_colors["highlight"],
            bg=self.current_colors["bg"],
            pady=10
        )
        self.current_lyric_label.pack(fill=tk.X)
        
        # 下一句歌词标签
        self.next_lyric_label = tk.Label(
            self.lyrics_window, 
            text="", 
            font=("Arial", 12),
            fg=self.current_colors["fg"],
            bg=self.current_colors["bg"],
            pady=5
        )
        self.next_lyric_label.pack(fill=tk.X)
        
        # 初始更新歌词
        self.update_lyrics_window()
    
    def on_lyrics_window_close(self):
        """关闭歌词窗口时清除引用"""
        if hasattr(self, "lyrics_window") and self.lyrics_window:
            self.lyrics_window.destroy()
            self.lyrics_window = None
    
    def update_lyrics(self, current_time):
        """根据当前播放时间更新歌词显示"""
        # 找到当前时间对应的歌词
        new_index = -1
        
        # 查找当前时间对应的歌词行
        for i, (time_stamp, _) in enumerate(self.lyrics):
            if current_time >= time_stamp:
                new_index = i
        
        # 如果歌词索引发生变化，更新显示
        if new_index != self.current_lyric_index:
            self.current_lyric_index = new_index
            
            # 更新主窗口歌词显示
            self.update_main_lyrics()
            
            # 更新歌词窗口
            if hasattr(self, "lyrics_window") and self.lyrics_window is not None:
                try:
                    if self.lyrics_window.winfo_exists():
                        self.update_lyrics_window()
                except tk.TclError:
                    self.lyrics_window = None
    
    def update_main_lyrics(self):
        """更新主窗口歌词显示区域"""
        if not self.lyrics:
            return
        
        # 获取当前时间点前后的歌词
        start_idx = max(0, self.current_lyric_index - 5)
        end_idx = min(len(self.lyrics), self.current_lyric_index + 10)
        
        lyrics_text = ""
        for i in range(start_idx, end_idx):
            time_stamp, text = self.lyrics[i]
            if i == self.current_lyric_index:
                lyrics_text += f"▶ {text}\n"
            else:
                lyrics_text += f"   {text}\n"
        
        self.lyrics_display.config(state=tk.NORMAL)
        self.lyrics_display.delete(1.0, tk.END)
        self.lyrics_display.insert(tk.END, lyrics_text)
        
        # 滚动到当前歌词位置
        if self.current_lyric_index > 0:
            line_index = self.current_lyric_index - start_idx + 1
            self.lyrics_display.see(f"{line_index}.0")
        
        self.lyrics_display.config(state=tk.DISABLED)
    
    def update_lyrics_window(self):
        """更新歌词窗口的内容"""
        if not hasattr(self, "lyrics_window") or self.lyrics_window is None:
            return
        
        try:
            # 检查窗口是否仍然存在
            if not self.lyrics_window.winfo_exists():
                self.lyrics_window = None
                return
        except tk.TclError:
            self.lyrics_window = None
            return
        
        current_text = ""
        next_text = ""
        
        if 0 <= self.current_lyric_index < len(self.lyrics):
            current_text = self.lyrics[self.current_lyric_index][1]
        
        if 0 <= self.current_lyric_index + 1 < len(self.lyrics):
            next_text = self.lyrics[self.current_lyric_index + 1][1]
        
        self.current_lyric_label.config(text=current_text)
        self.next_lyric_label.config(text=next_text)

    def update_scale_styles(self):
        """更新进度条和音量条样式"""
        # 创建ttk样式
        style = ttk.Style()
        
        # 进度条样式
        style.configure(
            "Custom.Horizontal.TScale",
            background=self.current_colors["progress"],
            troughcolor=self.current_colors["control_bg"]
        )
        if hasattr(self, 'progress'):
            self.progress.configure(style="Custom.Horizontal.TScale")
        
        # 音量条样式
        style.configure(
            "Volume.Horizontal.TScale",
            background=self.current_colors["highlight"],
            troughcolor=self.current_colors["control_bg"]
        )
        if hasattr(self, 'volume_scale'):
            self.volume_scale.configure(style="Volume.Horizontal.TScale")    
    # 进度条拖动功能
    def on_progress_drag(self, value):
        """处理进度条拖动事件"""
        if self.playing and not self.paused and hasattr(self, 'song_length'):
            # 计算拖动位置对应的秒数
            position_seconds = float(value) * self.song_length / 100
            # 设置播放位置
            pygame.mixer.music.set_pos(position_seconds)
    
    # 音乐播放功能
    def add_music(self):
        files = filedialog.askopenfilenames(
            filetypes=[("音乐文件", "*.mp3 *.wav *.ogg *.flac")]
        )
        if files:
            for file in files:
                if file not in self.playlist:
                    self.playlist.append(file)
                    self.playlist_box.insert(tk.END, os.path.basename(file))
            self.status_bar.config(text=f"已添加 {len(files)} 首歌曲")
            self.save_settings()
    
    def auto_add_music(self):
        """自动搜索音乐文件"""
        directory = filedialog.askdirectory(title="选择搜索目录")
        if not directory:
            return
        
        # 确保状态栏已创建
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text="正在搜索音乐文件...")
        else:
            print("状态栏尚未创建")
        
        # 在后台线程中执行搜索
        threading.Thread(target=self.search_music_files, args=(directory,), daemon=True).start()
    
    def search_music_files(self, directory):
        """在指定目录中递归搜索音乐文件"""
        music_files = []
        # 移除了.wav扩展名
        extensions = (".mp3", ".ogg", ".flac")
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(extensions):
                    music_files.append(os.path.join(root, file))
        
        # 更新UI
        self.root.after(0, self.add_searched_files, music_files)
    
    def add_searched_files(self, files):
        """添加搜索到的音乐文件"""
        added_count = 0
        
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                self.playlist_box.insert(tk.END, os.path.basename(file))
                added_count += 1
        
        # 确保状态栏已创建
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=f"找到 {len(files)} 首音乐，添加了 {added_count} 首新歌曲")
        else:
            print("状态栏尚未创建")
        
        self.save_settings()
    
    def remove_selected(self):
        selected = self.playlist_box.curselection()
        if selected:
            index = selected[0]
            self.playlist_box.delete(index)
            del self.playlist[index]
            if index < self.current_index:
                self.current_index -= 1
            elif index == self.current_index:
                self.stop_song()
            
            # 确保状态栏已创建
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="已移除选中的歌曲")
            else:
                print("状态栏尚未创建")
            
            self.save_settings()
    
    def clear_playlist(self):
        self.playlist_box.delete(0, tk.END)
        self.playlist.clear()
        self.stop_song()
        self.current_index = 0
        
        # 确保状态栏已创建
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text="播放列表已清空")
        else:
            print("状态栏尚未创建")
        
        self.save_settings()
    
    def play_selected(self, event=None):
        selected = self.playlist_box.curselection()
        if selected:
            self.stop_song()
            self.current_index = selected[0]
            self.play_song()
    
    def play_song(self):
        if not self.playlist:
            return
            
        try:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.play_btn.config(text="▶", bg=self.current_colors["button"], fg="white")
            self.pause_btn.config(bg="#FFC107", fg="black")
            
            song_name = os.path.basename(self.playlist[self.current_index])
            self.current_song_label.config(text=f"当前播放: {song_name}")
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_index)
            self.playlist_box.see(self.current_index)
            
            # 确保状态栏已创建
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text=f"正在播放: {song_name}")
            else:
                print("状态栏尚未创建")
            
            # 获取歌曲长度
            self.song_length = pygame.mixer.Sound(self.playlist[self.current_index]).get_length()
            self.time_label.config(text=f"00:00 / {self.format_time(self.song_length)}")
            
            # 尝试加载歌词
            self.load_lyrics(self.playlist[self.current_index])
            
        except Exception as e:
            # 确保状态栏已创建
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text=f"播放错误: {str(e)}")
            else:
                print(f"播放错误: {str(e)}")
    
    def toggle_play(self):
        if self.playing and self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.pause_btn.config(bg="#FFC107", fg="black")
            
            # 确保状态栏已创建
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="继续播放")
            else:
                print("状态栏尚未创建")
        elif self.playing:
            self.pause_song()
        else:
            self.play_song()
    
    def pause_song(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.pause_btn.config(bg=self.current_colors["button"], fg="white")
            
            # 确保状态栏已创建
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="已暂停")
            else:
                print("状态栏尚未创建")
    
    def toggle_pause(self):
        if self.playing:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.pause_btn.config(bg="#FFC107", fg="black")
                
                # 确保状态栏已创建
                if hasattr(self, 'status_bar'):
                    self.status_bar.config(text="继续播放")
                else:
                    print("状态栏尚未创建")
            else:
                pygame.mixer.music.pause()
                self.paused = True
                self.pause_btn.config(bg=self.current_colors["button"], fg="white")
                
                # 确保状态栏已创建
                if hasattr(self, 'status_bar'):
                    self.status_bar.config(text="已暂停")
                else:
                    print("状态栏尚未创建")
    
    def stop_song(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.play_btn.config(text="▶", bg=self.current_colors["highlight"], fg="white")
        self.pause_btn.config(bg="#FFC107", fg="black")
        self.progress.set(0)
        self.time_label.config(text="00:00 / 00:00")
        
        # 确保状态栏已创建
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text="已停止播放")
        else:
            print("状态栏尚未创建")
        
        # 重置睡眠定时器按钮颜色
        if hasattr(self, 'sleep_btn'):
            self.sleep_btn.config(bg=self.current_colors["button"])
        
        # 重置歌词显示
        self.current_lyric_index = -1
        if hasattr(self, "lyrics_display"):
            self.lyrics_display.config(state=tk.NORMAL)
            self.lyrics_display.delete(1.0, tk.END)
            self.lyrics_display.config(state=tk.DISABLED)
        
        # 关闭歌词窗口
        if hasattr(self, "lyrics_window") and self.lyrics_window is not None:
            try:
                if self.lyrics_window.winfo_exists():
                    self.lyrics_window.destroy()
            except tk.TclError:
                pass
            self.lyrics_window = None
    
    def get_next_song_index(self):
        """根据播放模式获取下一首歌的索引"""
        if not self.playlist:
            return 0
        
        if self.play_mode == "sequential":
            return (self.current_index + 1) % len(self.playlist)
        elif self.play_mode == "loop":
            return self.current_index
        elif self.play_mode == "random":
            return random.randint(0, len(self.playlist) - 1)
        else:
            return (self.current_index + 1) % len(self.playlist)
    
    def prev_song(self):
        if not self.playlist:
            return
            
        self.stop_song()
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_song()
    
    def next_song(self):
        if not self.playlist:
            return
            
        self.stop_song()
        self.current_index = self.get_next_song_index()
        self.play_song()
    
    def set_volume(self, val):
        self.volume = float(val)
        pygame.mixer.music.set_volume(self.volume)
    
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def update_progress(self):
        while True:
            if self.playing and not self.paused:
                try:
                    # 获取当前播放位置
                    current_pos = pygame.mixer.music.get_pos() / 1000.0
                    
                    # 更新进度条
                    if hasattr(self, 'song_length') and self.song_length > 0:
                        progress_percent = (current_pos / self.song_length) * 100
                        if progress_percent <= 100:
                            self.progress.set(progress_percent)
                            self.time_label.config(
                                text=f"{self.format_time(current_pos)} / {self.format_time(self.song_length)}"
                            )
                    
                    # 更新歌词显示
                    if self.lyrics:
                        self.update_lyrics(current_pos)
                    
                    # 检查歌曲是否播放完毕
                    if hasattr(self, 'song_length') and current_pos >= self.song_length - 0.5:
                        self.next_song()
                
                except Exception as e:
                    print(f"更新进度错误: {e}")
            
            time.sleep(0.5)
    
    def on_close(self):
        self.save_settings()
        pygame.mixer.music.stop()
        self.root.destroy()

if __name__ == "__main__":
    # 首先创建并显示启动画面
    splash_root = tk.Tk()
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, "Siroukin.gif")
    
    # 创建启动画面
    splash = SplashScreen(splash_root, gif_path)
    splash_root.mainloop()
    
    # 启动画面关闭后，创建主程序
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()