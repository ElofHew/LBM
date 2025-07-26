# Leaf Boot Manager - v1.0 - Source Code
"""
# Leaf Boot Manager
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
import threading
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
lbm_error_log = os.path.join(lbm_path, "error.log")

class Features:
    # 定义功能类
    def __init__(self):
        pass

    def clear_screen(self):
        os.system("cls" if os_type == "Windows" else "clear")

class Actions:
    # 定义操作类
    def __init__(self):
        pass

    def shutdown(self):
        Features().clear_screen()
        sys.exit(0)

    def st_with_error(self, error_code):
        input("(Press Enter to shutdown...)")
        Features().clear_screen()
        if error_code.isdigit():
            sys.exit(int(error_code))
        else:
            sys.exit(1)

    def reboot(self):
        Features().clear_screen()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()

    def rb_with_error(self):
        input("(Press Enter to reboot...)")
        Features().clear_screen()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()
    
    def rb_to_rec(self):
        input("(Press Enter to reboot to recovery mode...)")
        Features().clear_screen()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()

class BootSystem:
    """定义系统启动类"""
    def __init__(self, data_list):
        self.name = data_list.get("name", "Unknown")
        self.ename = data_list.get("ename", "Unknown")
        self.path = data_list.get("path", "")
        self.workdir = data_list.get("workdir", "")
        self.mainfile = data_list.get("mainfile", "")
        self.version = data_list.get("version", None)
        self.vercode = data_list.get("vercode", None)
        self.need_venv = data_list.get("need_venv", True)
        self.min_python = data_list.get("min_python", None)
        self.support_os = data_list.get("support_os", [])
    
    def main(self):
        try:
            check_os_path_result = self.check_os_path()
            if check_os_path_result != 0:
                return 1
            check_support_os_result = self.check_support_os()
            if check_support_os_result != 0:
                return 1
            # Check and return
            if self.need_venv:
                self.venv_path = self.check_venv()
                if self.venv_path == 1:
                    return 1
            if self.min_python:
                check_python_version_result = self.check_python_version()
                if check_python_version_result == 1:
                    return 1
            # Boot Fake OS
            start_system_result = self.start_system()
            os.chdir(boot_path)
            return start_system_result
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def check_os_path(self):
        try:
            if self.workdir and self.mainfile:
                os_path = os.path.join(self.workdir, self.mainfile)
                if os.path.exists(os_path):
                    self.fos_workdir = Path(self.workdir).resolve()
                    self.fos_mainfile = self.mainfile
                    return 0
                else:
                    print(f"{Fore.RED}Error: System file does not exist.{Style.RESET_ALL}")
                    return 1
            if self.path:
                if os.path.exists(self.path):
                    self.fos_path = self.path
                    return 0
                else:
                    print(f"{Fore.RED}Error: System file does not exist.{Style.RESET_ALL}")
                    return 1
            print(f"{Fore.RED}Error: System file does not exist.{Style.RESET_ALL}")
            return 1
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
            if int(get_version[0]) > int(imp_version[0]):
                return 0
            if int(get_version[1]) < int(imp_version[1]):
                print(f"{Fore.RED}Error: This Fake OS need Python {self.min_version} or higher, but your system has Python {current_version}. Please upgrade your Python version.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check Python version. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_venv(self):
        try:
            venvname = self.ename.lower()
            venvs_path = os.path.join(lbm_path, "pyvenv")
            if not os.path.exists(venvs_path):
                os.makedirs(venvs_path)
            current_venv = os.path.join(venvs_path, venvname)
            if not os.path.exists(current_venv):
                print(f"{Fore.YELLOW}WARNING: Virtual environment {venvname} does not exist. Creating...{Style.RESET_ALL}")
                os.chdir(venvs_path)
                make_venv = subprocess.run(["python" if os_type == "Windows" else "python3", "-m", "venv", venvname])
                if make_venv.returncode != 0:
                    print(f"{Fore.RED}Error: Failed to create virtual environment {venvname}.{Style.RESET_ALL}")
                    return 1
            return current_venv
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to create virtual environment {venvname}. Error message: {e}{Style.RESET_ALL}")
            return 1
        finally:
            os.chdir(boot_path)
    
    def start_system(self):
        try:
            boot_arg = ["--boot", "--regular"]
            if self.fos_workdir and self.fos_mainfile:
                work_path = self.fos_workdir
                file_name = self.fos_mainfile
            else:
                if self.fos_path:
                    work_path = os.path.dirname(self.fos_path)
                    file_name = os.path.basename(self.fos_path)
                else:
                    print(f"{Fore.RED}Error: System file does not exist.{Style.RESET_ALL}")
                    return 1
            if self.venv_path:
                pyexec = os.path.join(self.venv_path, "Scripts" if os_type == "Windows" else "bin", "python.exe" if os_type == "Windows" else "python")
            else:
                pyexec = "python" if os_type == "Windows" else "python3"
            os.chdir(work_path)
            start_system = subprocess.run([pyexec, file_name] + boot_arg)
            # Get Return Code
            sys_rtn_code = start_system.returncode
            if sys_rtn_code == 0:
                return 0
            else:
                return sys_rtn_code
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            return 1

def check_lbm_config():
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

def get_return_code(return_code=None):
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
            Actions().st_with_error(return_code)
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
            print("(Press Enter to reboot to recovery mode...)")
            Actions().rb_to_rec()
        elif return_code == 16:
            # 启动参数错误
            print(f"{Fore.RED}Error: Boot Arguments invalid.{Style.RESET_ALL}")
            Actions().rb_with_error()
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
        print(f"{int((terminal_width-17)/2) * ' '}{Fore.CYAN}Leaf Boot Manager{Style.RESET_ALL}{int((terminal_width-17)/2) * ' '}")
        print("=" * terminal_width)
        print(f"{Fore.LIGHTGREEN_EX}0. Shutdown{Style.RESET_ALL}")
        with open(lbm_system_file, "r") as lbm_system_file_obj:
            system_data = json.load(lbm_system_file_obj)
        for key, value in system_data.items():
            f_name = value.get("name", "Unknown name of this system.")
            f_version = value.get("version", "NaN")
            print(f"{Fore.LIGHTGREEN_EX}{key}. {f_name} - {f_version}{Style.RESET_ALL}")
        print("=" * terminal_width)
        return_code = None  # 初始化return_code
        while True:
            choice = input(f"{Fore.LIGHTBLUE_EX}>>> {Style.RESET_ALL}")
            if choice == "0":
                print(f"{Fore.LIGHTRED_EX}Shutting down...{Style.RESET_ALL}")
                sys.exit(0)
            elif choice.isdigit() and int(choice) in [int(k) for k in system_data.keys()]:  # 将choice转换为整数并与字典的整数键比较
                system_path = system_data[choice].get("path", "")
                if os.path.exists(system_path):
                    print(f"{Fore.LIGHTGREEN_EX}Starting system {system_data[choice]['name']}...{Style.RESET_ALL}")
                    time.sleep(0.5)
                    # Get Informations of the Fake Operating System
                    fos_data_list = system_data.get(choice, {})
                    # BootSystem Class
                    return_code = BootSystem(fos_data_list).main()
                    break
                else:
                    print(f"{Fore.RED}System {system_data[choice]['name']} does not exist.{Style.RESET_ALL}")
                    continue
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                continue
        get_return_code(return_code)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}WARNING: Shutdown initiated by user.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    Features().clear_screen()
    check_lbm_config()
    main()
