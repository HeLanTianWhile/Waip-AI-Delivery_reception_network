import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
DATA_ROOT = os.path.join(BASE_DIR, "data", "实验数据", "文本版本", "注意力范围机制数据")
IMG_DIR = os.path.join(DATA_ROOT, "图片")
DATA_DIR = os.path.join(DATA_ROOT, "3D数据")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

NEUROTRANSMITTERS = [
    ("多巴胺", "dopamine", "高多巴胺→注意力收窄，低多巴胺→注意力拓宽"),
    ("乙酰胆碱", "acetylcholine", "高乙酰胆碱→记忆力增强，注意力集中"),
    ("血清素", "serotonin", "高血清素→情绪稳定，注意力平稳"),
    ("内啡肽", "endorphin", "高内啡肽→愉悦感，注意力放松但持久"),
    ("P物质", "substance_P", "高P物质→痛觉敏感，注意力应激性增强"),
    ("肾上腺素", "epinephrine", "高肾上腺素→应激状态，注意力高度集中"),
    ("去甲肾上腺素", "Noradrenaline", "高去甲肾上腺素→警觉性高，注意力锐利"),
    ("GABA", "GABA", "高GABA→抑制过度兴奋，注意力平稳适中"),
    ("谷氨酸", "Glutamic_acid", "高谷氨酸→激活大脑皮层，注意力敏锐"),
]

TEXT_LEN_MIN, TEXT_LEN_MAX = 1, 30
NT_MIN, NT_MAX = 15000, 50000

def compute_attention_range(text_len, dopamine, acetylcholine, serotonin, endorphin,
                            substance_P, epinephrine, noradrenaline, GABA, glamic_acid):
    dp = float(100000 - dopamine) / 10000
    ap = float(100000 - acetylcholine) / 10000
    sp = float(100000 - serotonin) / 10000
    ep = float(100000 - endorphin) / 10000
    spp = float(substance_P) / 10000
    epip = float(epinephrine) / 10000
    np_ = float(100000 - noradrenaline) / 10000
    gabap = float(GABA) / 10000
    gp = float(glamic_acid) / 10000
    total = dp + ap + sp + ep + spp + epip + np_ + gabap + gp
    base_range = total / 10.0
    if text_len <= 5:
        attention_range = 4.0
    elif text_len <= 15:
        attention_range = base_range
    else:
        attention_range = max(1.0, base_range - (text_len - 15) * 0.15)
    return round(attention_range, 2)

def compute_surface_3d(neuro_index, other_const):
    name_cn, name_en, desc = NEUROTRANSMITTERS[neuro_index]
    text_lens = np.arange(TEXT_LEN_MIN, TEXT_LEN_MAX + 1)
    nt_levels = np.linspace(NT_MIN, NT_MAX, 50)
    Z = np.zeros((len(nt_levels), len(text_lens)))
    for i, nt_val in enumerate(nt_levels):
        for j, tlen in enumerate(text_lens):
            args = [tlen] + list(other_const)
            args[neuro_index + 1] = nt_val
            Z[i, j] = compute_attention_range(*args)
    return text_lens, nt_levels, Z, name_cn, name_en, desc

