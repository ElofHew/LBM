# Leaf Boot Manager - v1.0 - Source Code
"""
@ name: Leaf Boot Manager
@ author: ElofHew
@ date: 2025-07-18
@ version: 1.0
@ license: GNU General Public License v3.0
@ copyright: (c) 2025 Oak Studio. All rights reserved.
@ description: This is a Boot Manager for Python Fake Operating Systems.
"""

import os
import sys
import time
import json
import shutil
import platform
import subprocess
from pathlib import Path
from colorama import Fore, Style, Back
from colorama import init as cinit

cinit(autoreset=True)

# 定义全局变量
boot_path = os.path.dirname(os.path.abspath(__file__))
os_type = platform.system()

terminal_width = shutil.get_terminal_size().columns
terminal_height = shutil.get_terminal_size().lines

lbm_path = os.path.join(os.path.expanduser("~"), ".lbm")
lbm_config_file = os.path.join(lbm_path, "config.json")
lbm_system_file = os.path.join(lbm_path, "system.json")

lbm_error_log = os.path.join(lbm_path, "logs", "error.log")

def cs(): os.system("cls" if os_type == "Windows" else "clear")

class Actions:
    """定义操作类"""
    def __init__(self):
        pass

    def shutdown(self):
        cs()
        sys.exit(0)

    def st_with_error(self, error_code):
        input("(Press Enter to shutdown...)")
        cs()
        if isinstance(error_code, int):
            sys.exit(error_code)
        else:
            sys.exit(1)

    def reboot(self):
        cs()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()

    def rb_with_error(self):
        input("(Press Enter to reboot...)")
        cs()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()
    
    def rb_to_rec(self):
        input("(Press Enter to reboot to recovery mode...)")
        cs()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()
        # 重启到recovery模式，暂未实现

