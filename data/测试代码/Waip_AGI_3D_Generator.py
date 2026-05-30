import os
import shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_ROOT = os.path.join(BASE_DIR, "data", "实验数据", "Waip AI AGI-Text")

MECHANISMS = {
    "Text_Attention_Algorithm": {"desc": "注意力范围", "func": "attention"},
    "calculate_activation_valve": {"desc": "激活阀值", "func": "valve"},
    "Calculation_formula_number_branches_associative_tree": {"desc": "联想分支数", "func": "branches"},
}

NEUROTRANSMITTERS = [
    ("多巴胺", "dopamine"),
    ("乙酰胆碱", "acetylcholine"),
    ("血清素", "serotonin"),
    ("内啡肽", "endorphin"),
    ("P物质", "substance_P"),
    ("肾上腺素", "epinephrine"),
    ("去甲肾上腺素", "Noradrenaline"),
    ("GABA", "GABA"),
    ("谷氨酸", "glutamic_acid"),
]

NT_MIN, NT_MAX = 15000, 50000
TEXT_LEN_MIN, TEXT_LEN_MAX = 1, 30

def compute_attention_range(text_len, dopamine, acetylcholine, serotonin, endorphin,
                            substance_P, epinephrine, noradrenaline, GABA, glutamic_acid):
    dp = float(100000 - dopamine) / 10000
    ap = float(100000 - acetylcholine) / 10000
    sp = float(100000 - serotonin) / 10000
    ep = float(100000 - endorphin) / 10000
    spp = float(substance_P) / 10000
    epip = float(100000 - epinephrine) / 10000
    np_ = float(100000 - noradrenaline) / 10000
    gabap = float(GABA) / 10000
    gp = float(glutamic_acid) / 10000
    total = dp + ap + sp + ep + spp + epip + np_ + gabap + gp
    base_range = total / 10.0
    if text_len <= 5:
        return 4.0
    elif text_len <= 15:
        return round(base_range, 2)
    else:
        return round(max(1.0, base_range - (text_len - 15) * 0.15), 2)

def calculate_activation_valve(dopamine, acetylcholine, serotonin, endorphin,
                               substance_P, epinephrine, noradrenaline, GABA, glutamic_acid):
    dp = float((100000 - dopamine) / 5)
    ap = float((100000 - acetylcholine) / 5)
    sp = float((100000 - serotonin) / 5)
    ep = float((100000 - endorphin) / 5)
    spp = float(substance_P / 5)
    epip = float((100000 - epinephrine) / 5)
    np_ = float((100000 - noradrenaline) / 5)
    gabap = float((100000 - GABA) / 5)
    gp = float((100000 - glutamic_acid) / 5)
    return round((dp + ap + sp + ep + spp + epip + np_ + gabap + gp) / 10)

def calculate_branches(dopamine, acetylcholine, serotonin, endorphin,
                      substance_P, epinephrine, noradrenaline, GABA, glutamic_acid):
    dp = float(dopamine) / 1000
    ap = float(acetylcholine) / 1000
    sp = float(serotonin) / 1000
    ep = float(endorphin) / 1000
    spp = float(100000 - substance_P) / 1000
    epip = float(100000 - epinephrine) / 1000
    np_ = float(100000 - noradrenaline) / 1000
    gabap = float(100000 - GABA) / 1000
    gp = float(100000 - glutamic_acid) / 1000
    return round(dp + ap + sp + ep + spp + epip + np_ + gabap + gp)

