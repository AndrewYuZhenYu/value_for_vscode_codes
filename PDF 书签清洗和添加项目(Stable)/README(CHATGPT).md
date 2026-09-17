下面给你一份可以直接放进项目根目录的专业版 `README.md`。我会把**用户使用部分做成快速上手型**，而**开发者部分把数据流、目录解析、页码映射、PyMuPDF API、异常处理、扩展点和潜在限制**讲清楚。

# PDF 书签清洗和添加工具

一个基于 **Python + PyMuPDF** 的 PDF 目录（书签）自动生成与 Page Labels 注入工具。

本程序从外部 `.txt` / `.md` 目录文件读取结构化目录信息，根据指定的**书面页码偏移量（Offset）**自动计算 PDF 实际物理页码，然后：

- 清除 PDF 原有书签
- 批量写入新的 PDF 书签
- 自动设置 PDF Page Labels（逻辑页码）
- 支持“前言罗马数字 + 正文阿拉伯数字”的双重页码体系
- 原始 PDF 内容本身不做重新渲染或重新编码
- 目录数据与程序代码分离，修改目录无需修改核心代码

适合用于**教材、扫描书籍、OCR PDF、电子书等文档的目录清洗与书签重建**。

---

# 一、快速开始

## 1. 安装依赖

本程序只需要一个第三方 Python 库：

```bash
pip install PyMuPDF
```

程序使用：

```python
import fitz
```

其中 `fitz` 即 PyMuPDF 的 Python 接口。

---

## 2. 准备目录文件

创建一个 `.txt` 或 `.md` 文件，例如：

```text
1|第一章 集合|1
2|1.1 集合的概念|1
2|1.2 集合的运算|8
1|第二章 命题逻辑|25
2|2.1 命题与命题联结词|25
2|2.2 命题公式|32
```

每一行使用：

```text
层级|书签标题|书面页码
```

例如：

```text
2|1.2 集合的运算|8
```

表示：

- `2`：第二级书签
- `1.2 集合的运算`：书签名称
- `8`：书籍印刷页码

程序会根据：

```text
实际 PDF 页码 = 书面页码 + OFFSET
```

自动计算 PDF 中真正需要跳转到的物理页。

---

# 二、配置程序

程序顶部有一个统一的配置区：

```python
CONFIG = {
    "TOC_FILE": "目录文件路径",
    "INPUT_PDF": "原始 PDF 路径",
    "OUTPUT_PDF": "输出 PDF 路径",
    "OFFSET": 10
}
```

正常使用时，**只需要修改这里，不需要修改下面的核心代码。**

### `TOC_FILE`

目录文件路径。

支持：

```text
.txt
.md
```

例如：

```python
"TOC_FILE": "/Users/andrewyu/Documents/离散数学目录文件.md"
```

---

### `INPUT_PDF`

需要处理的原始 PDF。

例如：

```python
"INPUT_PDF": "/Users/andrewyu/Documents/离散数学.pdf"
```

---

### `OUTPUT_PDF`

处理完成后生成的新 PDF。

建议不要直接覆盖原文件，例如：

```python
"OUTPUT_PDF": "/Users/andrewyu/Documents/离散数学_最终版.pdf"
```

---

### `OFFSET`

这是本程序最重要的配置项。

定义：

```text
PDF物理页码 = 书面页码 + OFFSET
```

例如：

```text
正文第 1 页
对应
PDF 第 11 页
```

那么：

```python
OFFSET = 10
```

因此：

```text
书面页码 1 → PDF 第 11 页
书面页码 2 → PDF 第 12 页
书面页码 10 → PDF 第 20 页
```

---

# 三、运行程序

直接运行 Python 文件：

```bash
python main.py
```

成功后会依次显示类似：

```text
正在从 '离散数学目录文件.md' 解析目录数据...
正在打开 PDF 文件...
正在清除原有的目录...
准备写入 30 条新目录...
正在设置双重逻辑页码 (Page Labels)...
✅ 逻辑页码规则注入成功
正在保存新的 PDF 到: '离散数学_最终版.pdf'
✅ 处理完成！
```

