---
name: "code-generator"
description: "生成符合项目规范的代码，支持结构分析、代码复用、风格一致性、依赖管理和质量验证。当用户需要生成新代码或添加功能时调用此技能。"
---

# 代码生成器

此技能帮助您生成符合项目规范、可维护性高且易于集成的代码。

## 核心功能

### 1. 项目结构分析

在生成代码之前，必须先分析项目结构：

**分析步骤：**
- 使用 `LS` 工具扫描项目根目录和关键子目录
- 使用 `Glob` 工具查找特定类型的文件（如 `*.py`, `*.js`, `*.ts` 等）
- 使用 `SearchCodebase` 工具了解现有代码的组织方式和模块划分
- 识别项目的目录结构模式（如 MVC、分层架构、模块化等）

**关键检查点：**
- 源代码目录位置（src/, lib/, app/ 等）
- 公共模块/工具类目录位置（utils/, common/, shared/ 等）
- 配置文件位置（config/, settings/ 等）
- 测试目录位置（tests/, __tests__/ 等）
- 依赖配置文件（package.json, pyproject.toml, requirements.txt 等）

### 2. 代码复用机制

**识别可复用逻辑：**
- 使用 `SearchCodebase` 搜索相似功能的实现
- 查找公共工具函数和辅助类
- 识别重复的模式和逻辑

**复用策略：**
- 优先使用项目中已存在的函数和类
- 将可复用逻辑提取到公共模块中
- 避免重复实现相同功能

**公共模块放置原则：**
- 通用工具函数 → `utils/` 或 `lib/utils/`
- 业务通用组件 → `common/` 或 `shared/`
- 配置相关 → `config/`
- 类型定义 → `types/` 或 `@types/`

### 3. 代码风格一致性

**风格分析：**
- 检查现有代码的缩进方式（2空格、4空格、tab）
- 分析命名约定（camelCase, snake_case, PascalCase）
- 观察代码组织方式（导入顺序、函数/类结构）
- 识别使用的框架和库的模式

**遵循原则：**
- 完全复制现有代码的格式和风格
- 使用相同的导入顺序和分组
- 遵循项目的注释风格
- 保持一致的错误处理方式

**风格检查清单：**
- [ ] 缩进方式一致
- [ ] 命名约定一致
- [ ] 导入顺序一致
- [ ] 代码块组织方式一致
- [ ] 注释风格一致

### 4. 依赖管理

**依赖检查：**
- 读取项目的依赖配置文件：
  - JavaScript/TypeScript: `package.json`
  - Python: `pyproject.toml`, `requirements.txt`, `setup.py`
  - Go: `go.mod`
  - Java: `pom.xml`, `build.gradle`
- 分析已安装的依赖版本
- 检查是否满足新功能需求

**依赖评估：**
- 确定新功能所需的依赖
- 检查现有依赖是否足够
- 识别缺失的依赖

**依赖推荐：**
- 根据功能需求推荐合适的第三方库
- 考虑库的活跃度、维护状态和社区支持
- 选择与项目技术栈兼容的库

**依赖安装：**
- 提供安装命令
- 使用项目包管理器（npm, yarn, pnpm, pip, uv 等）
- 示例命令：
  ```bash
  # JavaScript/TypeScript
  npm install package-name
  yarn add package-name
  pnpm add package-name

  # Python (使用 uv)
  uv add package-name

  # Python (使用 pip)
  pip install package-name
  ```

### 5. 代码质量要求

**注释规范：**
- 仅在关键逻辑点添加注释
- 注释应清晰、简洁、有意义
- 避免注释显而易见的代码
- 使用项目约定的注释语言（中文或英文）

**代码简洁性：**
- 保持函数简短（通常不超过 50 行）
- 遵循单一职责原则
- 避免深层嵌套（通常不超过 3 层）
- 使用有意义的变量和函数名