def generate_static_images(other_const):
    print("\n============================================================")
    print("开始生成各神经递质对注意力范围影响的三维可视化图片")
    print("============================================================")
    for neuro_index, (name_cn, name_en, desc) in enumerate(NEUROTRANSMITTERS):
        text_lens, nt_levels, Z, name_cn, name_en, desc = compute_surface_3d(neuro_index, other_const)
        nt_pct = (nt_levels - NT_MIN) / (NT_MAX - NT_MIN) * 100
        T, N = np.meshgrid(text_lens, nt_pct)
        fig = plt.figure(figsize=(16, 12))
        ax1 = fig.add_subplot(221, projection="3d")
        surf = ax1.plot_surface(T, N, Z, cmap=cm.YlOrRd, alpha=0.85, linewidth=0, antialiased=True)
        ax1.set_xlabel("文本长度（字符）", fontsize=10, labelpad=8)
        ax1.set_ylabel(f"{name_cn}浓度 (%)", fontsize=10, labelpad=8)
        ax1.set_zlabel("注意力范围", fontsize=10, labelpad=8)
        ax1.set_title(f"【表面图】{name_cn}浓度 & 文本长度 → 注意力范围", fontsize=12, fontweight="bold")
        fig.colorbar(surf, ax=ax1, shrink=0.5, label="注意力范围", pad=0.1)
        ax1.view_init(elev=25, azim=45)
        ax2 = fig.add_subplot(222, projection="3d")
        surf2 = ax2.plot_surface(T, N, Z, cmap=cm.coolwarm, alpha=0.85, linewidth=0, antialiased=True)
        ax2.set_xlabel("文本长度（字符）", fontsize=10, labelpad=8)
        ax2.set_ylabel(f"{name_cn}浓度 (%)", fontsize=10, labelpad=8)
        ax2.set_zlabel("注意力范围", fontsize=10, labelpad=8)
        ax2.set_title(f"【冷暖图】{name_cn}浓度 & 文本长度 → 注意力范围", fontsize=12, fontweight="bold")
        fig.colorbar(surf2, ax=ax2, shrink=0.5, label="注意力范围", pad=0.1)
        ax2.view_init(elev=30, azim=135)
        ax3 = fig.add_subplot(223, projection="3d")
        colors_3d = [cm.viridis((nt - NT_MIN) / (NT_MAX - NT_MIN)) for nt in nt_levels]
        for k in range(0, len(nt_levels), 4):
            ax3.plot(text_lens, [k] * len(text_lens), Z[k], color=colors_3d[k], alpha=0.7, linewidth=1.5)
        scatter = ax3.scatter(
            np.repeat(text_lens[len(text_lens)//2], len(nt_levels[::4])),
            np.arange(0, len(nt_levels), 4),
            Z[::4, len(text_lens)//2],
            c=Z[::4, len(text_lens)//2], cmap="YlOrRd", s=40, zorder=5
        )
        ax3.set_xlabel("文本长度（字符）", fontsize=10, labelpad=8)
        ax3.set_ylabel(f"{name_cn}浓度层级", fontsize=10, labelpad=8)
        ax3.set_zlabel("注意力范围", fontsize=10, labelpad=8)
        ax3.set_title(f"【等高线侧视图】{name_cn}各浓度下的注意力范围曲线", fontsize=12, fontweight="bold")
        ax3.view_init(elev=20, azim=60)
        fig.colorbar(scatter, ax=ax3, shrink=0.5, label="注意力范围", pad=0.1)
        ax4 = fig.add_subplot(224)
        levels_to_show = [0, 12, 25, 37, 49]
        labels_to_show = ["0%(低)", "25%", "50%(中)", "75%", "100%(高)"]
        selected_idx = [levels_to_show[i] for i in range(len(levels_to_show)) if levels_to_show[i] < len(nt_levels)]
        sel_labels = [labels_to_show[i] for i in range(len(labels_to_show)) if levels_to_show[i] < len(nt_levels)]
        colors_line = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]
        for idx, (li, cl, label) in enumerate(zip(selected_idx, colors_line[:len(selected_idx)], sel_labels)):
            ax4.plot(text_lens, Z[li], color=cl, linewidth=2.5, marker="o", markersize=4, label=f"{name_cn}{label}")
        ax4.set_xlabel("文本长度（字符）", fontsize=11)
        ax4.set_ylabel("注意力范围", fontsize=11)
        ax4.set_title(f"【折线图】{name_cn}不同浓度下的注意力范围曲线族", fontsize=12, fontweight="bold")
        ax4.legend(fontsize=9, loc="upper right")
        ax4.grid(True, alpha=0.3)
        plt.suptitle(f"神经递质「{name_cn}」调高/调低对注意力范围的影响\n(desc: {desc})", fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()
        img_path = os.path.join(IMG_DIR, f"3D_{name_en}_注意力范围影响.png")
        plt.savefig(img_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  [OK] 3D_{name_en}_注意力范围影响.png")
        data_path = os.path.join(DATA_DIR, f"3D_{name_en}_注意力范围数据.3D.npz")
        np.savez(data_path,
                 text_lengths=text_lens,
                 nt_levels=nt_levels,
                 nt_levels_percent=(nt_levels - NT_MIN) / (NT_MAX - NT_MIN),
                 attention_surface=Z,
                 neurotransmitter_cn=name_cn,
                 neurotransmitter_en=name_en,
                 description=desc,
                 formula="(100000-x)/10000 for most, x/10000 for P物质, avg/10")
        print(f"  [OK] 3D_{name_en}_注意力范围数据.3D.npz")

def generate_overview_matrix(other_const):
    print("\n[生成] 全局神经递质影响矩阵...")
    fig = plt.figure(figsize=(20, 18))
    fig.suptitle("九种神经递质调高/调低对注意力范围影响的3D矩阵视图", fontsize=16, fontweight="bold", y=0.98)
    for neuro_index, (name_cn, name_en, desc) in enumerate(NEUROTRANSMITTERS):
        text_lens, nt_levels, Z, _, _, _ = compute_surface_3d(neuro_index, other_const)
        ax = fig.add_subplot(3, 3, neuro_index + 1, projection="3d")
        T, N_raw = np.meshgrid(text_lens, nt_levels)
        N = (N_raw - NT_MIN) / (NT_MAX - NT_MIN) * 100
        surf = ax.plot_surface(T, N, Z, cmap=cm.YlOrRd, alpha=0.85, linewidth=0, antialiased=True)
        ax.set_xlabel("文本长", fontsize=8)
        ax.set_ylabel(f"{name_cn}\n浓度%", fontsize=8)
        ax.set_zlabel("注意力", fontsize=8)
        ax.set_title(f"{name_cn}", fontsize=11, fontweight="bold")
        ax.view_init(elev=20, azim=30 + neuro_index * 15)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(IMG_DIR, "3D_九递质全局矩阵.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 3D_九递质全局矩阵.png")

def generate_nt_comparison_image(other_const):
    print("\n[生成] 九递质注意力响应对比图...")
    text_lens = np.arange(TEXT_LEN_MIN, TEXT_LEN_MAX + 1)
    nt_pct_vals = [10, 50, 90]
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("九种神经递质在低/中/高浓度下的注意力范围响应曲线", fontsize=14, fontweight="bold")
    for neuro_index, (name_cn, name_en, desc) in enumerate(NEUROTRANSMITTERS):
        ax = fig.add_subplot(3, 3, neuro_index + 1)
        _, _, Z, _, _, _ = compute_surface_3d(neuro_index, other_const)
        colors_c = ["#2196F3", "#4CAF50", "#F44336"]
        labels_c = ["低浓度(10%)", "中浓度(50%)", "高浓度(90%)"]
        idx_map = {10: 2, 50: 14, 90: 26}
        for pct, c, lbl in zip([10, 50, 90], colors_c, labels_c):
            idx = {10: 4, 50: 24, 90: 44}[pct]
            ax.plot(text_lens, Z[idx], color=c, linewidth=2, marker="o", markersize=3, label=lbl)
        ax.set_title(f"{name_cn}", fontsize=11, fontweight="bold")
        ax.set_xlabel("文本长度", fontsize=9)
        ax.set_ylabel("注意力范围", fontsize=9)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, alpha=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(IMG_DIR, "3D_九递质响应对比曲线.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 3D_九递质响应对比曲线.png")

def interactive_3d_viewer(other_const):
    print("\n[启动] 交互式3D注意力范围查看器说明:")
    print("  运行以下命令启动交互式查看器（需要图形界面）:")
    print(f"  cd \"{DATA_ROOT}\"")
    print("  python 交互式3D注意力查看器.py")
    viewer_code = r'''
import os
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

NT_MIN, NT_MAX = 15000, 50000
TEXT_LEN_MIN, TEXT_LEN_MAX = 1, 30

NEUROTRANSMITTERS = [
    ("多巴胺", "dopamine"),
    ("乙酰胆碱", "acetylcholine"),
    ("血清素", "serotonin"),
    ("内啡肽", "endorphin"),
    ("P物质", "substance_P"),
    ("肾上腺素", "epinephrine"),
    ("去甲肾上腺素", "Noradrenaline"),
    ("GABA", "GABA"),
    ("谷氨酸", "Glutamic_acid"),
]

def compute_attention_range(text_len, dopamine, acetylcholine, serotonin, endorphin,
                            substance_P, epinephrine, noradrenaline, GABA, glamic_acid):
    dp = float(100000 - dopamine) / 10000
    ap = float(100000 - acetylcholine) / 10000
    sp = float(100000 - serotonin) / 10000
    ep = float(100000 - endorphin) / 10000
    spp = float(substance_P) / 10000
    epip = float(epinephrine) / 10000
    np_ = float(100000 - noradrenaline) / 10000
    gabap = float(GABA) / 10000
    gp = float(glamic_acid) / 10000
    total = dp + ap + sp + ep + spp + epip + np_ + gabap + gp
    base_range = total / 10.0
    if text_len <= 5:
        attention_range = 4.0
    elif text_len <= 15:
        attention_range = base_range
    else:
        attention_range = max(1.0, base_range - (text_len - 15) * 0.15)
    return round(attention_range, 2)

class Attention3DViewer:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle("交互式3D注意力范围查看器 — 拖动滑块调整神经递质浓度", fontsize=14, fontweight="bold")
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.base_values = {
            "多巴胺": 35000, "乙酰胆碱": 25000, "血清素": 50000, "内啡肽": 40000,
            "P物质": 15000, "肾上腺素": 20000, "去甲肾上腺素": 22000, "GABA": 30000, "谷氨酸": 25000
        }
        self.current_values = dict(self.base_values)
        self.fixed_nt = "多巴胺"
        self.slider_ax = []
        self.sliders = {}
        self.init_ui()
        self.update_plot()

    def init_ui(self):
        slider_colors = ["#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5",
                         "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#FF9800"]
        top = 0.92
        for i, (name, en) in enumerate(NEUROTRANSMITTERS):
            left = 0.02 + (i % 3) * 0.16
            height = 0.018
            ax = self.fig.add_axes([left, top - (i // 3) * 0.05, 0.14, height])
            slider = Slider(ax, name, 0, 100, valinit=self.value_to_pct(self.base_values[name]),
                            color=slider_colors[i % len(slider_colors)])
            slider.on_changed(self.on_slider_change)
            self.sliders[name] = slider
        self.fixed_ax = self.fig.add_axes([0.55, 0.01, 0.40, 0.03])
        self.fixed_radio = RadioButtons(self.fixed_ax, [n for n, e in NEUROTRANSMITTERS],
                                         active=0, activecolor="#2196F3")
        self.fixed_radio.on_clicked(self.on_fixed_change)
        self.reset_ax = self.fig.add_axes([0.02, 0.01, 0.10, 0.03])
        self.reset_btn = Button(self.reset_ax, "重置基准值", color="#607D8B")
        self.reset_btn.on_clicked(self.on_reset)

    def value_to_pct(self, v):
        return (v - NT_MIN) / (NT_MAX - NT_MIN) * 100

    def pct_to_value(self, p):
        return NT_MIN + (p / 100) * (NT_MAX - NT_MIN)

    def on_slider_change(self, val):
        name = [k for k, s in self.sliders.items() if s == val][0] if False else None
        for n, s in self.sliders.items():
            if s.val == val and s is val:
                name = n
                break
        self.update_plot()

    def on_fixed_change(self, label):
        self.fixed_nt = label
        self.update_plot()

    def on_reset(self, event):
        for n, s in self.sliders.items():
            s.reset()

    def update_plot(self):
        self.ax.clear()
        for name, slider in self.sliders.items():
            self.current_values[name] = self.pct_to_value(slider.val)
        fixed_vals = [self.current_values[n] for n, e in NEUROTRANSMITTERS]
        text_lens = np.arange(TEXT_LEN_MIN, TEXT_LEN_MAX + 1)
        fixed_idx = [n for n, e in NEUROTRANSMITTERS].index(self.fixed_nt)
        fixed_range = np.linspace(NT_MIN, NT_MAX, 40)
        Z = np.zeros((len(fixed_range), len(text_lens)))
        for i, fv in enumerate(fixed_range):
            args = fixed_vals.copy()
            args[fixed_idx] = fv
            for j, tlen in enumerate(text_lens):
                Z[i, j] = compute_attention_range(tlen, *args)
        T, F = np.meshgrid(text_lens, fixed_range)
        F_pct = (F - NT_MIN) / (NT_MAX - NT_MIN) * 100
        surf = self.ax.plot_surface(T, F_pct, Z, cmap=cm.YlOrRd, alpha=0.88, linewidth=0, antialiased=True)
        self.ax.set_xlabel("文本长度（字符）", fontsize=11, labelpad=10)
        self.ax.set_ylabel(f"{self.fixed_nt}浓度 (%)", fontsize=11, labelpad=10)
        self.ax.set_zlabel("注意力范围", fontsize=11, labelpad=10)
        self.ax.set_title(f"Z = 注意力范围 | X = 文本长度 | Y = {self.fixed_nt}浓度 (%)", fontsize=12, fontweight="bold")
        self.ax.view_init(elev=22, azim=45)
        try:
            self.fig.colorbar(surf, ax=self.ax, shrink=0.6, label="注意力范围", pad=0.12)
        except:
            pass
        info = "当前递质值:\\n" + "\\n".join([f"  {n}: {self.value_to_pct(v):.0f}%" for n, v in self.current_values.items()])
        self.ax.text2D(0.02, 0.95, info, transform=self.ax.transAxes, fontsize=8,
                       verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

if __name__ == "__main__":
    viewer = Attention3DViewer()
    viewer.show()
'''
    viewer_path = os.path.join(IMG_DIR, "交互式3D注意力查看器.py")
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(viewer_code)
    print(f"  [OK] 交互式3D注意力查看器.py (保存在图片目录下)")

def main():
    print("=" * 60)
    print("Waip AGI 注意力范围3D可视化生成器")
    print("=" * 60)
    print(f"\n图片输出目录: {IMG_DIR}")
    print(f"3D数据输出目录: {DATA_DIR}")
    baseline = {
        "多巴胺": 35000, "乙酰胆碱": 25000, "血清素": 50000, "内啡肽": 40000,
        "P物质": 15000, "肾上腺素": 20000, "去甲肾上腺素": 22000, "GABA": 30000, "谷氨酸": 25000
    }
    other_const = [baseline[n] for n, e, d in NEUROTRANSMITTERS]
    generate_static_images(other_const)
    generate_overview_matrix(other_const)
    generate_nt_comparison_image(other_const)
    interactive_3d_viewer(other_const)
    data_overview = os.path.join(DATA_DIR, "注意力范围_全局3D数据.3D.npz")
    text_lens = np.arange(TEXT_LEN_MIN, TEXT_LEN_MAX + 1)
    all_surfaces = {}
    for neuro_index, (name_cn, name_en, desc) in enumerate(NEUROTRANSMITTERS):
        _, nt_levels, Z, _, _, _ = compute_surface_3d(neuro_index, other_const)
        all_surfaces[name_en] = Z
    np.savez(data_overview,
             text_lengths=text_lens,
             nt_levels=(nt_levels - NT_MIN) / (NT_MAX - NT_MIN),
             attention_surfaces=all_surfaces,
             baseline_values=baseline,
             formula="avg((100000-x)/10000)/10, 9 neurotransmitters")
    print(f"  [OK] 注意力范围_全局3D数据.3D.npz")
    print(f"\n{'=' * 60}")
    print(f"全部完成！图片和3D数据已保存至:")
    print(f"  图片: {IMG_DIR}")
    print(f"  3D数据: {DATA_DIR}")
    print("=" * 60)
    print("\n生成内容清单:")
    print("  图片:")
    print("    - 3D_多巴胺_注意力范围影响.png")
    print("    - 3D_乙酰胆碱_注意力范围影响.png")
    print("    - ... (共9个递质)")
    print("    - 3D_九递质全局矩阵.png")
    print("    - 3D_九递质响应对比曲线.png")
    print("    - 交互式3D注意力查看器.py")
    print("  3D数据:")
    print("    - 3D_多巴胺_注意力范围数据.3D.npz")
    print("    - ... (共9个递质)")
    print("    - 注意力范围_全局3D数据.3D.npz")

if __name__ == "__main__":
    main()