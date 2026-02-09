# RAG系统自动化评估 - 使用本地Ollama模型

基于notebook `2_4_自动化评测答疑机器人的表现.ipynb` 中3.1.1章节的代码，实现了使用本地Ollama模型进行RAG系统自动化评估的功能。

## 项目结构

```
app/
├── config.py                  # Ollama和测试配置
├── factory.py                # 组件工厂
├── ragas_ollama_wrapper.py   # Ollama LLM包装器
├── ollama_embeddings.py      # Ollama Embeddings包装器
├── logger.py                # 日志配置
├── ragas_test_ollama.py    # Ragas评估核心逻辑
├── main_ollama_ragas.py    # 主程序入口
├── test_ollama_connection.py # Ollama连接测试
├── test_components.py       # 组件测试
└── simple_ragas_test.py     # 简单Ragas评估测试

utils/
└── ollama_client.py         # Ollama客户端封装
```

## 功能特性

1. **双模型支持**：
   - 主模型：`qwen3:8b` 用于生成和评估
   - Embedding模型：`bge-m3:latest` 用于向量嵌入

2. **完整的错误处理**：
   - 自动重试机制（最多3次）
   - 详细的错误日志
   - 友好的错误提示

3. **多种评估指标**：
   - Answer Correctness（答案准确度）
   - Context Recall（上下文召回率）
   - Context Precision（上下文精确度）

4. **灵活的配置**：
   - 支持自定义模型参数
   - 支持自定义测试数据
   - 支持自定义Ollama服务地址

## 使用方法

### 1. 确保Ollama服务运行

```bash
# 启动Ollama服务
ollama serve

# 拉取所需模型（如果还没有）
ollama pull qwen3:8b
ollama pull bge-m3:latest
```

### 2. 测试Ollama连接

```bash
python app/test_ollama_connection.py
```

### 3. 测试组件

```bash
python app/test_components.py
```

### 4. 运行简单评估测试

```bash
python app/simple_ragas_test.py
```

### 5. 运行完整评估

```bash
python app/main_ollama_ragas.py
```

## 评估结果说明

### Answer Correctness（答案准确度）
- 范围：0-1
- 越接近1表示答案越准确
- 示例结果：
  - 无效答案：0.149547
  - 幻觉答案：0.188627
  - 正确答案：0.993943

### Context Recall（上下文召回率）
- 范围：0-1
- 越接近1表示检索到的相关文档越完整

### Context Precision（上下文精确度）
- 范围：0-1
- 越接近1表示检索到的文档相关性越高且排序越靠前

## 配置说明

在 `app/config.py` 中可以修改默认配置：

```python
@dataclass
class OllamaConfig:
    model: str = "qwen3:8b"              # 主模型
    embedding_model: str = "bge-m3:latest" # Embedding模型
    base_url: Optional[str] = None         # Ollama服务地址
    timeout: int = 120                     # 超时时间（秒）
    temperature: float = 0.7                # 温度参数
    top_p: float = 0.9                    # Top-p参数
```

## 自定义测试数据

在 `app/config.py` 中修改 `TestConfig`：

```python
@dataclass
class TestConfig:
    questions: list = None      # 问题列表
    answers: list = None       # RAG系统回答列表
    ground_truths: list = None # 正确答案列表
    contexts: list = None      # 检索到的上下文列表
```

## 注意事项

1. 确保Ollama服务已启动并可访问
2. 确保所需的模型已下载
3. 评估过程可能需要较长时间，请耐心等待
4. 如果遇到连接问题，请检查Ollama服务地址和端口

## 依赖项

- ollama
- ragas
- langchain-core
- datasets
- 其他依赖见 `requirements.txt`

## 示例输出

```
================================================================================
RAG系统自动化评估 - 使用本地Ollama模型
================================================================================
模型: qwen3:8b
地址: http://localhost:11434
================================================================================

================================================================================
1. 评估答案准确度 (Answer Correctness)
================================================================================
    question  ... answer_correctness
0  张伟是哪个部门的？  ...           0.149547
1  张伟是哪个部门的？  ...           0.188627
2  张伟是哪个部门的？  ...           0.993943

================================================================================
评估完成！
================================================================================
```
