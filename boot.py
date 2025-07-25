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
import platform
import subprocess
import shutil
from pathlib import Path
from colorama import Fore, Style, Back
from colorama import init as cinit

cinit(autoreset=True)

boot_path = os.path.dirname(os.path.abspath(__file__))
os_type = platform.system()

terminal_width = shutil.get_terminal_size().columns
terminal_height = shutil.get_terminal_size().lines

lbm_path = os.path.join(os.path.expanduser("~"), ".lbm")
lbm_config_file = os.path.join(lbm_path, "config.json")
lbm_system_file = os.path.join(lbm_path, "system.json")

class BootSystem:
    def __init__(self, name, ename, path, version, vercode, need_venv, min_python, support_os):
        self.name = name
        self.ename = ename
        self.path = path        
        self.version = version
        self.vercode = vercode
        self.need_venv = need_venv
        self.min_python = min_python
        self.support_os = support_os
        try:
            check_os_path_result = self.check_os_path(self.path)
            if check_os_path_result != 0:
                return 1
            check_support_os_result = self.check_support_os(self.support_os)
            if check_support_os_result != 0:
                return 1
            if self.need_venv:
                self.venv_path = self.check_venv(self.ename)
                if self.venv_path == 1:
                    return 1
            if self.min_python:
                check_python_version_result = self.check_python_version(self.min_python)
                if check_python_version_result == 1:
                    return 1
            # Boot Fake OS
            start_system_result = self.start_system(self.venv_path if self.need_venv else None, self.path)
            if start_system_result in [0, 100]:
                return 0
            elif start_system_result == 101:
                return 1
            else:
                return 2
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def check_os_path(self, os_path):
        try:
            if not os.path.exists(os_path):
                print(f"{Fore.RED}Error: The path of this Fake OS does not exist.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check path. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_support_os(self, support_os):
        try:
            if os_type not in support_os:
                print(f"{Fore.RED}Error: This system is not supported by this Fake Operating System.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check support OS. Error message: {e}{Style.RESET_ALL}")        
            return 1

    def check_python_version(self, min_version):
        try:
            current_version = platform.python_version()
            get_version = current_version.split(".")
            imp_version = min_version.split(".")
            if int(imp_version[0]) == 2:
                print(f"{Fore.RED}Error: Leaf Boot Manager only supports Python 3.{Style.RESET_ALL}")
                return 1
            if int(get_version[1]) < int(imp_version[1]):
                print(f"{Fore.RED}Error: This Fake OS need Python {min_version} or higher, but your system has Python {current_version}. Please upgrade your Python version.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check Python version. Error message: {e}{Style.RESET_ALL}")
            return 0

    def check_venv(self, ename):
        try:
            venvname = ename.lower()
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
    
    def start_system(self, venv_path, os_path):
        try:
            boot_arg = ["--boot", "--regular"]
            if venv_path:
                pyexec = os.path.join(venv_path, "Scripts" if os_type == "Windows" else "bin", "python.exe" if os_type == "Windows" else "python")
            else:
                pyexec = "python" if os_type == "Windows" else "python3"
            os.chdir(os_path)
            start_system = subprocess.run([pyexec, "main.py"] + boot_arg)
            # Get Return Code
            sys_rtn_code = start_system.returncode
            if sys_rtn_code == 0:
                os.chdir(boot_path)
                return 0
            elif sys_rtn_code == 11:
                return 101
            elif sys_rtn_code == 12:
                print(f"{Fore.YELLOW}WARNING: This OS returned 12, Thats means an unfinished feature.{Style.RESET_ALL}")
                return 100
            elif sys_rtn_code == 16:
                print(f"{Fore.YELLOW}WARNING: Boot Argument not correct.{Style.RESET_ALL}")
                return 101
            elif sys_rtn_code == 19:
                print(f"{Fore.YELLOW}WARNING: This OS catched some errors.{Style.RESET_ALL}")
                return 100
            else:
                print(f"{Fore.YELLOW}WARNING: This OS returned an unknown code: {sys_rtn_code}.{Style.RESET_ALL}")
                return 100
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)

def check_lbm_config():
    try:
        if not os.path.exists(lbm_path):
            os.makedirs(lbm_path)
        if not os.path.exists(lbm_config_file):
            config_file_data = {
                "name": "Leaf Boot Manager",
                "path": boot_path,
                "version": "1.0",
                "vcode": "1000",
                "default": "0",
                "timeout": "10"
            }
            with open(lbm_config_file, "w") as new_lbm_config_file:
                json.dump(config_file_data, new_lbm_config_file, indent=4)
            new_lbm_config_file.close()
        if not os.path.exists(lbm_system_file):
            with open(lbm_system_file, "w") as new_lbm_system_file:
                json.dump({}, new_lbm_system_file, indent=4)
            new_lbm_system_file.close()
    except Exception as e:
        print(f"{Fore.RED}Error: Have some problems when creating config file. Error message: {e}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    try:
        print(f"{int((terminal_width-17)/2) * " "}{Fore.CYAN}Leaf Boot Manager{Style.RESET_ALL}{int((terminal_width-17)/2) * " "}")
        print("=" * terminal_width)
        print(f"{Fore.LIGHTGREEN_EX}0. Shutdown{Style.RESET_ALL}")
        with open(lbm_system_file, "r") as lbm_system_file_obj:
            system_data = json.load(lbm_system_file_obj)
        if not system_data:
            pass
        else:
            index = 1
            for index in system_data:
                f_name = system_data[str(index)].get("name", "Unknown name of this system.")
                f_version = system_data[str(index)].get("version", "NaN")
                print(f"{Fore.LIGHTGREEN_EX}{index}. {f_name} - {f_version}{Style.RESET_ALL}")
                index += 1
        print("=" * terminal_width)
        while True:
            choice = input(f"{Fore.LIGHTBLUE_EX}>>> {Style.RESET_ALL}")
            if choice == "0":
                print(f"{Fore.LIGHTRED_EX}Shutting down...{Style.RESET_ALL}")
                sys.exit(0)
            elif choice.isdigit() and str(choice) in system_data:
                system_path = system_data[str(choice)].get("path", "")
                if os.path.exists(system_path):
                    print(f"{Fore.LIGHTGREEN_EX}Starting system {system_data[str(choice)]['name']}...{Style.RESET_ALL}")
                    time.sleep(0.5)
                    # Get Informations of the Fake Operating System
                    fos_name = system_data.get(index, {}).get("name", "Unknown")
                    fos_ename = system_data.get(index, {}).get("ename", "Unknown")
                    fos_path = system_data.get(index, {}).get("path", "")
                    fos_version = system_data.get(index, {}).get("version", None)
                    fos_vercode = system_data.get(index, {}).get("vercode", None)
                    need_venv = system_data.get(index, {}).get("need_venv", True)
                    min_python = system_data.get(index, {}).get("min_python", None)
                    support_os = system_data.get(index, {}).get("support_os", [])
                    # BootSystem Class
                    return_code = BootSystem(fos_name, fos_ename, fos_path, fos_version, fos_vercode, need_venv, min_python, support_os)
                    break
                else:
                    print(f"{Fore.RED}System {system_data[str(choice)]['name']} does not exist.{Style.RESET_ALL}")
                    continue
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                continue
        if return_code == 0:
            sys.exit(0)
        elif return_code == 1:
            pass
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Shutting down...{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    check_lbm_config()
    while True:
        main()
