# PDF 智能自动书签生成器 (PDF Auto Bookmark)

本项目是一个纯本地运行的端到端自动化工具，旨在解决扫描版、影印版 PDF 电子书（如考研数学教材、专业课本、考研资料等）缺少左侧导航书签和多级目录的问题。

项目结合了 **YOLOv8 目标检测** 与 **EasyOCR 光学字符识别** 技术，通过极少量的人工标注（提取数十张特征页），即可让 AI 自动学习书籍的物理排版特征，流式扫描全书数百页甚至 1GB 以上的大型 PDF，精准提取多级标题坐标与文字，并最终利用 `pypdf` 将树状多级目录注入到 PDF 底层。

## 核心功能

* **基于视觉的排版解析**：彻底脱离传统基于字体、字号的死板规则解析。YOLOv8 直接通过视觉特征（如字号大小、缩进、留白、层级结构等）理解书籍的物理排版，定位不同层级的标题，不受传统文本正则匹配方式限制，对扫描倾斜、水印等干扰具有较强的抗干扰能力。
* **自动化高清样本提取**：无需手动截图，自动根据指定页码从 PDF 中提取 300 DPI 高清 PNG 样本图用于标注。
* **内存安全的长文档流式扫描**：针对 1GB 以上的大型 PDF 进行了内存优化。全书扫描采用“单页转图片 -> 识别 -> 释放”的流式处理，即使是 1GB 级别的高清 PDF 也不会因为一次性加载整本文件而导致内存溢出。
* **防越级与容错修复**：自动修复 AI 识别过程中可能出现的目录“越级”现象，例如 1 级标题直接跳到 3 级，强制保证 PDF 书签树结构规范。
* **自定义后处理清洗**：支持通过关键词黑名单过滤视觉模型可能产生的误判，例如将“习题”、“解答”等纯文本误识别为一级标题时，可以在进入 JSON/PDF 前进行过滤，而无需重新训练模型。
* **安全解耦的目录注入**：将耗时的“全书扫描 OCR 提取”与最终的“PDF 底层重构注入”物理分离。扫描结果会实时备份为本地 `toc_backup.json`，即使最终 PDF 因阅读器占用等原因写入失败，也无需重新扫描全书。
* **底层目录树重构**：使用 `pypdf` 引擎从 0 构建带“超一级总纲”的多级父子节点并注入 PDF，生成完整的树状书签结构。

## 环境依赖与安装

本项目核心计算依赖深度学习，但支持不同硬件平台运行，包括 NVIDIA 独立显卡、Apple Silicon、Intel/AMD 核显以及纯 CPU 环境。

推荐在配备 NVIDIA GPU 的 Windows 机器上运行，以获得更高的 YOLO 和 OCR 推理速度。

### 1. 基础环境

* **Python**：3.10 - 3.13
* **操作系统**：Windows / macOS / Linux
* **CUDA**：使用 NVIDIA 独立显卡时，建议 CUDA 12.1 或 CUDA 12.4 及以上，以充分激活 NVIDIA 显卡加速。

### 2. 通用核心依赖

在终端中执行以下命令安装项目所需的第三方核心库：

Bash

```bash
pip install ultralytics easyocr PyMuPDF opencv-python numpy pypdf
```

### 3. PyTorch 底座安装（根据硬件选择）

YOLOv8 和 EasyOCR 的运行速度极度依赖 PyTorch 的硬件加速后端。请根据电脑配置选择对应的安装方案。

#### 方案 A：Windows + NVIDIA 独立显卡（推荐，性能最强）

利用 CUDA 核心进行 GPU 加速。

首先卸载可能存在的纯 CPU 版本：

Bash

```bash
pip uninstall torch torchvision torchaudio -y
```

然后安装 CUDA 12.4 满血版 PyTorch：

Bash

```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124
```

NVIDIA GPU 环境可以充分利用 CUDA 加速 YOLOv8 和 EasyOCR，整体扫描速度相比纯 CPU 模式可以大幅提升。

#### 方案 B：macOS + Apple Silicon（M1/M2/M3 等）

苹果 Mac 电脑无需额外安装 CUDA，官方 PyTorch 支持苹果芯片的 **MPS（Metal Performance Shaders）** 硬件加速。

直接安装：

Bash

```bash
pip install torch torchvision torchaudio
```

运行时，YOLO 和 EasyOCR 可以根据底层环境调用 Mac 的 GPU 核心进行加速。

#### 方案 C：轻薄本 / Intel 或 AMD 核显 / 纯 CPU 运行

如果电脑只有 Intel 或 AMD 集成显卡（核显），或者遇到显卡驱动问题，可以直接使用 CPU 模式运行。

