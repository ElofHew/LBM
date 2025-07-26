# 适配 Leaf Boot Manager

如果您也想为您的Python伪系统引入Leaf Boot Manager作为启动引导管理器，请参考以下步骤：

## Leaf Boot Manager 启动原理

在Leaf Boot Manager中，启动Python伪系统的主要原理为，使用 `subprocess` 模块启动Python伪系统作为子进程。

```python
import subprocess

boot_args = ["--boot", "--regular"]
subprocess.run(['python', 'path/to/your/fakeos.py'] + boot_args)
```

其中 `boot_args` 是一个列表，用于传递启动参数，例如 `--boot` 表示启动Leaf Boot Manager，`--regular` 表示启动普通模式。

所以，在您的Python伪系统中，需要导入 `sys` 模块，并使用 `sys.argv` 来获取启动参数。例如：

```python
import sys

if sys.argv[1:]:
    if sys.argv[1] == "--boot":
        if sys.argv[2] == "--regular":
            # Start regular mode
        else:
            pass
    else:
        pass
else:
    pass
```

这样，只有当启动参数 `--boot` 和 `--regular` 都存在时，才会正常启动该Python伪系统。

如果启动参数不正确，则可以打印出错误信息，并退出程序。

## 程序返回值

我们都知道，一个程序运行结束后，会返回一个值，也叫做返回代码，表示程序的运行结果。

通常如果一个程序没有在源代码中显式地返回值，则默认返回值为0。

例如在 C++ 中，我们可以用 `return` 语句来返回一个值，例如：

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, world!" << endl;
    return 0; // Return 0 to indicate successful execution
}
```

这样当程序运行结束时，会返回 0 这个值，控制权会返回到调用它的地方，通常是操作系统。

而在Python中，我们应该知道也有 `return`，但它并不是我们通常意义上的返回值，而是退出当前函数，返回一个值到调用它的地方，例如：

```python
def my_function():
    print("Hello, world!")
    return 0 # Return 0 to indicate successful execution

my_function()
```

这样当 `my_function()` 运行结束时，会返回 0 这个值，控制权会返回到调用它的语句。

而 `return` 不能放在非函数的代码内，所以当Python程序运行结束后，除非出现错误，否则不会有返回值。

所以我们需要导入 `sys` 模块，并使用 `sys.exit()` 来退出程序，并返回一个值。例如：

```python
import sys

def my_function():
    print("Hello, world!")
    sys.exit(0) # Exit program and return 0

my_function()
```

这样当 `my_function()` 运行结束时，会退出程序并返回 0 这个值，并且由于我们使用了 `sys.exit(0)`，所以返回代码就是 0。

相应的，如果我们使用 `sys.exit(114)` 来退出程序，则返回代码就是 114。

通常来说，非0值均表示程序运行出错。但是当您的Python伪系统需要与Leaf Boot Manager配合工作时，控制权会返回到Leaf Boot Manager。

## Leaf Boot Manager 接受的返回值

Leaf Boot Manager 接受的返回值有以下几种：

| 返回值 | 含义 |
| --- | --- |
| 0 | 正常关机 |
| 11 | 重新启动 |
| 12 | 预留但还未实现的功能 |
| 13 | 系统启动失败 |
| 14 | 系统崩溃 |
| 15 | 进入恢复模式 |
| 16 | 启动参数不正确 |
| 17 | Ctrl+C 被触发 |
| 19 | 捕捉到异常错误 |
| 其他 | 未知错误 |

其中，除了关机、捕捉异常、未知错误是直接退出引导以外，其他返回值均会重新进入引导程序。

## 总结

通过以上介绍，我们可以知道，在Leaf Boot Manager中，启动Python伪系统的主要原理为，使用 `subprocess` 模块启动Python伪系统作为子进程，并通过 `sys.argv` 获取启动参数。

如果启动参数不正确，则可以打印出错误信息，并退出程序。

如果程序运行结束后，没有返回值，则需要使用 `sys.exit()` 来退出程序并返回一个值。

---

<div align="center">

Written by [ElofHew](https://github.com/ElofHew)

&copy; 2025 [Oak Studio](https://os.drevan.xyz/)

</div>