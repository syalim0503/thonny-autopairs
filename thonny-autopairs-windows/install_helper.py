"""
Copies autopairs.py into the plugin folder of the Thonny whose Python runs this script.
Run with Thonny's own python.exe (install.bat does that).
"""

import os
import shutil

import thonny

here = os.path.dirname(os.path.abspath(__file__))
source = os.path.join(here, "thonnycontrib", "autopairs.py")
target_dir = os.path.join(thonny.get_sys_path_directory_containg_plugins(), "thonnycontrib")

os.makedirs(target_dir, exist_ok=True)
shutil.copy2(source, target_dir)
print("설치 완료:", os.path.join(target_dir, "autopairs.py"))