安装：

Bash

```bash
pip install torch torchvision torchaudio
```

纯 CPU 模式下运行 `main_progress.py` 时，终端可能提示：

```text
Neither CUDA nor MPS are available - defaulting to CPU
```

这是正常反馈，程序依然可以稳定运行，只是全书扫描耗时会相应增加。

如果 EasyOCR 初始化时指定了 GPU，而当前机器不存在可用的 CUDA 或 MPS 后端，程序会出现 Warning 并自动 Fallback 到 CPU 计算，无需手动修改代码。

## 项目使用指南（用户端完整流程）

整个项目分为五个核心阶段，只需按照顺序执行即可得到带有多级书签的 PDF。

### 阶段一：提取高清样本图

模型需要学习这本特定书籍的排版，因此首先需要从 PDF 中挑选出包含各级标题的代表性页面，将其转换为高清图片。

1. 打开 `目录页码.py`。
2. 修改 `pdf_path` 为你的原始 PDF 路径。
3. 打开 PDF 阅读器，找出约 20~30 页包含一级、二级、三级标题的典型页面。
4. 将这些页面的**绝对页码**填入 `target_pages` 列表。

   > 注意：这里填写的是 PDF 阅读器顶部显示的页码，而不是纸张上印刷的页码。

5. 运行 `目录页码.py`。

程序会在项目根目录自动创建：

```text
dataset/images/
```

并生成 300 DPI 的高清 PNG 图片。

### 阶段二：在线标注数据集（核心人工环节）

