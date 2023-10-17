import sys
from cx_Freeze import setup, Executable

# 入口点文件名称
target = "red_book.py"

# 包含的文件和目录
includes = ["PyQt5", "selenium", "settings"]
include_files = [
    ("src/desktop.ico", "src/desktop.ico"),
    ("chromedriver.exe", "chromedriver.exe"),
    ("logs/", "logs/"),
]

# 应用程序的基本信息
base = None
icon = "./src/desktop.ico"
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="小红书自动跑",
    version="2.0",
    description="The author of this piece is Qin Yu.",
    options={
        "build_exe": {
            "includes": includes,
            "include_files": include_files,
            "excludes": [],
            "optimize": 2,
        }
    },
    executables=[Executable(target, base=base, icon=icon)]
)