**模块化原则：**
- 将大功能拆分为小函数
- 每个模块只负责一个功能领域
- 保持模块间的低耦合
- 确保模块的高内聚

**代码质量检查清单：**
- [ ] 函数职责单一
- [ ] 变量命名清晰
- [ ] 无重复代码
- [ ] 适当的错误处理
- [ ] 必要的类型检查
- [ ] 合理的默认值
- [ ] 避免全局变量

### 6. 代码验证

**语法检查：**
- 生成代码后立即执行语法检查
- 根据语言使用相应的检查工具：
  - JavaScript/TypeScript: `eslint`, `tsc --noEmit`
  - Python: `python -m py_compile`, `flake8`, `mypy`
  - Go: `go build`, `gofmt`
  - Java: `javac`

**验证流程：**
1. 生成代码
2. 执行语法检查命令
3. 如果有错误，立即修复
4. 确保代码无语法错误

**测试建议：**
- 不自动运行测试用例
- 提供测试建议和示例
- 建议测试覆盖的关键场景
- 提供测试文件模板

**测试建议内容：**
- 单元测试建议
- 集成测试建议
- 边界条件测试
- 错误处理测试

### 7. 迭代优化

**用户反馈处理：**
- 记录用户的测试反馈
- 根据反馈修改代码
- 优化性能和可读性
- 修复发现的问题

**历史记录维护：**
- 记录代码生成历史
- 保存不同版本的代码
- 便于回溯和比较
- 提供版本变更说明

**优化方向：**
- 性能优化
- 代码可读性提升
- 错误处理改进
- 功能完善
- 依赖精简

## 工作流程

### 阶段 1: 分析阶段

1. **项目结构分析**
   - 扫描项目目录
   - 识别项目类型和技术栈
   - 理解代码组织方式

2. **代码风格分析**
   - 检查现有代码风格
   - 识别命名约定
   - 了解代码组织模式

3. **依赖分析**
   - 读取依赖配置文件
   - 分析现有依赖
   - 评估依赖需求

### 阶段 2: 设计阶段

1. **功能设计**
   - 理解用户需求
   - 设计功能实现方案
   - 确定代码结构

2. **复用分析**
   - 搜索可复用的代码
   - 识别公共模块
   - 规划代码复用策略

3. **依赖规划**
   - 确定需要的依赖
   - 检查依赖可用性
   - 准备安装命令

### 阶段 3: 生成阶段

1. **代码生成**
   - 遵循项目代码风格
   - 实现功能需求
   - 添加必要的注释

2. **代码验证**
   - 执行语法检查
   - 修复语法错误
   - 确保代码质量

3. **依赖安装**
   - 提供安装命令
   - 说明依赖用途
   - 确保兼容性

### 阶段 4: 优化阶段

1. **收集反馈**
   - 记录用户反馈
   - 分析测试结果
   - 识别改进点

2. **代码优化**
   - 根据反馈修改代码
   - 优化性能
   - 提升可读性

3. **文档更新**
   - 更新代码注释
   - 提供使用说明
   - 记录变更历史

## 工具使用指南

### SearchCodebase
用于搜索现有代码，了解项目结构和可复用组件：
```python
# 搜索特定功能
SearchCodebase(information_request="用户认证相关代码")

# 搜索工具函数
SearchCodebase(information_request="公共工具函数和辅助类")
```

### Glob
用于查找特定类型的文件：
```python
# 查找所有 Python 文件
Glob(pattern="**/*.py")

# 查找配置文件
Glob(pattern="**/package.json")
Glob(pattern="**/pyproject.toml")
```

### Read
用于读取文件内容，分析代码风格：
```python
# 读取关键文件了解代码风格
Read(file_path="/path/to/example/file.py", limit=100)
```

### RunCommand
用于执行语法检查和依赖安装：
```python
# Python 语法检查
RunCommand(command="python -m py_compile generated_file.py", blocking=True, requires_approval=False)

# JavaScript 语法检查
RunCommand(command="eslint generated_file.js", blocking=True, requires_approval=False)

# 安装依赖
RunCommand(command="uv add package-name", blocking=True, requires_approval=False)
```