def clear_and_create(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

def setup_folders():
    for mech_name in MECHANISMS:
        mech_path = os.path.join(DATA_ROOT, mech_name)
        clear_and_create(os.path.join(mech_path, "图片"))
        clear_and_create(os.path.join(mech_path, "3D数据"))

def generate_attention_plots(baseline, other_const):
    mech_name = "Text_Attention_Algorithm"
    mech_path = os.path.join(DATA_ROOT, mech_name)
    img_dir = os.path.join(mech_path, "图片")
    data_dir = os.path.join(mech_path, "3D数据")
    nt_pct = np.linspace(0, 100, 50)
    text_lens = np.arange(TEXT_LEN_MIN, TEXT_LEN_MAX + 1)
    colors = ["#F44336","#E91E63","#9C27B0","#673AB7","#3F51B5","#2196F3","#00BCD4","#009688","#4CAF50"]

    print(f"\n[{mech_name}] 生成注意力范围3D可视化...")
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        Z = np.zeros((len(nt_pct), len(text_lens)))
        for i, pct in enumerate(nt_pct):
            for j, tlen in enumerate(text_lens):
                args = list(other_const)
                args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
                Z[i, j] = compute_attention_range(tlen, *args)
        T, N = np.meshgrid(text_lens, nt_pct)
        fig = plt.figure(figsize=(16, 10))
        ax1 = fig.add_subplot(221, projection="3d")
        surf = ax1.plot_surface(T, N, Z, cmap=cm.YlOrRd, alpha=0.85, linewidth=0, antialiased=True)
        ax1.set_xlabel("文本长度", fontsize=10, labelpad=8)
        ax1.set_ylabel(f"{name_cn}浓度%", fontsize=10, labelpad=8)
        ax1.set_zlabel("注意力范围", fontsize=10, labelpad=8)
        ax1.set_title(f"表面图：{name_cn}浓度&文本长度→注意力范围", fontsize=11, fontweight="bold")
        ax1.view_init(elev=25, azim=45)
        fig.colorbar(surf, ax=ax1, shrink=0.5, label="注意力范围", pad=0.1)

        ax2 = fig.add_subplot(222, projection="3d")
        surf2 = ax2.plot_surface(T, N, Z, cmap=cm.coolwarm, alpha=0.85, linewidth=0, antialiased=True)
        ax2.set_xlabel("文本长度", fontsize=10, labelpad=8)
        ax2.set_ylabel(f"{name_cn}浓度%", fontsize=10, labelpad=8)
        ax2.set_zlabel("注意力范围", fontsize=10, labelpad=8)
        ax2.set_title(f"冷暖图：{name_cn}浓度&文本长度→注意力范围", fontsize=11, fontweight="bold")
        ax2.view_init(elev=30, azim=135)
        fig.colorbar(surf2, ax=ax2, shrink=0.5, label="注意力范围", pad=0.1)

        ax3 = fig.add_subplot(223, projection="3d")
        for k in range(0, len(nt_pct), 4):
            ax3.plot(text_lens, [k]*len(text_lens), Z[k], color=colors[neuro_index], alpha=0.6)
        scatter_idx = list(range(0, len(nt_pct), 10))
        ax3.scatter(np.repeat(text_lens[len(text_lens)//2], len(scatter_idx)), scatter_idx, Z[scatter_idx, len(text_lens)//2], c=Z[scatter_idx, len(text_lens)//2], cmap="YlOrRd", s=40)
        ax3.set_xlabel("文本长度", fontsize=10, labelpad=8)
        ax3.set_ylabel(f"{name_cn}浓度层级", fontsize=10, labelpad=8)
        ax3.set_zlabel("注意力范围", fontsize=10, labelpad=8)
        ax3.set_title(f"等高线侧视图：{name_cn}各浓度下的注意力曲线", fontsize=11, fontweight="bold")
        ax3.view_init(elev=20, azim=60)

        ax4 = fig.add_subplot(224)
        for idx, (p, lbl) in enumerate(zip([0, 24, 49], ["低(0%)", "中(50%)", "高(100%)"])):
            ax4.plot(text_lens, Z[p], color=colors[idx], linewidth=2, marker="o", markersize=4, label=f"{name_cn}{lbl}")
        ax4.set_xlabel("文本长度（字符）", fontsize=11)
        ax4.set_ylabel("注意力范围", fontsize=11)
        ax4.set_title(f"折线图：{name_cn}不同浓度下的注意力范围曲线族", fontsize=11, fontweight="bold")
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)

        plt.suptitle(f"神经递质「{name_cn}」调高/调低对注意力范围的影响", fontsize=13, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(img_dir, f"3D_{name_en}_注意力范围影响.png"), dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  [OK] 3D_{name_en}_注意力范围影响.png")

        np.savez(os.path.join(data_dir, f"3D_{name_en}_注意力范围数据.3D.npz"),
                 text_lengths=text_lens, nt_percent=nt_pct, attention_surface=Z,
                 neurotransmitter_cn=name_cn, neurotransmitter_en=name_en)
        print(f"  [OK] 3D_{name_en}_注意力范围数据.3D.npz")

    print(f"\n[{mech_name}] 生成九递质全局矩阵...")
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle("九种神经递质调高/调低对注意力范围影响的3D矩阵视图", fontsize=14, fontweight="bold", y=0.98)
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        Z = np.zeros((len(nt_pct), len(text_lens)))
        for i, pct in enumerate(nt_pct):
            for j, tlen in enumerate(text_lens):
                args = list(other_const)
                args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
                Z[i, j] = compute_attention_range(tlen, *args)
        ax = fig.add_subplot(3, 3, neuro_index + 1, projection="3d")
        T, N_raw = np.meshgrid(text_lens, nt_pct)
        surf = ax.plot_surface(T, N_raw, Z, cmap=cm.YlOrRd, alpha=0.85, linewidth=0, antialiased=True)
        ax.set_xlabel("文本长", fontsize=8)
        ax.set_ylabel(f"{name_cn}\n浓度%", fontsize=8)
        ax.set_zlabel("注意力", fontsize=8)
        ax.set_title(f"{name_cn}", fontsize=11, fontweight="bold")
        ax.view_init(elev=20, azim=30 + neuro_index * 15)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(img_dir, "3D_九递质全局矩阵.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 3D_九递质全局矩阵.png")

    print(f"\n[{mech_name}] 生成九递质响应对比曲线...")
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("九种神经递质在低/中/高浓度下的注意力范围响应曲线", fontsize=14, fontweight="bold", y=0.98)
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        Z = np.zeros((len(nt_pct), len(text_lens)))
        for i, pct in enumerate(nt_pct):
            for j, tlen in enumerate(text_lens):
                args = list(other_const)
                args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
                Z[i, j] = compute_attention_range(tlen, *args)
        ax = fig.add_subplot(3, 3, neuro_index + 1)
        for idx, (pct_val, c, lbl) in enumerate(zip([0, 24, 49], ["#2196F3","#4CAF50","#F44336"], ["低(0%)","中(50%)","高(100%)"])):
            ax.plot(text_lens, Z[pct_val], color=c, linewidth=2, marker="o", markersize=3, label=lbl)
        ax.set_title(f"{name_cn}", fontsize=11, fontweight="bold")
        ax.set_xlabel("文本长度", fontsize=9)
        ax.set_ylabel("注意力范围", fontsize=9)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, alpha=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(img_dir, "3D_九递质响应对比曲线.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 3D_九递质响应对比曲线.png")

    all_surfaces = {}
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        Z = np.zeros((len(nt_pct), len(text_lens)))
        for i, pct in enumerate(nt_pct):
            for j, tlen in enumerate(text_lens):
                args = list(other_const)
                args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
                Z[i, j] = compute_attention_range(tlen, *args)
        all_surfaces[name_en] = Z
    np.savez(os.path.join(data_dir, "注意力范围_全局3D数据.3D.npz"),
             text_lengths=text_lens, nt_percent=nt_pct, attention_surfaces=all_surfaces,
             baseline_values=baseline, formula="avg((100000-x)/10000)/10")
    print(f"  [OK] 注意力范围_全局3D数据.3D.npz")

def generate_valve_plots(baseline, other_const):
    mech_name = "calculate_activation_valve"
    mech_path = os.path.join(DATA_ROOT, mech_name)
    img_dir = os.path.join(mech_path, "图片")
    data_dir = os.path.join(mech_path, "3D数据")
    nt_pct = np.linspace(0, 100, 50)
    colors = ["#F44336","#E91E63","#9C27B0","#673AB7","#3F51B5","#2196F3","#00BCD4","#009688","#4CAF50"]

    print(f"\n[{mech_name}] 生成激活阀值可视化...")
    all_valves = []
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        valves = []
        for pct in nt_pct:
            args = list(other_const)
            args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
            valves.append(calculate_activation_valve(*args))
        all_valves.append(valves)

    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("激活阀值 - 神经递质浓度影响分析", fontsize=14, fontweight="bold")
    ax1 = fig.add_subplot(221)
    for i, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        ax1.plot(nt_pct, all_valves[i], color=colors[i], linewidth=2, label=name_cn)
    ax1.set_xlabel("神经递质浓度 (%)", fontsize=11)
    ax1.set_ylabel("激活阀值", fontsize=11)
    ax1.set_title("各神经递质对激活阀值的影响曲线", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=8, loc="upper right", ncol=3)
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(222, projection="3d")
    X, Y = np.meshgrid(nt_pct, np.arange(9))
    Z = np.array(all_valves)
    ax2.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.85, linewidth=0, antialiased=True)
    ax2.set_xlabel("递质浓度 (%)", fontsize=10)
    ax2.set_ylabel("递质编号", fontsize=10)
    ax2.set_zlabel("激活阀值", fontsize=10)
    ax2.set_title("激活阀值三维分布图", fontsize=12, fontweight="bold")
    ax2.view_init(elev=25, azim=45)

    baseline_valve = calculate_activation_valve(*other_const)
    changes = []
    for neuro_index in range(9):
        high_args = list(other_const); high_args[neuro_index] = NT_MAX
        low_args = list(other_const); low_args[neuro_index] = NT_MIN
        changes.append({"name": NEUROTRANSMITTERS[neuro_index][0], "high": calculate_activation_valve(*high_args), "low": calculate_activation_valve(*low_args), "baseline": baseline_valve})

    ax3 = fig.add_subplot(223)
    x_pos = np.arange(9)
    ax3.bar(x_pos - 0.3, [c["low"] for c in changes], 0.3, label="低浓度", color="#2196F3")
    ax3.bar(x_pos, [c["baseline"] for c in changes], 0.3, label="基准值", color="#4CAF50")
    ax3.bar(x_pos + 0.3, [c["high"] for c in changes], 0.3, label="高浓度", color="#F44336")
    ax3.set_xlabel("神经递质", fontsize=11)
    ax3.set_ylabel("激活阀值", fontsize=11)
    ax3.set_title("各神经递质高低浓度下的激活阀值对比", fontsize=12, fontweight="bold")
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([c["name"] for c in changes], rotation=45, fontsize=9)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    ax4 = fig.add_subplot(224)
    sensitivity = [abs(c["high"] - c["low"]) / c["baseline"] * 100 for c in changes]
    ax4.barh([c["name"] for c in changes], sensitivity, color=colors)
    ax4.set_xlabel("阀值变化敏感度 (%)", fontsize=11)
    ax4.set_ylabel("神经递质", fontsize=11)
    ax4.set_title("各神经递质对激活阀值的敏感度", fontsize=12, fontweight="bold")
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "激活阀值_神经递质影响.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 激活阀值_神经递质影响.png")

    fig3d = plt.figure(figsize=(12, 10))
    ax = fig3d.add_subplot(111, projection="3d")
    for i, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        ax.plot(nt_pct, [i]*len(nt_pct), all_valves[i], color=colors[i], linewidth=2.5, label=name_cn)
    ax.scatter([50]*9, np.arange(9), [baseline_valve]*9, c="gold", s=100, marker="*", label="基准状态")
    ax.set_xlabel("神经递质浓度 (%)", fontsize=11)
    ax.set_ylabel("神经递质类型", fontsize=11)
    ax.set_zlabel("激活阀值", fontsize=11)
    ax.set_title("激活阀值三维分布图（可旋转查看）", fontsize=13, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")
    ax.view_init(elev=30, azim=60)
    plt.savefig(os.path.join(img_dir, "激活阀值_三维分布图.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 激活阀值_三维分布图.png")

    valve_data = {}
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        valve_data[name_en] = all_valves[neuro_index]
    np.savez(os.path.join(data_dir, "激活阀值_全局数据.3D.npz"),
             nt_percent=nt_pct, valve_data=valve_data, baseline_values=baseline,
             formula="avg((100000-x)/5)/10")
    print(f"  [OK] 激活阀值_全局数据.3D.npz")

def generate_branches_plots(baseline, other_const):
    mech_name = "Calculation_formula_number_branches_associative_tree"
    mech_path = os.path.join(DATA_ROOT, mech_name)
    img_dir = os.path.join(mech_path, "图片")
    data_dir = os.path.join(mech_path, "3D数据")
    nt_pct = np.linspace(0, 100, 50)
    colors = ["#F44336","#E91E63","#9C27B0","#673AB7","#3F51B5","#2196F3","#00BCD4","#009688","#4CAF50"]

    print(f"\n[{mech_name}] 生成联想分支数可视化...")
    all_branches = []
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        branches = []
        for pct in nt_pct:
            args = list(other_const)
            args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
            branches.append(calculate_branches(*args))
        all_branches.append(branches)

    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("联想分支树分支数 - 神经递质浓度影响分析", fontsize=14, fontweight="bold")
    ax1 = fig.add_subplot(221)
    for i, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        ax1.plot(nt_pct, all_branches[i], color=colors[i], linewidth=2, label=name_cn)
    ax1.set_xlabel("神经递质浓度 (%)", fontsize=11)
    ax1.set_ylabel("分支数", fontsize=11)
    ax1.set_title("各神经递质对联想分支数的影响曲线", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=8, loc="upper left", ncol=3)
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(222, projection="3d")
    X, Y = np.meshgrid(nt_pct, np.arange(9))
    Z = np.array(all_branches)
    ax2.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.85, linewidth=0, antialiased=True)
    ax2.set_xlabel("递质浓度 (%)", fontsize=10)
    ax2.set_ylabel("递质编号", fontsize=10)
    ax2.set_zlabel("分支数", fontsize=10)
    ax2.set_title("联想分支数三维分布图", fontsize=12, fontweight="bold")
    ax2.view_init(elev=25, azim=135)

    baseline_branch = calculate_branches(*other_const)
    changes = []
    for neuro_index in range(9):
        high_args = list(other_const); high_args[neuro_index] = NT_MAX
        low_args = list(other_const); low_args[neuro_index] = NT_MIN
        changes.append({"name": NEUROTRANSMITTERS[neuro_index][0], "high": calculate_branches(*high_args), "low": calculate_branches(*low_args), "baseline": baseline_branch})

    ax3 = fig.add_subplot(223)
    x_pos = np.arange(9)
    ax3.bar(x_pos - 0.3, [c["low"] for c in changes], 0.3, label="低浓度", color="#2196F3")
    ax3.bar(x_pos, [c["baseline"] for c in changes], 0.3, label="基准值", color="#4CAF50")
    ax3.bar(x_pos + 0.3, [c["high"] for c in changes], 0.3, label="高浓度", color="#F44336")
    ax3.set_xlabel("神经递质", fontsize=11)
    ax3.set_ylabel("分支数", fontsize=11)
    ax3.set_title("各神经递质高低浓度下的联想分支数对比", fontsize=12, fontweight="bold")
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([c["name"] for c in changes], rotation=45, fontsize=9)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    ax4 = fig.add_subplot(224)
    sensitivity = [abs(c["high"] - c["low"]) / c["baseline"] * 100 for c in changes]
    ax4.barh([c["name"] for c in changes], sensitivity, color=colors)
    ax4.set_xlabel("分支数变化敏感度 (%)", fontsize=11)
    ax4.set_ylabel("神经递质", fontsize=11)
    ax4.set_title("各神经递质对联想分支数的敏感度", fontsize=12, fontweight="bold")
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "联想分支数_神经递质影响.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 联想分支数_神经递质影响.png")

    fig3d = plt.figure(figsize=(12, 10))
    ax = fig3d.add_subplot(111, projection="3d")
    for i, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        ax.plot(nt_pct, [i]*len(nt_pct), all_branches[i], color=colors[i], linewidth=2.5, label=name_cn)
    ax.scatter([50]*9, np.arange(9), [baseline_branch]*9, c="gold", s=100, marker="*", label="基准状态")
    ax.set_xlabel("神经递质浓度 (%)", fontsize=11)
    ax.set_ylabel("神经递质类型", fontsize=11)
    ax.set_zlabel("分支数", fontsize=11)
    ax.set_title("联想分支数三维分布图（可旋转查看）", fontsize=13, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")
    ax.view_init(elev=30, azim=60)
    plt.savefig(os.path.join(img_dir, "联想分支数_三维分布图.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 联想分支数_三维分布图.png")

    fig_compare = plt.figure(figsize=(16, 10))
    fig_compare.suptitle("激活阀值与联想分支数对比分析", fontsize=14, fontweight="bold")
    nt_pct_all = np.linspace(0, 100, 50)
    all_valves = []
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        valves = []
        for pct in nt_pct_all:
            args = list(other_const)
            args[neuro_index] = NT_MIN + (pct / 100) * (NT_MAX - NT_MIN)
            valves.append(calculate_activation_valve(*args))
        all_valves.append(valves)

    ax1 = fig_compare.add_subplot(121)
    for i, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        ax1.scatter(all_valves[i], all_branches[i], color=colors[i], alpha=0.7, label=name_cn)
    ax1.set_xlabel("激活阀值", fontsize=11)
    ax1.set_ylabel("联想分支数", fontsize=11)
    ax1.set_title("激活阀值 vs 联想分支数散点图", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    ax2 = fig_compare.add_subplot(122)
    corr_coeffs = [np.corrcoef(all_valves[i], all_branches[i])[0, 1] for i in range(9)]
    ax2.bar([n[0] for n in NEUROTRANSMITTERS], corr_coeffs, color=colors)
    ax2.set_xlabel("神经递质", fontsize=11)
    ax2.set_ylabel("相关性系数", fontsize=11)
    ax2.set_title("激活阀值与分支数的相关性", fontsize=12, fontweight="bold")
    ax2.set_xticks(np.arange(9))
    ax2.set_xticklabels([n[0] for n in NEUROTRANSMITTERS], rotation=45, fontsize=9)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "激活阀值与分支数对比图.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] 激活阀值与分支数对比图.png")

    branch_data = {}
    for neuro_index, (name_cn, name_en) in enumerate(NEUROTRANSMITTERS):
        branch_data[name_en] = all_branches[neuro_index]
    np.savez(os.path.join(data_dir, "联想分支数_全局数据.3D.npz"),
             nt_percent=nt_pct, branch_data=branch_data, baseline_values=baseline,
             formula="avg(x/1000 for dopamine-like, avg((100000-x)/1000 for others))")
    print(f"  [OK] 联想分支数_全局数据.3D.npz")

def main():
    print("=" * 60)
    print("Waip AGI 三大机制3D可视化生成器")
    print("=" * 60)
    print(f"\n数据根目录: {DATA_ROOT}")
    print("\n[1/4] 创建并清空目录结构...")
    setup_folders()
    baseline = {
        "多巴胺": 35000, "乙酰胆碱": 25000, "血清素": 50000, "内啡肽": 40000,
        "P物质": 15000, "肾上腺素": 20000, "去甲肾上腺素": 22000, "GABA": 30000, "谷氨酸": 25000
    }
    other_const = [baseline[n] for n, e in NEUROTRANSMITTERS]
    generate_attention_plots(baseline, other_const)
    generate_valve_plots(baseline, other_const)
    generate_branches_plots(baseline, other_const)
    print("\n" + "=" * 60)
    print("全部完成！三大机制数据已保存至:")
    print(f"  {os.path.join(DATA_ROOT, 'Text_Attention_Algorithm')}")
    print(f"  {os.path.join(DATA_ROOT, 'calculate_activation_valve')}")
    print(f"  {os.path.join(DATA_ROOT, 'Calculation_formula_number_branches_associative_tree')}")
    print("=" * 60)

if __name__ == "__main__":
    main()