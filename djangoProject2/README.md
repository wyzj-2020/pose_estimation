# 基于骨架的动作识别系统

> Human Action Recognition based on Skeleton Data — Django Web Application

基于 **OpenPose** 人体姿态估计与 **ST-GCN**（Spatial Temporal Graph Convolutional Network）骨架动作识别的 Web 应用。提供实时摄像头姿态检测、视频文件动作识别、用户认证等功能。

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 🔐 用户认证 | 注册 / 登录 / 登出，含图形验证码 |
| 📷 实时摄像头 | 浏览器端实时显示摄像头画面 |
| 🦴 姿态估计 | 基于 OpenPose 的实时 2D 人体关键点检测 |
| 🏃 实时动作识别 | ST-GCN 对摄像头画面进行实时动作分类 |
| 📹 离线视频识别 | 上传 MP4 视频文件，进行动作识别分析 |
| 📸 截图保存 | 网页端截图保存至服务器 |

---

## 技术栈

- **后端框架**: Django 3.2
- **姿态估计**: [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) (C++ 库 + Python 绑定)
- **动作识别**: [ST-GCN](https://github.com/yysijie/st-gcn) (AAAI 2018)
- **深度学习**: PyTorch
- **计算机视觉**: OpenCV
- **数据库**: MySQL（可切换 SQLite）
- **前端**: Bootstrap 3 + jQuery

---

## 项目结构

```
djangoProject2/
├── manage.py                  # Django 入口
├── djangoProject2/            # 项目配置
│   ├── settings.py            # Django 设置
│   ├── urls.py                # URL 路由
│   └── wsgi.py                # WSGI 入口
├── app/                       # 主应用
│   ├── views.py               # 视图函数（核心逻辑）
│   ├── models.py              # 数据模型（User, ImgData）
│   ├── main.py                # 实时动作识别入口
│   ├── file_main.py           # 离线视频识别入口
│   ├── processor/             # 视频处理管线
│   │   ├── demo_realtime.py   # 实时演示处理器
│   │   ├── demo_offline.py    # 离线演示处理器
│   │   ├── recognition.py     # 动作识别器
│   │   └── io.py              # I/O 工具
│   ├── net/                   # ST-GCN 网络定义
│   │   ├── st_gcn.py          # 单流 ST-GCN
│   │   └── st_gcn_twostream.py# 双流 ST-GCN
│   ├── feeder/                # 数据加载器
│   ├── tools/                 # 数据预处理工具
│   ├── torchlight/            # 训练辅助库
│   ├── utils/                 # 工具函数（加密、分页等）
│   ├── config/                # ST-GCN 训练/测试配置
│   ├── migrations/            # 数据库迁移文件
│   ├── templates/             # HTML 模板（11 个页面）
│   ├── static/                # 静态资源（CSS/JS/图片）
│   └── resource/              # 演示素材与参考数据
├── openpose/models/           # OpenPose 模型配置文件（.prototxt）
├── .env.example               # 环境变量模板
└── .gitignore
```

---

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+（或使用 SQLite）
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) 编译安装（需 Visual Studio + CUDA）
- Windows 10/11（当前仅支持 Windows）

### 安装步骤

**1. 克隆仓库**

```bash
git clone https://github.com/wyzj-2020/pose_estimation.git
cd pose_estimation
```

**2. 配置环境变量**

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入实际配置：

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DB_ENGINE=django.db.backends.mysql   # 或 django.db.backends.sqlite3
DB_NAME=openpose
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
OPENPOSE_BIN_PATH=D:/path/to/openpose/bin
```

**3. 安装 Python 依赖**

```bash
pip install -r app/requirements.txt
```

主要依赖：`pyyaml`, `numpy`, `opencv-python`, `torch`, `torchvision`

**4. 安装 OpenPose**

- 从 [OpenPose 官方仓库](https://github.com/CMU-Perceptual-Computing-Lab/openpose) 编译 Windows 版本
- 将编译后的 `bin/` 和 `models/` 放到项目 `openpose/` 目录下
- 或设置 `OPENPOSE_BIN_PATH` 环境变量指向编译目录

**5. 获取模型权重**

OpenPose 模型权重（自动下载）：

```bash
cd openpose/models
powershell -ExecutionPolicy Bypass -File getModels.bat
```

ST-GCN 预训练权重需要手动下载并放入 `app/models/` 目录：

| 模型 | 用途 |
|------|------|
| `st_gcn.kinetics.pt` | Kinetics 数据集预训练 |
| `st_gcn.ntu-xsub.pt` | NTU-RGB+D X-Sub 预训练 |
| `st_gcn.ntu-xview.pt` | NTU-RGB+D X-View 预训练 |

**6. 初始化数据库**

```bash
python manage.py migrate
```

**7. 启动服务**

```bash
python manage.py runserver
```

访问 `http://127.0.0.1:8000`，注册账号后即可使用。

---

## 页面路由

| URL | 页面 | 说明 |
|-----|------|------|
| `/` | 首页 | 项目介绍 |
| `/register/` | 注册 | 用户注册（用户名+邮箱+密码） |
| `/login/` | 登录 | 登录（含图形验证码） |
| `/logout/` | 登出 | 清除会话 |
| `/page1/` | 仪表盘 | 登录后主页 |
| `/page2/` | 视频上传 | 上传 MP4 离线识别 |
| `/pose/` | 原始摄像头 | 摄像头实时画面 |
| `/pose_estimate/` | 姿态估计 | 摄像头 + OpenPose 骨架叠加 |
| `/estimate/` | 动作识别 | 摄像头 + ST-GCN 实时识别 |
| `/demo_offline/` | 离线识别 | 上传视频的处理结果 |
| `/privacy/` | 个人信息 | 用户信息页 |
| `/video_feed/` | 视频流 | 原始摄像头 MJPEG 流 |
| `/video_process/` | 处理流 | OpenPose 处理后的 MJPEG 流 |
| `/image/code/` | 验证码 | 图形验证码图片 |
| `/save/image/` | 截图 | 保存网页截图 |

---

## 动作识别类别（Kinetics-400 子集）

支持识别约 400 类人体动作，包括：

`clean_and_jerk`（挺举）、`hammer_throw`（链球）、`juggling_balls`（杂耍球）、`pull_ups`（引体向上）、`tai_chi`（太极）、`skateboarding`（滑板）等。

完整类别列表见 `app/resource/kinetics_skeleton/label_name.txt`。

---

## 参考论文

> **Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition**, Sijie Yan, Yuanjun Xiong and Dahua Lin, AAAI 2018. [[arXiv]](https://arxiv.org/abs/1801.07455)

- ST-GCN 原始仓库：[yysijie/st-gcn](https://github.com/yysijie/st-gcn)
- 新版框架（推荐迁移）：[open-mmlab/mmskeleton](https://github.com/open-mmlab/mmskeleton)

---

## 注意事项

- 本项目为毕业设计作品，部分代码为原型质量
- 当前仅支持 **Windows** 平台（OpenPose 二进制为 Windows 编译）
- `DEBUG=True` 仅用于开发，部署时务必设为 `False`
- 密码使用 MD5 哈希（不安全），生产环境应更换为 bcrypt/PBKDF2
- 模型权重文件（`.caffemodel`, `.pt`）不上传至 GitHub，需按步骤自行下载

---

## License

本项目代码部分参考 [ST-GCN](https://github.com/yysijie/st-gcn)（MIT License）。详见 `app/LICENSE`。