class BootSystem:
    """定义系统启动类"""
    def __init__(self, data_list):
        self.name = data_list.get("name", "")
        self.ename = data_list.get("ename", "")
        self.version = data_list.get("version", "Unknown")
        self.vercode = data_list.get("vercode", "0000")
        self.setup_date = data_list.get("setup_date", "1970-01-01")
        self.need_venv = data_list.get("need_venv", "")
        self.min_python = data_list.get("min_python", "")
        self.support_os = data_list.get("support_os", [])
        self.boot_class = data_list.get("boot_class", "")
        self.work_file = data_list.get("work_file", "")
        self.work_path = data_list.get("work_path", "")

    # 启动主函数
    def main(self):
        try:
            # 检查该伪系统的路径是否存在
            check_os_path_result = self.check_os_path()
            if check_os_path_result != 0:
                return 1
            # 检查父操作系统是否受支持
            check_support_os_result = self.check_support_os()
            if check_support_os_result != 0:
                return 1
            # 检查Python版本是否满足最低要求
            check_python_version_result = self.check_python_version()
            if check_python_version_result == 1:
                return 1
            # 检查是否需要虚拟环境
            self.venv_path_result = self.check_venv()
            if self.venv_path_result == 1:
                return 1
            # 是时候启动了孩子们（）
            start_system_result = self.start_system()
            return start_system_result
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)
        finally:
            os.chdir(boot_path)
    
    def check_os_path(self):
        try:
            if not os.path.exists(self.work_path):
                print(f"{Fore.RED}Error: System work path does not exist.{Style.RESET_ALL}")
                return 1
            if not os.path.exists(self.work_file):
                print(f"{Fore.RED}Error: System work file does not exist.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check path. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_support_os(self):
        try:
            if os_type not in self.support_os:
                print(f"{Fore.RED}Error: This system is not supported by this Fake Operating System.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check support OS. Error message: {e}{Style.RESET_ALL}")        
            return 1

    def check_python_version(self):
        try:
            current_version = platform.python_version()
            get_version = current_version.split(".")
            imp_version = self.min_python.split(".")
            if int(imp_version[0]) == 2:
                print(f"{Fore.RED}Error: Leaf Boot Manager only supports Python 3.{Style.RESET_ALL}")
                return 1
            elif int(get_version[0]) < int(imp_version[0]):
                print(f"{Fore.RED}Error: This Fake OS need Python {self.min_python} or higher, but your system has Python {current_version}. Please upgrade your Python version.{Style.RESET_ALL}")
                return 1
            elif int(get_version[1]) < int(imp_version[1]):
                print(f"{Fore.RED}Error: This Fake OS need Python {self.min_python} or higher, but your system has Python {current_version}. Please upgrade your Python version.{Style.RESET_ALL}")
                return 1
            else:
                return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check Python version. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_venv(self):
        try:
            venvname = self.ename.lower()
            venvs_path = os.path.join(lbm_path, "pyvenv")
            current_venv = os.path.join(venvs_path, venvname)
            executable_path = os.path.join(current_venv, "Scripts" if os_type == "Windows" else "bin", "python.exe" if os_type == "Windows" else "python")
            if not os.path.exists(executable_path):
                print(f"{Fore.YELLOW}WARNING: Virtual environment {venvname} does not exist. Creating...{Style.RESET_ALL}")
                if os.path.exists(current_venv):
                    shutil.rmtree(current_venv)
                os.chdir(venvs_path)
                make_venv = subprocess.run(["python" if os_type == "Windows" else "python3", "-m", "venv", venvname])
                if make_venv.returncode != 0:
                    print(f"{Fore.RED}Error: Failed to create virtual environment {venvname}.{Style.RESET_ALL}")
                    return 1
            self.venv_exec = executable_path
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to create virtual environment {venvname}. Error message: {e}{Style.RESET_ALL}")
            return 1
        finally:
            os.chdir(boot_path)
    
    def start_system(self):
        try:
            # 准备启动专用的参数
            if self.boot_class == "system":
                boot_arg = ["--boot", "--regular"]
            elif self.boot_class == "recovery":
                boot_arg = ["--boot", "--recovery"]
            else:
                boot_arg = []
            # 准备系统工作路径和主文件名
            work_path = self.work_path
            work_file = self.work_file
            # 根据是否需要虚拟环境来决定使用的Python解释器
            if self.need_venv:
                pyexec = self.venv_exec
            else:
                pyexec = "python" if os_type == "Windows" else "python3"
            # 正式启动系统
            os.chdir(work_path)
            system_process = subprocess.run([pyexec, work_file] + boot_arg)
            # 获取该伪系统的返回码并返回到上层
            return system_process.returncode
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            return 1

class CheckConfig:
    """定义配置文件检查类"""
    def __init__(self):
        self.check_lbm_config()
        self.check_config_full()

    def check_lbm_config(self):
        """检查并创建Leaf Boot Manager的配置文件"""
        try:
            if not os.path.exists(lbm_path):
                os.makedirs(lbm_path)
            if not os.path.exists(lbm_config_file):
                config_file_data = {
                    "name": "Leaf Boot Manager",
                    "path": boot_path,
                    "version": "1.0",
                    "vcode": "1000"
                }
                with open(lbm_config_file, "w") as new_lbm_config_file:
                    json.dump(config_file_data, new_lbm_config_file, indent=4)
            if not os.path.exists(lbm_system_file):
                with open(lbm_system_file, "w") as new_lbm_system_file:
                    json.dump({}, new_lbm_system_file, indent=4)
        except Exception as e:
            print(f"{Fore.RED}Error: Have some problems when creating config file. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def check_config_full(self):
        """检查LBM配置文件完整性"""
        try:
            lbm_config = {
                "name": "Leaf Boot Manager",
                "path": boot_path,
                "version": "1.0",
                "vcode": "1000"
            }
            with open(lbm_config_file, "r+") as lbm_config_data:  # 修正这里
                config_data = json.load(lbm_config_data)
                modified = False
                # 检查并更新默认值
                for key, value in lbm_config.items():
                    if key not in config_data:
                        config_data[key] = value
                        modified = True
                # 只有在配置有修改时才写入文件
                if modified:
                    lbm_config_data.seek(0)  # 将文件指针移到文件开头
                    json.dump(config_data, lbm_config_data, indent=4)
                    lbm_config_data.truncate()  # 截断文件以去除多余内容
                return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

def get_return_code(return_code=None):
    """根据返回值执行相应操作"""
    try:
        # 根据返回值执行相应操作
        if return_code is None:
            print(f"{Fore.RED}Error: No valid system was selected.{Style.RESET_ALL}")
            Actions().st_with_error(1)
        elif return_code == 0:
            # 正常关机
            Actions().shutdown()
        elif return_code == 1:
            # 启动前检查环节出错
            print(f"{Fore.RED}Error: Failed to start system. Please check the system configuration.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 11:
            # 重新启动
            Actions().reboot()
        elif return_code == 12:
            # 未完成的功能
            print(f"{Fore.YELLOW}WARNING: This Fake OS want to boot into an unfinished feature.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 13:
            # 系统启动失败
            print(f"{Fore.RED}Error: Boot Fake OS failed.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 14:
            # 系统崩溃
            print(f"{Fore.RED}Error: This Fake OS has crashed.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 15:
            # 重启至恢复模式
            Actions().rb_to_rec()
        elif return_code == 16:
            # 启动参数错误
            print(f"{Fore.RED}Error: Boot Arguments invalid.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 17:
            # Ctrl+C被触发
            print(f"{Fore.YELLOW}WARNING: Shutdown initiated by user.{Style.RESET_ALL}")
            Actions().st_with_error()
        elif return_code == 19:
            # 捕捉到异常错误
            print(f"{Fore.RED}Error: This Fake OS caught an exception error.{Style.RESET_ALL}")
            Actions().rb_with_error()
        else:
            # 未知错误
            print(f"{Fore.RED}Error: Unknown error. Code: {return_code}{Style.RESET_ALL}")
            Actions().st_with_error(return_code)
    except Exception as e:
        print(f"{Fore.RED}Error: Failed to handle return code. Error message: {e}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    """主函数"""
    try:
        # 读取系统启动项列表
        with open(lbm_system_file, "r") as lbm_system_file_obj:
            system_data = json.load(lbm_system_file_obj)

        # 绘制启动菜单
        print(f"{int((terminal_width-17)/2) * ' '}{Fore.CYAN}Leaf Boot Manager{Style.RESET_ALL}{int((terminal_width-17)/2) * ' '}")
        print("=" * terminal_width)
        print(f"{Fore.LIGHTGREEN_EX}0. Shutdown{Style.RESET_ALL}")
        for key, value in system_data.items():
            f_name = value.get("name", "Unknown Name")
            f_version = value.get("version", "NaN")
            print(f"{Fore.LIGHTGREEN_EX}{key}. {f_name} - {f_version}{Style.RESET_ALL}")
        print("=" * terminal_width)

        return_code = None  # 初始化return_code

        # 选择启动项
        while True:
            choice = input(f"{Fore.LIGHTBLUE_EX}>>> {Style.RESET_ALL}")
            if choice == "0":
                return_code = 0
                break
            elif choice.isdigit() and int(choice) in [int(k) for k in system_data.keys()]:
                # 将choice转换为整数并与字典的整数键比较
                print(f"{Fore.LIGHTGREEN_EX}Starting system {system_data[choice]['name']}...{Style.RESET_ALL}")
                time.sleep(0.5)
                # Get Informations of the Fake Operating System
                fos_data_list = system_data.get(choice, {})
                # BootSystem Class
                return_code = BootSystem(fos_data_list).main()
                break
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                continue
        get_return_code(return_code)
    except KeyboardInterrupt:
        get_return_code(17)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    cs()
    CheckConfig()
    main()