然后使用 PDF 阅读器打开输出文件即可。

---

# 四、程序最终实现的效果

程序处理的是两个不同但相关的 PDF 导航体系。

## 1. PDF Bookmarks

也就是通常所说的：

> 侧边栏目录 / 书签

例如：

```text
第一章 集合
    1.1 集合的概念
    1.2 集合的运算
第二章 命题逻辑
    2.1 命题
    2.2 命题公式
```

点击书签后直接跳转到对应页面。

---

## 2. PDF Page Labels

Page Labels 是 PDF 的**逻辑页码显示系统**。

它与 PDF 内部的物理页编号不同。

例如一本教材可能是：

```text
PDF物理页：

1    封面
2    扉页
3    版权页
4    前言
5    前言
...
11   正文第1页
12   正文第2页
13   正文第3页
```

程序可以设置为：

```text
物理页 1  → i
物理页 2  → ii
物理页 3  → iii
...
物理页 10 → x
物理页 11 → 1
物理页 12 → 2
物理页 13 → 3
...
```

因此 PDF 阅读器可以同时正确体现：

```text
前言：i, ii, iii, iv...
正文：1, 2, 3, 4...
```

---

# 五、目录文件格式

## 基本格式

每行：

```text
LEVEL|TITLE|PAGE
```

例如：

```text
1|第一章 集合|1
2|1.1 集合的概念|1
2|1.2 集合的运算|8
3|1.2.1 并集与交集|9
1|第二章 命题逻辑|25
```

字段之间必须使用：

```text
|
```

分隔。

---

## LEVEL：书签层级

例如：

```text
1|第一章 集合|1
2|1.1 集合的概念|1
3|1.1.1 集合的表示|3
```

最终形成：

```text
第一章 集合
├── 1.1 集合的概念
│   └── 1.1.1 集合的表示
```

程序本身不会强制限制层级数。

理论上可以使用：

```text
1
2
3
4
5
...
```

具体显示效果由 PDF 阅读器对书签层级的支持决定。

---

## TITLE：书签标题

可以直接使用中文：

```text
1|第一章 集合|1
```

文件使用：

```text
UTF-8
```

编码读取，因此适合中文目录。

---

## PAGE：书面页码

这里填写的是**书籍印刷页码**，而不是 PDF 文件内部的物理页码。

例如：

```text
1|第一章 集合|1
2|1.1 集合的概念|1
2|1.2 集合的运算|8
```

程序再根据 `OFFSET` 自动转换。

---

# 六、注释与空行

程序会自动忽略：

### 空行

```text

```

### `#` 开头的行

```text
# 第一章
```

因此可以在 Markdown 文件中写一些说明：

```text
# 离散数学目录

1|第一章 集合|1
2|1.1 集合的概念|1

# 第二章

1|第二章 命题逻辑|25
```

注意：

`#` 在这里仅仅被程序作为**注释标记**处理，并不是 Markdown 标题语法。

---

# 七、错误检查

程序会自动检查：

## 文件不存在

```text
❌ 错误: 找不到目录文件
```

或者：

```text
❌ 错误: 找不到 PDF 文件
```

---

## 数字格式错误

例如：

```text
1|第一章 集合|abc
```

程序会跳过该行，并提示：

```text
⚠️ 警告: 第 X 行格式错误(含有非数字)
```

---

## 分隔符数量错误

例如：

```text
1|第一章 集合
```

或者：

```text
1|第一章|集合|1
```

程序会提示：

```text
⚠️ 警告: 第 X 行格式不匹配
```

---

## 没有有效目录

如果整个目录文件都无法解析：

```text
❌ 错误: 没有解析到任何有效的目录数据
```

程序不会继续修改 PDF。

---

# 八、技术架构

