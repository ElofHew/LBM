# 如何使用 Leaf Boot Manager

Leaf Boot Manager 是一款开源、基于Python的Python伪系统启动器（引导程序），支持Windows、Linux、MacOS等操作系统。

## 配置文件

Leaf Boot Manager 的核心配置文件为 `config.json`，位于当前系统用户目录的 `.lbm` 文件夹中。

```json
{
    "name": "Leaf Boot Manager",
    "path": "D:\\WinDocuments\\GitHub\\LBM",
    "version": "1.0",
    "vcode": "1000"
}
```

- `name`：Leaf Boot Manager 的名称。
- `path`：Leaf Boot Manager 的安装目录。
- `version`：Leaf Boot Manager 的版本号。
- `vcode`：Leaf Boot Manager 的版本代号。

(其实这个配置文件当前可有可无，但后期会用到)

## 启动项配置文件

Leaf Boot Manager 作为启动管理器，需要一个启动项配置文件，该配置文件为 `system.json`，位于当前系统用户目录的 `.lbm` 文件夹中。

例如：

```json
{
    "1": {
        "name": "Quarter OS",
        "ename": "QOS",
        "version": "Alpha 0.2.2",
        "vercode": "0220",
        "setup_date": "2025-07-04",
        "need_venv": true,
        "min_python": "3.10",
        "support_os": ["Windows", "Linux", "Darwin"],
        "boot_class": "system",
        "work_path": "D:\\WinDocuments\\GitHub\\QOS\\QOS\\",
        "work_file": "D:\\WinDocuments\\GitHub\\QOS\\QOS\\system\\main.py"
    }
}
```

1. `name` : 启动项的名称。
2. `ename` : 启动项的简称。
3. `version` : 启动项的版本号。
4. `vercode` : 启动项的版本代号。
5. `setup_date` : 启动项的安装部署日期。
6. `need_venv` : 启动项是否需要虚拟环境。
7. `min_python` : 启动项所需的最低 Python 版本。
8. `support_os` : 启动项支持的操作系统列表<br>(Windows/Linux/macOS)。
9. `boot_class` : 启动项的启动类型。<br>(`system`表示正常伪系统，`recovery`表示系统恢复模式)
10. `work_path` : 启动项的工作目录(绝对路径)。
11. `work_file` : 启动项的主程序文件位置(绝对路径)。

其中，`need_venv`，`min_python`，`boot_class` 键值均为字符串，`support_os` 键值为列表，且这四个最为重要。

其他键值均为Leaf Boot Manager在读取启动项并将其显示出来时所需的元数据。

`work_path`：该Python伪系统的工作路径，必须是绝对路径。例如：`/home/evan/github/QOS/QOS/`。

`work_file`：该Python伪系统的主程序文件位置，必须是绝对路径。例如：`/home/evan/github/QOS/QOS/system/main.py`。

`need_venv`：该Python伪系统是否需要虚拟环境。如果该值为 `true`，Leaf Boot Manager会检查 `.lbm` 文件夹下的 `pyvenv` 文件夹内是否已有该Python伪系统专用的虚拟环境，如果没有，则会自动创建。(虚拟环境名为 `ename` 键所代表的值的小写)

`min_python`：该Python伪系统所需的最低 Python 版本，在Leaf Boot Manager启动该Python伪系统时，会检查当前系统的Python版本是否小于该值，如果小于，则会弹出提示框要求用户升级Python版本。

`boot_class`：该Python伪系统的启动类型，目前支持 `system` 和 `recovery` 两种类型。

`support_os`：该Python伪系统支持的操作系统列表，如果当前系统不在该列表中，则会提示当前系统不受支持，并退出。

## 启动Leaf Boot Manager

由于Leaf Boot Manager的相关配置文件均存放在用户目录的 `.lbm` 文件夹中，并且Leaf Boot Manager仅有一个主程序文件，因此用户不必担心路径错误导致启动失败或无法正常运行等问题。

所以，用户可以直接双击 `boot.py` 文件运行Leaf Boot Manager。

亦或是对于Windows系统，用户可以使用 `pyinstaller` 模块将文件编译为 `boot.exe` 可执行文件，双击运行该文件即可启动Leaf Boot Manager。

另外，用户也可以前往Leaf Boot Manager的 [GitHub仓库](https://github.com/ElofHew/LBM) 或 [Gitee仓库](https://gitee.com/ElofHew/LBM) 下载最新版的**已编译**的exe文件。

## 启动项管理

在使用Leaf Boot Manager时启动的Python伪系统中，应该已经自带了Leaf Boot Manager的启动项管理工具。启动命令为：`lbmmng`，同时也可携带参数启动。

- 如果没有，且该Python伪系统支持第三方软件包安装，可以前往该Python伪系统的软件仓库查看是否有名为 `lbmmng` 的软件包。

>[!TIP]
> 特殊的，对于Quarter OS，用户可以直接在终端中输入 `biscuit get lbmmng` 来安装 `lbmmng` 软件包。（通常情况下Quarter OS可能已经默认内置了 `lbmmng` 软件包）

- 如果没有，且该Python伪系统不支持第三方软件包安装，可以联系该Python伪系统的作者，寻求帮助并手动将本仓库中的 `lbmmng.py` 文件移植到该Python伪系统中。

使用 `lbmmng` 命令可以进行以下操作：

- `add`：添加启动项。
- `del`：删除启动项。
- `edit`：编辑启动项。
- `list`：列出所有启动项。
- `help`: 查看所有命令帮助。
- `backup`：备份启动项配置文件。
- `restore`：恢复启动项配置文件。

## 修复引导

如果在某些不正确的操作和一些意外情况下，Leaf Boot Manager遭到损坏，届时您可以通过以下操作来修复它：

1. 针对于支持第三方软件包的Python伪系统：

   - 安装 `lbmfix` 软件包。
   - 运行 `lbmfix` 命令。
   - 按照提示操作，修复Leaf Boot Manager。
   - 根据不同的Python伪系统，运行指定的命令来修复本Python伪系统的启动项。（例如：对于Quarter OS，首先通过Biscuit安装 `qboot`， 然后运行 `qboot fix` 命令）

2. 对于不支持第三方软件包的Python伪系统：

   - 从本仓库中提取出 `lbmfix.py` 文件。
   - 在操作系统环境中，使用 `python3` 运行 `lbmfix.py` 文件。
   - 按照提示操作，修复Leaf Boot Manager。
   - 运行 `lbmsf.py` 文件来修复本Python伪系统的启动项。

>[!WARNING]
> 修复Leaf Boot Manager后，请务必备份 `config.json` 和 `system.json` 文件，以防止数据丢失。

## 注意事项

- Leaf Boot Manager理论上可以兼容所有Python伪系统，但由于不同伪系统之间的适配力度和自身的一些已知问题，可能存在一些兼容性问题。
- Leaf Boot Manager仅支持Python伪系统，不支持真正的系统引导程序，更不能直接被当作直接在物理机上运行的引导程序。
- Leaf Boot Manager相关工具会随着版本更新而更新，请及时更新以确保避免出现兼容性问题。
- 请不要在实际生产环境中使用Leaf Boot Manager，因为它可能存在不稳定的功能或安全性问题。
- 一切最终解释权归Oak Studio所有。

---

<div align="center">

Written by [ElofHew](https://github.com/ElofHew)

&copy; 2025 [Oak Studio](https://os.drevan.xyz/). All rights reserved.

</div>