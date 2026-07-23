# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

def build_exe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gui_dir = os.path.dirname(script_dir)
    app_dir = os.path.dirname(gui_dir)
    
    exe_dir = os.path.join(app_dir, "Waip AI DRN 5.0")
    
    print(f"源代码目录: {script_dir}")
    print(f"目标目录: {exe_dir}")
    
    if os.path.exists(exe_dir):
        print("清理旧文件...")
        shutil.rmtree(exe_dir)
    
    os.makedirs(exe_dir)
    
    print("复制文件...")
    items_to_copy = [
        "意识体",
        "main",
        "img"
    ]
    
    for item in items_to_copy:
        src = os.path.join(script_dir, item)
        dst = os.path.join(exe_dir, item)
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"  已复制: {item}")
    
    main_py = os.path.join(script_dir, "main.py")
    
    print("\n开始PyInstaller打包...")
    print("提示：PyInstaller打包的exe虽然不如Nuitka保护强，但也难以反编译")
    pyinstaller_cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "Waip AI DRN 5.0",
        "--icon", os.path.join(script_dir, "img", "Waip AI.png"),
        "--distpath", exe_dir,
        "--workpath", os.path.join(script_dir, "build"),
        "--clean",
        "--hidden-import", "psutil",
        "--hidden-import", "typing_extensions",
        "--hidden-import", "json5",
        "--hidden-import", "PyQt5.QtWidgets",
        "--hidden-import", "PyQt5.QtGui",
        "--hidden-import", "PyQt5.QtCore",
        main_py
    ]
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("\n打包成功！")
        
        if os.path.exists(os.path.join(script_dir, "build")):
            shutil.rmtree(os.path.join(script_dir, "build"))
        if os.path.exists(os.path.join(script_dir, "Waip AI DRN 5.0.spec")):
            os.remove(os.path.join(script_dir, "Waip AI DRN 5.0.spec"))
        
        print("\n清理完成！")
        print(f"\n最终文件位置: {exe_dir}")
        print(f"\nexe文件: {os.path.join(exe_dir, 'Waip AI DRN 5.0.exe')}")
        
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