```text
                 ┌──────────────────┐
                 │   CONFIG 配置区   │
                 └────────┬─────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │ 检查输入文件是否存在 │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   解析 TOC 文件      │
              │ TXT / Markdown      │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ 生成 new_toc        │
              │ level/title/page    │
              └──────────┬──────────┘
                         │
                         │ page + OFFSET
                         ▼
              ┌─────────────────────┐
              │   打开 PDF          │
              │   PyMuPDF / fitz    │
              └──────────┬──────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      ┌──────────────┐      ┌────────────────┐
      │ 清除旧书签    │      │ 设置 Page      │
      │ set_toc([])  │      │ Labels         │
      └──────┬───────┘      └───────┬────────┘
             │                      │
             └──────────┬───────────┘
                        ▼
               ┌──────────────────┐
               │ 写入新书签        │
               │ set_toc(new_toc) │
               └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ 保存输出 PDF      │
               │ doc.save()       │
               └──────────────────┘
```

---

# 九、技术栈

## Python

程序主体语言。

使用 Python 的主要原因：

- PDF 操作库成熟
- 文本文件解析简单
- 跨平台
- 适合快速构建个人文档处理工具
- 配置和核心逻辑容易分离

---

## PyMuPDF

核心 PDF 操作库。

导入方式：

```python
import fitz
```

主要负责：

```text
PDF读取
PDF书签读取/修改
PDF Page Labels 修改
PDF保存
```

程序实际使用的核心 API 包括：

```python
fitz.open()
doc.set_toc()
doc.set_page_labels()
doc.save()
doc.close()
```

---

## os

Python 标准库：

```python
import os
```

用于进行最基础的文件存在性检查：

```python
os.path.exists()
```

---

# 十、核心数据结构

程序的核心目录数据存储在：

```python
new_toc = []
```

每一条目录最终转换成：

```python
[level, title, actual_page]
```

例如：

```python
[
    1,
    "第一章 集合",
    11
]
```

多个目录组合：

```python
[
    [1, "第一章 集合", 11],
    [2, "1.1 集合的概念", 11],
    [2, "1.2 集合的运算", 18],
    [1, "第二章 命题逻辑", 35]
]
```

这正是 PyMuPDF `set_toc()` 所需要的目录结构。

---

# 十一、目录解析流程

程序逐行读取目录文件：

```python
with open(toc_file, 'r', encoding='utf-8') as f:
```

然后：

```python
for line_num, line in enumerate(f, 1):
```

逐行处理。

首先清理首尾空白：

```python
line = line.strip()
```

然后过滤：

```python
if not line or line.startswith('#'):
    continue
```

接下来按照 `|` 分割：

```python
parts = line.split('|')
```

预期得到：

```text
[level, title, book_page]
```

然后进行类型转换：

```python
level = int(parts[0].strip())
title = parts[1].strip()
book_page = int(parts[2].strip())
```

最终计算：

```python
actual_page = book_page + offset
```

并加入：

```python
new_toc.append([level, title, actual_page])
```

---

# 十二、页码映射机制

这是程序最核心的业务逻辑之一。

程序假设：

```text
书面页码 + OFFSET = PDF物理页码
```

例如：

```text
OFFSET = 10
```

那么：

| 书面页码 | PDF物理页码 |
| -------: | ----------: |
|        1 |          11 |
|        2 |          12 |
|        3 |          13 |
|       10 |          20 |
|       50 |          60 |
|      100 |         110 |

因此：

```python
actual_page = book_page + offset
```

---

# 十三、为什么书签页码不是从 0 开始？

这里需要特别注意 PyMuPDF 与用户习惯之间的区别。

用户通常认为：

```text
PDF第1页
PDF第2页
PDF第3页
```

而 PDF 内部页面索引通常是：

```text
0
1
2
```

PyMuPDF 的 `set_toc()` 使用的是**从 1 开始的页码表示**。

因此本程序中：

```python
actual_page = book_page + offset
```

得到的 `actual_page` 可以直接作为：

```python
set_toc()
```

的目标页码。

而 `set_page_labels()` 使用的是 PDF 内部的**0-based page index**，所以二者不能混淆。

这是程序中一个非常重要的概念：

```text
书签目标页：
1-based

Page Labels：
0-based
```

