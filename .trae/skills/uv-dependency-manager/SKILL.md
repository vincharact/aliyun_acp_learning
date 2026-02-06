---
name: "uv-dependency-manager"
description: "使用 uv 工具管理 Python 项目依赖。当用户需要安装、更新、移除依赖或管理虚拟环境时调用此技能。"
---

# UV 依赖管理器

此技能帮助您使用 uv 工具高效管理 Python 项目的依赖包。

## 什么是 uv

uv 是一个快速的 Python 包管理器，可以替代 pip 和 pip-tools，提供更快的依赖解析和安装速度。

## 常用命令

### 初始化项目

```bash
# 创建新项目
uv init my-project

# 在现有目录中初始化
uv init
```

### 管理依赖

```bash
# 添加依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 添加特定版本
uv add package-name==1.2.3

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 移除依赖
uv remove package-name

# 更新依赖
uv lock --upgrade-package package-name
```

### 虚拟环境管理

```bash
# 创建虚拟环境
uv venv

# 指定 Python 版本创建虚拟环境
uv venv --python 3.11

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 运行命令（自动使用虚拟环境）
uv run python script.py
uv run pytest
```

### 依赖同步

```bash
# 同步依赖（安装 pyproject.toml 中定义的所有依赖）
uv sync

# 仅同步生产依赖
uv sync --no-dev
```

### 查看依赖

```bash
# 列出已安装的包
uv pip list

# 查看依赖树
uv pip show package-name

# 检查过时的包
uv pip list --outdated
```

## 项目文件结构

使用 uv 的项目通常包含：

```
my-project/
├── pyproject.toml      # 项目配置和依赖声明
├── uv.lock             # 锁定的依赖版本（自动生成）
├── .venv/              # 虚拟环境（自动创建）
└── src/                # 源代码
```

## pyproject.toml 示例

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
```

## 最佳实践

1. **始终使用 `uv add` 而不是手动编辑 pyproject.toml**
   - uv 会自动解析依赖冲突
   - 自动更新 uv.lock 文件

2. **提交 uv.lock 到版本控制**
   - 确保团队成员使用相同的依赖版本
   - 实现可重现的构建

3. **使用 `uv run` 执行命令**
   - 自动激活虚拟环境
   - 确保使用正确的 Python 环境

4. **区分开发和生产依赖**
   - 使用 `--dev` 标志添加开发依赖
   - 使用 `uv sync --no-dev` 安装生产环境依赖

5. **定期更新依赖**
   - 使用 `uv lock --upgrade` 更新所有依赖
   - 或使用 `--upgrade-package` 更新特定包

## 故障排除

### 依赖冲突
如果遇到依赖冲突，uv 会自动尝试解决。如果失败，可以：
- 检查 pyproject.toml 中的版本约束
- 使用 `uv add --resolution=lowest` 选择最低兼容版本

### 速度慢
uv 已经很快了，但如果需要更快：
- 使用 `uv sync --frozen` 跳过依赖解析
- 确保使用最新的 uv 版本

### 虚拟环境问题
如果虚拟环境有问题：
```bash
# 删除并重新创建
rm -rf .venv
uv venv
uv sync
```

## 与 pip 的对比

| 功能 | uv | pip |
|------|----|-----|
| 依赖解析速度 | 极快 | 较慢 |
| 并行下载 | 支持 | 不支持 |
| 锁文件 | 自动生成 | 需要 pip-tools |
| 虚拟环境 | 内置 | 需要 venv |
| pyproject.toml | 原生支持 | 需要额外工具 |