## 最佳实践

### 代码生成原则
1. **先分析，后生成** - 充分理解项目后再生成代码
2. **复用优先** - 优先使用现有代码和组件
3. **风格一致** - 严格遵循项目代码风格
4. **质量第一** - 确保代码质量，不生成有问题的代码
5. **渐进式** - 从简单到复杂，逐步完善

### 常见场景处理

**场景 1: 生成新功能模块**
1. 分析现有模块结构
2. 确定新模块位置
3. 复用公共工具函数
4. 遵循现有代码风格
5. 执行语法检查

**场景 2: 添加 API 端点**
1. 查找现有 API 实现
2. 了解路由配置方式
3. 复用认证和错误处理逻辑
4. 保持一致的响应格式
5. 提供测试建议

**场景 3: 创建数据模型**
1. 查找现有模型定义
2. 了解数据库配置
3. 复用字段类型和验证逻辑
4. 保持一致的命名约定
5. 提供迁移脚本建议

**场景 4: 添加工具函数**
1. 检查现有工具函数
2. 确定放置位置
3. 保持函数签名一致
4. 添加必要的类型检查
5. 提供使用示例

## 注意事项

1. **不要假设** - 不要假设项目使用特定的库或框架，先验证
2. **不要过度设计** - 保持代码简洁，避免不必要的复杂性
3. **不要忽略错误** - 妥善处理所有可能的错误情况
4. **不要硬编码** - 使用配置文件或环境变量
5. **不要生成测试代码** - 只提供测试建议，不自动生成测试用例

## 输出格式

生成的代码应包含：

1. **文件说明** - 文件用途和功能描述
2. **导入部分** - 按项目规范组织导入
3. **代码实现** - 遵循项目风格的代码
4. **关键注释** - 在关键逻辑点添加注释
5. **使用说明** - 如何使用生成的代码（如需要）
6. **依赖说明** - 需要的依赖和安装命令
7. **测试建议** - 建议的测试场景和方法

## 示例输出

```python
"""
用户认证模块

提供用户登录、注册、密码重置等认证功能。
"""

from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt

from .models import User
from .database import get_db
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否正确"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str) -> Optional[User]:
    """验证用户凭据"""
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

## 依赖说明

此技能需要以下依赖（根据项目类型选择）：

**Python 项目：**
- `pydantic` - 数据验证
- `fastapi` - Web 框架（如需要）
- `sqlalchemy` - ORM（如需要）

**JavaScript/TypeScript 项目：**
- `typescript` - TypeScript 编译器
- `eslint` - 代码检查
- `@types/node` - Node.js 类型定义

安装命令：
```bash
# Python
uv add pydantic fastapi sqlalchemy

# JavaScript/TypeScript
npm install --save-dev typescript eslint @types/node
```

## 测试建议

建议测试以下场景：

1. **功能测试** - 验证生成的代码是否实现预期功能
2. **边界测试** - 测试边界条件和异常情况
3. **集成测试** - 验证与现有代码的集成
4. **性能测试** - 测试性能是否满足要求
5. **安全测试** - 检查是否存在安全漏洞

## 常见问题

**Q: 如何确定使用哪个包管理器？**
A: 检查项目根目录的锁定文件（package-lock.json, yarn.lock, pnpm-lock.yaml, uv.lock 等）。

**Q: 如何处理代码风格不一致的情况？**
A: 优先遵循项目主要代码的风格，或者检查是否有 .eslintrc, .prettierrc, pyproject.toml 等配置文件。

**Q: 如何确定代码放置位置？**
A: 分析现有代码的目录结构，将新代码放在逻辑上最合适的位置。

**Q: 生成代码后需要做什么？**
A: 执行语法检查，然后根据用户反馈进行优化。