---

# 十四、Page Labels 的实现

程序通过：

```python
doc.set_page_labels(page_labels)
```

设置 PDF 的逻辑页码。

当：

```python
offset > 0
```

时创建两个 Page Label 区间。

## 第一段

```python
{
    "startpage": 0,
    "style": "r",
    "prefix": "",
    "start": 1
}
```

表示：

```text
从 PDF 第 0 个内部页面开始
使用小写罗马数字
从 i 开始
```

即：

```text
i
ii
iii
iv
v
...
```

---

## 第二段

```python
{
    "startpage": offset,
    "style": "D",
    "prefix": "",
    "start": 1
}
```

表示：

```text
从内部页面 offset 开始
使用十进制数字
从 1 开始
```

例如：

```python
offset = 10
```

则：

```text
内部页 0  → i
内部页 1  → ii
...
内部页 9  → x
内部页 10 → 1
内部页 11 → 2
...
```

---

# 十五、为什么 `startpage` 是 OFFSET，而不是 OFFSET + 1？

因为：

```python
startpage
```

使用的是 PDF 内部的 **0-based index**。

例如：

```text
PDF第11页
```

对应：

```text
内部索引10
```

因此：

```python
"startpage": 10
```

正确表示：

> 从 PDF 的第 11 个物理页面开始显示正文页码 1。

这也是代码中书签页码与 Page Labels 页索引存在差异的原因。

---

# 十六、PDF 修改策略

程序采用的是：

```python
doc = fitz.open(input_pdf)
```

打开原始 PDF，然后修改 PDF 文档对象。

程序修改的主要对象是：

```text
Document Catalog / Outline / Page Labels
```

而不是重新生成每一页 PDF。

核心操作：

```python
doc.set_toc([])
```

清除原有目录。

然后：

```python
doc.set_toc(new_toc)
```

写入新的目录。

最后：

```python
doc.set_page_labels(page_labels)
```

设置逻辑页码。

因此本程序的核心目标是：

> **修改 PDF 的导航元数据，而不是重新制作 PDF 页面内容。**

---

# 十七、为什么先清除原目录？

程序使用：

```python
doc.set_toc([])
```

主动删除原有 TOC。

原因是该工具的定位并不是“在原目录上追加几个书签”，而是：

> 根据外部目录文件重新构建一套干净、可控的 PDF 目录。

这样可以避免：

```text
旧目录
+
新目录
```

产生重复。

也可以解决原 PDF：

- 书签层级错误
- 书签名称错误
- OCR 后目录异常
- 书签页码错误
- 存在大量无效书签

等问题。

---

# 十八、函数设计

核心函数：

```python
def update_pdf_toc_from_file(
    input_pdf,
    output_pdf,
    toc_file,
    offset
):
```

四个参数分别表示：

| 参数         | 作用                            |
| ------------ | ------------------------------- |
| `input_pdf`  | 输入 PDF                        |
| `output_pdf` | 输出 PDF                        |
| `toc_file`   | 外部目录文件                    |
| `offset`     | 书面页码到 PDF 物理页码的偏移量 |

这种设计使核心函数与顶部 `CONFIG` 解耦。

因此函数本身也可以被其他 Python 程序调用：

```python
update_pdf_toc_from_file(
    input_pdf="input.pdf",
    output_pdf="output.pdf",
    toc_file="toc.md",
    offset=10
)
```

---

# 十九、程序入口

最后：

```python
if __name__ == "__main__":
```

用于判断当前 Python 文件是否被直接运行。

如果直接运行：

```bash
python main.py
```

则执行：

```python
update_pdf_toc_from_file(...)
```

如果该文件被其他 Python 程序：

```python
import main
```

则不会自动执行主程序。

这种写法是标准 Python 模块化程序结构。

---

# 二十、错误处理设计

程序主要采用两层错误处理。

## 输入阶段

对于目录文件：

```python
if not os.path.exists(toc_file):
```

对于 PDF：

```python
if not os.path.exists(input_pdf):
```

