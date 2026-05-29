
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