推荐使用基于浏览器的 [MakeSense.ai](https://www.makesense.ai/?utm_source=gemini) 进行目标检测标注。

该工具可以直接在浏览器中完成标注，无需额外配置本地标注软件环境。

#### 详细标注流程

1. **访问网站**

   打开浏览器进入：

   `https://www.makesense.ai/`

   点击右下角 `Get Started`。
2. **导入图片**

   将上一步生成的 `dataset/images/` 目录下的所有高清图片拖入网页。
3. **选择模式**

   点击：

   `Object Detection`

   即目标检测模式。
4. **创建标签**

   依次创建：

    * `L1`：一级标题
    * `L2`：二级标题
    * `L3`：三级标题

   每输入一个标签后点击加号。

   可以根据需要为不同标签设置不同颜色，例如：

    * `L1`：大红色
    * `L2`：亮绿色
    * `L3`：深蓝色

   高对比度颜色可以缓解长时间标注时的视觉疲劳。

   创建完成后点击 `Start project`。
5. **画框标记**

   使用鼠标框选每一页中的标题区域，也可以使用快捷键 `W`。

   框选后，在右侧菜单中赋予对应的：

    * `L1`
    * `L2`
    * `L3`

   标签。

   框选区域应尽量贴合标题文字边缘，不要包含过多无关空白或正文。

   **标准要求：只框选真正需要作为书签的文本。**

   如果页面中出现无关的：

    * “习题”
    * “例题”
    * “解答”

   等文本，且不希望它们成为最终书签，则不要对这些文本进行标注。

   完成一张后点击右上角箭头进入下一张。
6. **导出数据**

   标注完成后：

    * 点击左上角 `Actions`
    * 点击 `Export Annotations`
    * 选择 **`A .zip package containing files in YOLO format`**

   下载 ZIP 后解压。

   将其中所有 `.txt` 标签文件复制到：

```text
dataset/labels/
```

**严格检查：**

图片文件名和标签文件名必须完全一致并一一对应。

例如：

```text
dataset/images/page_8.png
dataset/labels/page_8.txt
```

同时确保 `images/` 中的图片数量与 `labels/` 中的 `.txt` 文件数量完全一致。

### 阶段三：训练专属视觉模型

现在让机器学习这本书独特的排版特征。

1. 在项目根目录创建 `config.yaml`。
2. 写入：

YAML

```yaml
path: ./dataset
train: images
val: images
nc: 3
names: ['L1', 'L2', 'L3']
```

3. 运行：

```text
train_model.py
```

4. 代码会自动下载 `yolov8n.pt` 轻量级底座，并结合本地人工标注的数据进行训练。
5. 默认训练 50 轮（Epochs）。
6. 训练过程中会根据当前硬件环境自动调用可用的计算设备。
7. 训练完成后，会在：

```text
runs/detect/train/weights/
```

生成：

```text
best.pt
```

这就是属于当前书籍的专属视觉模型权重。

### 阶段四：流式扫描全书与 OCR 识别

这是整个系统的核心扫描阶段，耗时根据 PDF 页数、图片分辨率以及计算机硬件性能而定，通常需要几分钟到十几分钟。

1. 打开：

```text
main_progress.py
```

2. 确认配置区中的：

```text
pdf_path
output_pdf_path
model_path
```

均正确。

其中 `model_path` 应指向上一阶段生成的：

```text
best.pt
```

3. 关闭所有正在使用该 PDF 的阅读器，例如：

    * WPS
    * Edge
    * Adobe Acrobat
    * 其他 PDF 阅读器

   防止最终写入时触发文件占用问题。
4. 运行脚本。

程序会依次执行：

* 逐页将 PDF 转换为图像；
* 使用 YOLO 定位标题区域；
* 获取标题的像素坐标；
* 根据 BBox 从原图中裁剪标题区域；
* 将标题图像块送入 EasyOCR；
* 获取标题文字；
* 根据 Y 轴坐标从上到下排序；
* 记录标题层级、文字和 PDF 页码。

整个过程采用单页流式处理：

```text
单页 PDF
   ↓
转换为图片
   ↓
YOLO 标题检测
   ↓
BBox 裁剪
   ↓
EasyOCR
   ↓
记录结果
   ↓
释放当前页面图像
   ↓
下一页
```

5. **关键护城河：持久化备份**

扫描完成后，程序会将所有识别到的：

* 层级
* 标题文字
* 页码

保存至：

```text
toc_backup.json
```

这个文件是整本书扫描后的扁平化结构数据资产。

即使后续 PDF 注入阶段失败，也无需重新经历漫长的全书扫描过程。

### 阶段五：书签重构与底层注入

这一阶段负责将 `toc_backup.json` 中的扁平数据重新构造成 PDF 所需的树状目录结构。

如果上一步由于 PDF 被占用导致写入失败，或者发现书签存在整体页码偏移，无需重新扫描全书，可以直接使用独立的：

```text
inject_only.py
```

#### 1. 配置 `inject_only.py`

根据需要修改：

```text
ROOT_TITLE
PAGE_OFFSET
```

其中：

* `ROOT_TITLE`：设置一个超一级总目录名称，例如：

```python
"《考研数学基础30讲 (高数分册)》"
```

所有自动提取的书签都会被收纳到这个根目录之下。

* `PAGE_OFFSET`：设置页码整体偏移量。

例如生成的书签点击后整体少翻 5 页，可以设置：

```text
PAGE_OFFSET = 5
```

如果需要向前偏移，也可以设置负值，例如：

```text
PAGE_OFFSET = -2
```

#### 2. 关闭 PDF 阅读器

运行注入脚本前关闭所有正在使用目标 PDF 的软件，以避免触发：

```text
PermissionError
```

#### 3. 运行注入脚本

运行：

```text
inject_only.py
```

程序会快速读取：

```text
toc_backup.json
```

然后：

1. 修复跨级错误；
2. 根据 `PAGE_OFFSET` 修正页码；
3. 构建多级父子节点；
4. 通过 `pypdf` 注入 PDF；
5. 输出最终带有完整多级书签的 PDF。

## 开发者文档（架构与技术实现）

### 项目结构

```text
PDF_Auto_Bookmark/
├── data_raw/            # 存放原始 1GB 的 PDF 书籍
├── dataset/             # YOLO 模型的数据集主目录
│   ├── images/          # 从 PDF 抽帧提取的 300 DPI 原图 (png)
│   └── labels/          # MakeSense.ai 导出的 YOLO txt 坐标标签
├── runs/                # Ultralytics (YOLO) 训练的日志与权重产出
├── config.yaml          # YOLOv8 训练配置文件
├── 目录页码.py          # [脚本] 核心：根据绝对页码提取指定高清内页
├── train_model.py       # [脚本] 核心：加载 yolov8n.pt 并进行微调训练
├── main_progress.py     # [脚本] 核心：完整扫描管线（含 OCR 与 JSON 备份）
├── inject_only.py       # [脚本] 核心：读取 JSON 并执行 PDF 书签注入
├── toc_backup.json      # [数据] 扫描管线生成的持久化扁平目录结构
└── 27张宇基础30讲最终完美版.pdf # 最终成品输出
```

## 核心数据流

本项目遵循经典的“机器视觉 + NLP 预处理”管道结构。

### 1. 原始文档 -> 高清图像 -> OpenCV

使用 `PyMuPDF` 加载 PDF 页面，并将页面渲染为高清图像。

代码中使用：

```text
pix.tobytes("png")
```

配合：

```text
cv2.imdecode
```

进行图像解码。

代码摒弃过时的：

```text
pix.tobytes("rgb")
```

方式，以解决不同 PyMuPDF 版本之间的 API 兼容性问题。

项目中的高清样本提取阶段使用 300 DPI，而全书扫描阶段可以根据实际性能需求使用相应的渲染分辨率。

### 2. 像素图 -> 边界框（BBox）

将 OpenCV 的 BGR 矩阵送入训练好的 YOLOv8 模型。

YOLO 推理得到：

```text
[x1, y1, x2, y2, conf, class]
```

其中包含：

* 标题左上角坐标；
* 标题右下角坐标；
* 置信度；
* 标题层级类别。

### 3. 边界框 -> 文本字符串（OCR）

根据 BBox 从原图中裁剪标题区域：

```python
crop_img = img_bgr[y1:y2, x1:x2]
```

然后将裁剪结果交给基于 PyTorch 的 EasyOCR。

默认语言环境为：

```text
ch_sim
en
```

即简体中文 + 英文。

### 4. 扁平文本 -> 树状目录树（PDF Outlines）

OCR 最终得到的是类似下面的扁平列表：

```text
L1  第一章 函数
L2  1.1 函数的概念
L3  1.1.1 函数定义
L2  1.2 函数的性质
L1  第二章 极限
...
```

注入模块需要将其重新构造成 PDF 所需的树状结构。

程序通过：

```text
parent_nodes
```

字典追踪不同层级节点之间的父子关系。

同时使用跨级修复逻辑：

```text
lvl > last_level + 1
```

当发现当前标题层级比上一个标题直接跳跃超过一级时，将其降级为允许的下一层级，从而避免非法的 PDF 书签树结构。

## 关键设计取舍

### 1. 为什么分离扫描层和注入层？

在 Windows 环境下，PDF 文件容易被办公软件或阅读器锁死，例如 WPS 在后台占用 PDF。

如果使用单一脚本：

```text
AI 扫描几十分钟
        ↓
最后 doc.save()
        ↓
PermissionError
        ↓
前面的扫描结果无法复用
```

会导致大量计算时间浪费。

因此项目将：

```text
全书扫描
```

与：

```text
PDF 书签注入
```

完全分离。

扫描结果先保存为：

```text
toc_backup.json
```

之后由：

```text
inject_only.py
```

单独完成注入。

这样即使 PDF 最终写入失败，也只需要重新执行注入阶段，无需重新扫描整本 PDF。

### 2. 为什么使用 `pypdf` 而不是 `PyMuPDF` 注入目录？

`PyMuPDF (fitz)` 提供：

```text
doc.set_toc()
```

用于设置 PDF 目录。

但在向原本完全没有底层目录树结构的扫描 PDF 中注入书签时，有时无法正确注册底层 Catalog，导致部分主流阅读器无法正常识别。

项目最终采用：

```text
pypdf
```

并利用：

```text
add_outline_item
```

构建更加原生的 PDF 树状目录节点。

### 3. 后处理清洗（Post-Processing）

由于不同内容可能具有高度相似的排版样式，视觉模型可能将字体粗大的：

```text
习题
解答
例题
```

等文本误认为标题。

此类问题不一定需要重新训练模型，可以在进入最终 JSON/PDF 之前增加关键词黑名单进行过滤。

例如：

```python
BLACKLIST = ["习题", "解答"]

cleaned_toc = []

for item in final_toc:
    lvl, title, page = item

    if any(black_word in title for black_word in BLACKLIST):
        continue

    cleaned_toc.append(item)
```

后续针对：

```text
cleaned_toc
```

进行目录树重构即可。

## 扩展性与可移植性开发指南

### 1. 跨语言支持拓展（OCR 引擎）

当前 `main_progress.py` 中 EasyOCR 的初始化参数为：

```python
['ch_sim', 'en']
```

适用于中文 + 英文教材及公式环境。

如果需要处理其他语言，可以修改：

```text
main_progress.py
```

中的：

```text
easyocr.Reader()
```

初始化部分。

例如：

**纯英文教材：**

```python
['en']
```

**繁体中文 + 英文：**

```python
['ch_tra', 'en']
```

首次切换语言时，EasyOCR 会自动下载对应的推理模型库。

### 2. 硬件平台的无缝迁移

在 `main_progress.py` 中，硬件分配主要由底层库根据当前运行环境自动处理。

YOLOv8 的：

```python
model(img_bgr)
```

推理动作可以根据系统环境调用对应计算后端：

```text
NVIDIA 独立显卡
        ↓
CUDA

Apple Silicon
        ↓
MPS

无可用 GPU
        ↓
CPU
```

因此同一套项目代码可以在不同硬件平台之间迁移。

对于没有独立 GPU 的轻薄本，如果 EasyOCR 初始化时设置了 GPU，而当前环境不存在可用 CUDA/MPS 后端，程序会发出 Warning 并自动回退到 CPU，无需手动修改完整处理流程。

### 3. 结果精细化清洗（后处理拓展）

除了简单的关键词黑名单之外，也可以根据实际书籍结构继续增加后处理规则。

例如：

```python
BLACKLIST = ["习题", "解答"]

cleaned_toc = []

for item in final_toc:
    lvl, title, page = item

    if any(black_word in title for black_word in BLACKLIST):
        continue

    cleaned_toc.append(item)
```

这种方式可以将：

```text
视觉检测
    ↓
OCR
    ↓
JSON
    ↓
数据清洗
    ↓
目录树
    ↓
PDF
```

中的数据清洗独立出来，而无需反复训练 YOLO 模型。

### 4. 目录树嵌套逻辑的深度定制

目前项目的防护逻辑是“强行平铺降级”。

当检测到：

```text
lvl > last_level + 1
```

时，将当前层级强制调整为：

```text
last_level + 1
```

从而避免 `pypdf` 的：

```text
add_outline_item
```

因为非法跨级结构而构建失败。

如果面对极度复杂的定制排版需求，例如存在：

```text
卷
 └── 篇
      └── 章
           └── 节
                └── 目
```

这种 5 级目录结构，只需在：

```text
inject_only.py
```

中扩展：

```text
parent_nodes
```

字典的寻址深度，以及：

```text
lvl
```

变量的映射范围，无需修改庞大的目标检测和 OCR 推理管线。

## 项目整体工作流

最终整个项目可以概括为：

```text
原始 PDF
    ↓
目录页码.py
    ↓
提取 20~30 张高清样本页
    ↓
dataset/images/
    ↓
MakeSense.ai
    ↓
人工标注 L1 / L2 / L3
    ↓
dataset/labels/
    ↓
train_model.py
    ↓
YOLOv8 专属模型 best.pt
    ↓
main_progress.py
    ↓
逐页 PDF → 图像
    ↓
YOLOv8 标题检测
    ↓
BBox 标题区域
    ↓
EasyOCR
    ↓
标题文字 + 层级 + 页码
    ↓
toc_backup.json
    ↓
inject_only.py
    ↓
跨级修复 + 页码偏移 + 父子节点重构
    ↓
pypdf
    ↓
最终带多级书签的 PDF
```

其中最核心的数据资产和容错节点为：

```text
toc_backup.json
```

它将耗时的 AI 扫描阶段与最终 PDF 注入阶段彻底解耦，使整个处理流程具备较强的容错能力。
写在最后：
```text
推荐的项目结构：
PDF_Auto_Bookmark/
├── inputs/                 # 存放原始输入文件 (替代原 data_raw)
│   └── 27张宇基础30讲高数_带大纲.pdf
├── outputs/                # 存放所有管线产出，保持项目根目录绝对清爽
│   ├── backups/            # 存放中间扫描结果 (如 toc_backup.json)
│   └── final_pdfs/         # 存放最终注入完美书签的成品 PDF
├── dataset/                # AI 专属训练场地
│   ├── images/             # 提取的高清样本原图
│   └── labels/             # 对应的 YOLO txt 坐标标签
├── models/                 # 统一管理所有模型权重 (防止散落在根目录)
│   ├── base/               # 存放自动下载的 yolov8n.pt 等通用底座
│   └── custom/             # 存放你自己炼制成功的 best.pt
├── runs/                   # YOLO 训练时自动生成的日志与产物面板 (跑完可定期清理)
├── config.yaml             # YOLO 训练数据集配置文件
├── 01_extract_pages.py     # (原 目录页码.py) 阶段 1：抽帧提取
├── 02_train_model.py       # (原 train_model.py) 阶段 2：模型微调
├── 03_scan_pdf.py          # (原 main_progress.py) 阶段 3：全书流式扫描
├── 04_inject_toc.py        # (原 inject_only.py) 阶段 4：书签清洗与注入
├── requirements.txt        # 环境依赖清单，方便在新电脑上一键复刻环境
├── .gitignore              # Git 忽略配置，防止把 1GB 的 PDF 和大模型传到云端
└── README.md               # 项目完整使用说明与开发者文档
```

我在仓库里的一些空文件夹里面加入了一些.gitkeep文件，是为了能够比较完整的保持项目结构，为了这些文件夹能够被上传，不需要考虑其存在会对项目有什么影响。