避免在路径错误时进入 PDF 操作流程。

---

## PDF 操作阶段

打开 PDF：

```python
try:
    doc = fitz.open(input_pdf)
except Exception as e:
```

设置 Page Labels：

```python
try:
    ...
except Exception as e:
```

保存 PDF：

```python
try:
    doc.save(output_pdf)
except Exception as e:
```

这样可以把：

```text
文件不存在
PDF无法打开
Page Labels设置失败
PDF无法保存
```

等问题分别报告。

---

# 二十一、资源管理

程序最后使用：

```python
finally:
    doc.close()
```

确保 PDF 文档对象最终关闭。

这对于文件操作尤其重要，因为 PDF 在处理过程中可能持有：

- 文件句柄
- 内存资源
- 内部对象

使用 `close()` 可以避免资源长期占用。

---

# 二十二、项目结构建议

推荐项目结构：

```text
pdf-bookmark-tool/
│
├── main.py
├── README.md
├── requirements.txt
│
├── input/
│   └── book.pdf
│
├── toc/
│   └── toc.md
│
└── output/
    └── book_final.pdf
```

其中：

```text
main.py
```

负责程序逻辑。

```text
toc/
```

负责保存目录数据。

```text
input/
```

保存原始 PDF。

```text
output/
```

保存生成结果。

这种结构比把所有文件全部放在程序同一目录下更加清晰。

---

# 二十三、requirements.txt

如果项目需要固定依赖，可以建立：

```text
requirements.txt
```

内容：

```text
PyMuPDF
```

安装：

```bash
pip install -r requirements.txt
```

如果需要锁定具体版本，则可以写成：

```text
PyMuPDF==1.x.x
```

具体版本应根据项目实际测试环境确定，而不是在 README 中固定一个未经测试的版本。

---

# 二十四、当前版本的设计边界

本程序有意保持简单。

目前主要支持：

```text
外部 TXT/MD 目录
        ↓
结构化解析
        ↓
页码偏移
        ↓
PDF Bookmarks
        ↓
PDF Page Labels
```

它并不是一个完整的 PDF 编辑器。

目前没有实现：

- GUI 图形界面
- 自动 OCR
- 自动识别目录
- 自动识别书籍页码
- 自动寻找章节第一页
- PDF 页面合并
- PDF 页面删除
- PDF 内容编辑
- PDF 图片压缩
- PDF 重新排版
- 自动生成目录文件

因此它更准确的定位是：

> **一个面向结构化 PDF 目录重建的轻量级命令行工具。**

---

# 二十五、已知注意事项

## 1. OFFSET 必须正确

如果：

```text
正文第1页实际上对应 PDF 第12页
```

却设置：

```python
OFFSET = 10
```

那么所有书签都会整体偏移一页。

因此使用前最好先确认：

```text
书面页码 1
↓
PDF 中实际对应哪一页
```

---

## 2. 目录页本身不一定是正文页

如果书籍目录显示：

```text
第一章 集合 ........ 1
```

那么 `1` 是书籍印刷页码。

程序不会判断：

> 这个页码是不是目录页、章节首页还是正文页。

程序只执行用户提供的映射关系。

---

## 3. OFFSET 默认是统一偏移

当前程序采用：

```text
实际页码 = 书面页码 + 一个固定 OFFSET
```

因此它适合页码连续对应的普通教材。

如果 PDF 中间存在：

- 缺页
- 多插入页面
- 删除页面
- 扫描顺序异常
- 彩页单独插入
- 部分章节缺失

那么单一 `OFFSET` 可能无法覆盖整个 PDF。

---

# 二十六、未来扩展方向

如果以后继续发展这个工具，可以按照以下方向扩展。

## 1. 支持多段 Offset

例如：

```text
第 1–100 页：+10
第 101–200 页：+12
第 201–300 页：+13
```

可以建立：

```python
OFFSET_RULES = [
    ...
]
```

根据书面页码选择不同映射规则。

---

## 2. 支持前缀

Page Labels 不一定只能显示：

```text
1
2
3
```

