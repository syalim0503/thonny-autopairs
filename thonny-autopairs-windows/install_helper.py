"""
Copies autopairs.py into Thonny's plugin folder.

- Inside Thonny: open this file and press F5 (Run) with Thonny's default interpreter.
- As thonny-autopairs-setup.exe (built by .github/workflows/release.yml): finds Thonny's
  python.exe and asks it for the plugin folder, because that folder depends on Thonny's
  Python version, portable mode and THONNY_USER_DIR.
"""

import os
import shutil
import subprocess
import sys

FROZEN = getattr(sys, "frozen", False)
QUERY = (
    "import sys, thonny; "
    "sys.stdout.buffer.write(thonny.get_sys_path_directory_containg_plugins().encode('utf-8'))"
)


def source_file():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "thonnycontrib", "autopairs.py")


def find_thonny_python():
    for var in ("LOCALAPPDATA", "ProgramFiles", "ProgramFiles(x86)"):
        root = os.environ.get(var)
        if root:
            subdir = ("Programs", "Thonny") if var == "LOCALAPPDATA" else ("Thonny",)
            candidate = os.path.join(root, *subdir, "python.exe")
            if os.path.isfile(candidate):
                return candidate

    print("Thonny 설치 폴더를 찾지 못했습니다.")
    print("Thonny 폴더 경로를 붙여넣고 Enter를 누르세요.")
    print("  (Thonny 바로가기 우클릭 > 파일 위치 열기로 찾을 수 있습니다)")
    entered = input("경로: ").strip().strip('"')
    candidate = entered if os.path.isfile(entered) else os.path.join(entered, "python.exe")
    if not entered or not os.path.isfile(candidate):
        raise SystemExit("그 폴더에서 python.exe를 찾지 못했습니다. 설치를 취소합니다.")
    return candidate


def plugins_dir():
    if not FROZEN:
        try:
            import thonny

            return thonny.get_sys_path_directory_containg_plugins()
        except ImportError:
            pass

    result = subprocess.run([find_thonny_python(), "-I", "-c", QUERY], capture_output=True)
    if result.returncode != 0 or not result.stdout:
        raise SystemExit("Thonny에서 플러그인 폴더를 알아내지 못했습니다.\n"
                         + result.stderr.decode("utf-8", "replace"))
    return result.stdout.decode("utf-8")


def main():
    target_dir = os.path.join(plugins_dir(), "thonnycontrib")
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(source_file(), target_dir)
    print("설치 완료:", os.path.join(target_dir, "autopairs.py"))
    print("Thonny를 껐다가 다시 열면 적용됩니다.")


if __name__ == "__main__":
    if FROZEN:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    code = 0
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            print(e.code if isinstance(e.code, str) else "설치에 실패했습니다.")
            code = 1
    except Exception as e:
        print("설치에 실패했습니다:", e)
        code = 1
    if FROZEN:
        try:
            input("\nEnter를 누르면 창이 닫힙니다.")
        except EOFError:
            pass
    sys.exit(code)
