# 项目自动备份工具

一个简单易用的项目版本备份工具，支持一键备份、版本管理、快速恢复和自动清理功能。

## 功能特点

- ✨ **一键备份**：带时间戳的自动备份，支持添加注释
- 📋 **版本管理**：清晰查看所有备份版本
- 🔄 **快速恢复**：一键恢复到指定版本
- 🗑️ **备份清理**：删除不需要的备份，自动管理备份数量
- 🚫 **智能排除**：自动排除不需要备份的文件（如.git、node_modules等）
- 💾 **灵活存储**：支持压缩和文件夹两种备份模式
- 🖥️ **双界面支持**：命令行界面（CLI）和图形界面（GUI）

## 环境要求

- Python 3.6+（支持Windows、macOS、Linux）
- 无需额外安装依赖库（使用Python标准库）

## 安装说明

1. **下载项目**
   - 直接下载或克隆本项目到你的工作目录
   
2. **放置脚本**
   - 将 `backup_tool.py` 和 `gui_backup_tool.py` 复制到你需要备份的项目根目录
   
3. **验证Python安装**
   ```bash
   python --version
   ```

## 使用方法

### 一、命令行界面（CLI）

在项目根目录下运行以下命令：

#### 创建备份
```bash
python backup_tool.py --create
# 或带注释
python backup_tool.py --create --comment "开发完成v1.0"
```

#### 列出所有备份
```bash
python backup_tool.py --list
```

#### 恢复到指定版本
```bash
python backup_tool.py --restore v001_20230101_120000
```

#### 删除指定备份
```bash
python backup_tool.py --delete v001_20230101_120000
```

#### 查看帮助
```bash
python backup_tool.py --help
```

### 二、图形界面（GUI）

直接运行图形界面脚本：

```bash
python gui_backup_tool.py
```

#### 图形界面功能

1. **创建备份**：点击「创建备份」按钮，可添加注释
2. **恢复备份**：选择备份项，点击「恢复备份」按钮
3. **删除备份**：选择备份项，点击「删除备份」按钮
4. **刷新列表**：点击「刷新列表」更新备份列表
5. **查看详情**：双击备份项查看详细信息

## 配置说明

首次运行时，会自动创建 `config.json` 配置文件，可根据需要修改：

```json
{
    "backup_root": "../project_backups",
    "auto_exclude": [
        ".git", "node_modules", "__pycache__", ".pytest_cache",
        "venv", ".venv", "env", ".env", ".idea", ".vscode",
        ".DS_Store", "*.pyc", "*.log", "*.tmp", "*.bak",
        "backup_*", "dist", "build", "*.egg-info"
    ],
    "max_backups": 50,
    "compression": true,
    "hash_check": true
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| backup_root | 备份文件存储根目录 | ../project_backups |
| auto_exclude | 自动排除的文件/文件夹列表 | 见上 |
| max_backups | 最大备份数量，超过自动清理旧备份 | 50 |
| compression | 是否使用压缩模式 | true |
| hash_check | 是否进行哈希校验 | true |

## 项目结构

```
ProjectBackupTool/
├── backup_tool.py      # 主程序（命令行版）
├── gui_backup_tool.py  # 图形界面版
├── config.json        # 配置文件（自动生成）
├── requirements.txt   # 依赖说明
└── README.md         # 说明文档
```

## 备份文件命名规则

```
{项目名}_v{版本号}_{时间戳}_{注释}.zip
```

示例：
```
my_project_v001_20230101_120000_initial_backup.zip
```

## 注意事项

1. **备份位置**：默认备份到项目同级目录的 `project_backups` 文件夹
2. **排除文件**：确保 `auto_exclude` 配置包含了所有不需要备份的文件
3. **恢复操作**：恢复操作会覆盖当前项目文件，请谨慎操作
4. **权限问题**：确保有足够的权限读写备份目录
5. **备份大小**：对于大型项目，建议使用压缩模式节省空间
6. **定期清理**：系统会自动清理超出数量限制的旧备份

## 常见问题

### Q: 如何修改备份存储位置？
A: 修改 `config.json` 中的 `backup_root` 配置项

### Q: 如何添加自定义排除规则？
A: 在 `config.json` 的 `auto_exclude` 列表中添加规则，支持：
   - 文件名精确匹配（如：`.git`）
   - 扩展名匹配（如：`*.pyc`）
   - 路径包含匹配（如：`node_modules`）

### Q: 备份失败怎么办？
A: 检查：
   - 磁盘空间是否充足
   - 权限是否足够
   - 排除规则是否正确

## 版本历史

- v1.0.0 (2024-01-18)
  - 初始版本
  - 支持命令行和图形界面
  - 实现核心备份恢复功能
  - 智能排除和自动清理

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请在GitHub上提交Issue。