还可以设计：

```text
A-1
A-2
A-3
```

或者：

```text
正文-1
正文-2
正文-3
```

对应：

```python
"prefix": "正文-"
```

---

## 3. 支持更多 Page Label 区间

例如：

```text
封面：Cover
前言：i, ii, iii
目录：1, 2, 3
正文：1, 2, 3
附录：A-1, A-2
```

可以通过多个 Page Label 区间实现。

---

## 4. 自动验证书签范围

可以增加：

```python
if actual_page > len(doc):
```

检查目标页面是否超过 PDF 总页数。

例如：

```text
目录要求跳转到 PDF 第 500 页
但 PDF 只有 480 页
```

则提前报告错误，而不是生成无效目录。

---

## 5. 目录格式进一步结构化

目前：

```text
1|第一章 集合|1
```

非常简单。

未来可以支持 YAML / JSON：

```json
{
  "level": 1,
  "title": "第一章 集合",
  "page": 1
}
```

或者：

```yaml
- level: 1
  title: 第一章 集合
  page: 1
```

这样可以携带更多元数据。

---

## 6. 自动从 Markdown 标题生成目录

目前 Markdown 中的：

```markdown
# 第一章 集合

## 1.1 集合的概念

## 1.2 集合的运算
```

会被程序视为注释，而不会自动转换。

未来可以增加 Markdown 原生解析模式：

```markdown
# 第一章 集合

## 1.1 集合的概念

## 1.2 集合的运算
```

再结合页码信息自动生成 TOC。

---

# 二十七、安全与数据处理

本程序采用本地文件处理方式。

程序本身：

- 不上传 PDF
- 不连接网络
- 不调用云端 OCR
- 不将文档发送给第三方服务

输入 PDF、目录文件和输出 PDF 均由本地 Python 进程处理。

因此适合处理不希望上传到在线 PDF 服务的个人文档。

---

# 二十八、典型使用场景

### OCR 教材整理

扫描教材经过 OCR 后：

```text
页面内容已经存在
↓
但 PDF 没有书签
↓
准备目录文件
↓
运行本程序
↓
获得带完整目录的 PDF
```

### 修复错误书签

原 PDF：

```text
书签页码全部错误
```

可以直接：

```text
重新准备 TOC
↓
清除旧书签
↓
重新生成
```

### 统一 PDF 页码

例如：

```text
前言 → i ii iii iv
正文 → 1 2 3 4
```

使用 Page Labels 统一逻辑页码显示。

---

# 二十九、最简使用流程

如果只想快速使用，只需要记住：

### 第一步

安装：

```bash
pip install PyMuPDF
```

### 第二步

准备目录：

```text
1|第一章 集合|1
2|1.1 集合的概念|1
2|1.2 集合的运算|8
1|第二章 命题逻辑|25
```

### 第三步

修改：

```python
CONFIG = {
    "TOC_FILE": "你的目录文件",
    "INPUT_PDF": "你的原始PDF",
    "OUTPUT_PDF": "输出PDF",
    "OFFSET": 10
}
```

### 第四步

运行：

```bash
python main.py
```

完成。

---

# 三十、核心思想总结

整个程序实际上只解决一个核心问题：

> **把“人能够理解的书籍目录页码”，转换成“PDF 能够跳转的物理页码”，并同时建立正确的 PDF 逻辑页码体系。**

其核心映射关系为：

```text
书籍目录
    │
    │  book_page
    ▼
书面页码
    │
    │  + OFFSET
    ▼
PDF物理页码
    │
    ├───────────────┐
    ▼               ▼
Bookmarks       Page Labels
    │               │
    ▼               ▼
点击目录跳转      阅读器显示正确页码
```

从架构上看，程序将：

```text
目录数据
```

与：

```text
PDF处理逻辑
```

进行了分离。

因此以后更换一本书时，原则上只需要替换：

```text
TOC_FILE
INPUT_PDF
OUTPUT_PDF
OFFSET
```

而不需要修改核心处理代码。

---

# License

本项目未指定开源许可证。
