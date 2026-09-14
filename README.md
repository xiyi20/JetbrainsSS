# JetbrainsSS

**JetbrainsSS**（全称 Jetbrains Splash Studio）是一款 JetBrains IDE 启动图自定义工具，通过修改 IDE 安装目录中 jar 包内的 splash 资源，实现启动画面的个性化替换。

基于 PyQt6 + [QFluentWidgets](https://qfluentwidgets.com/) 构建，采用 Fluent Design 风格界面，支持深浅色主题自动切换。

## ✨ 功能特性

- 🎨 **一键替换启动图**：选择 IDE 安装目录与两张启动图，点击"开始修补"即可完成替换
- 🗂 **多 IDE 支持**：IntelliJ IDEA / PyCharm / WebStorm
- ⏪ **随时还原**：修补前自动备份原始 jar，一键还原官方启动图
- 🧹 **自动清理缓存**：修补/还原后自动清理 JetBrains  splash 缓存，重启 IDE 立即生效
- 💾 **配置持久化**：安装目录与启动图绑定关系自动保存，下次启动无需重新配置
- 🔒 **防误触设计**：绑定后的路径输入框自动锁定，长按右键或长按"选择"按钮解锁

## 📌 支持的 IDE 与版本

| IDE | 版本 | jar 路径 |
| --- | --- | --- |
| IntelliJ IDEA | 2025.3 (253) | `/lib/product-backend.jar` |
| PyCharm | 2025.3 (253) | `/lib/product-backend.jar` |
| WebStorm | 2025.3 (253) | `/lib/app-backend.jar` |

> 其他版本可在 [JarPath.py](src/main/app/common/JarPath.py) 中自行扩展配置。

## ⚠️ 重要提示

- **IDE 更新前请先点击[还原]撤销修补**，否则会导致 IDE 更新校验失败
- 修补时 IDE 必须处于**关闭状态**，否则会因文件占用而失败
- 启动图尺寸要求严格，不符合尺寸的图片无法通过校验：
  - 启动图 1：**640 × 400 px**（PNG）
  - 启动图 2：**1280 × 800 px**（PNG）

## 🚀 使用方法

1. 从 [Actions](https://github.com/xiyi20/JetbrainsSS/actions) 下载最新构建的 `JetbrainsSS-Artifacts.zip` 后解压运行
2. 在对应 IDE 卡片中点击 **[选择]**，绑定 IDE 安装目录（需包含 `bin/idea64.exe` 等启动程序）
3. 分别选择两张符合尺寸的启动图
4. 点击 **[开始修补]**，等待进度条完成
5. 重启 IDE 查看效果；如需恢复官方启动图，点击 **[还原]**

### 输入框解锁

路径绑定后输入框会被锁定以防误改：

- **长按输入框右键** 或 **长按 [选择] 按钮** 即可解锁手动编辑

## 🛠 开发

### 环境要求

- Python 3.8+
- Windows（依赖 `pywin32` 读取 exe 版本信息）

### 运行

```bash
# 克隆仓库
git clone https://github.com/xiyi20/JetbrainsSS.git
cd JetbrainsSS

# 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 运行（需将项目根目录加入 PYTHONPATH，以便解析 src 包）
$env:PYTHONPATH = "$PWD"
python src/main/app/main.py
```

### 项目结构

```
src/main/
├── app/
│   ├── main.py              # 程序入口
│   ├── config.json          # 持久化配置(IDE 路径/版本/启动图绑定)
│   ├── common/              # 通用逻辑
│   │   ├── AppTheme.py      # 主题配色(主题色/徽章/警告条自适应)
│   │   ├── JarEditor.py     # jar 内 splash 资源的修补与还原
│   │   ├── JarPath.py       # 各 IDE 版本的 jar 路径与目标资源映射
│   │   ├── PathTool.py      # 目录/图片选择与校验
│   │   └── RwConfig.py      # 配置读写(单例)
│   └── component/           # 界面组件
│       ├── MainWindow.py    # 主窗口(FluentWindow)
│       ├── HomeWidget.py    # 主页(滚动卡片布局)
│       ├── IDEWidget.py     # IDE 卡片(路径绑定/版本徽章)
│       ├── OptionWidget.py  # 修补面板(启动图选择/进度条)
│       ├── AboutWidget.py   # 关于页
│       └── ...              # 基础控件封装
└── resources/               # 图标与 IDE logo
```

### 打包

```bash
pyinstaller --onefile --windowed --name=JetbrainsSS.exe \
  -i .\src\main\resources\logo.ico --add-data 'src;src' \
  .\src\main\app\main.py
```

打包产物需与 `config.json`、`resources/` 目录放在同一目录下分发（参考 [.github/workflows/AutoCompilation.yml](.github/workflows/AutoCompilation.yml) 中的 CI 自动构建流程）。

## 📄 License

本项目基于 [MIT License](LICENSE) 开源。仅供学习交流使用，请勿用于任何商业用途或对软件完整性的非法篡改。
