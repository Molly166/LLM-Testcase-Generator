# LLM-Testcase-Generator

大模型测试样例生成器 - 专为AI记账App设计

## 项目简介

这是一个基于Python开发的测试样例生成器，用于生成AI记账类型App的测试用例。生成的测试用例包含三个核心部分：**question**（问题）、**answer**（答案）、**category**（分类）。

## 功能特性

- ✅ 多维度测试用例生成
  - **维度一**：意图类型（意图推测、分析识别、归档任务）
  - **维度二**：场景和明细
- ✅ 三种分类支持：闲聊、app使用、记账原理
- ✅ 灵活的模板系统，支持自定义
- ✅ 批量生成功能
- ✅ 多格式导出（JSON、CSV）

## 项目结构

```
LLM-Testcase-Generator/
├── testcase_generator.py  # 核心生成器
├── config.py              # 配置文件
├── requirements.txt       # 依赖包
└── README.md             # 说明文档
```

## 快速开始

### 1. 环境要求

- Python 3.7+
- 无需额外依赖（使用Python标准库）

### 2. 基本使用

#### 生成单个测试用例

```python
from testcase_generator import TestCaseGenerator

generator = TestCaseGenerator()

# 生成单个测试用例
testcase = generator.generate_testcase(
    intent_type="意图推测",
    category="app使用",
    scenario="添加支出",
    detail="具体操作步骤"
)

print(f"问题: {testcase.question}")
print(f"答案: {testcase.answer}")
print(f"分类: {testcase.category}")
```

#### 批量生成测试用例

```python
# 批量生成10个测试用例
testcases = generator.generate_batch(
    count=10,
    intent_types=["意图推测", "分析识别"],
    categories=["闲聊", "app使用"]
)

# 导出到JSON
generator.export_to_json(testcases, "testcases.json")

# 导出到CSV
generator.export_to_csv(testcases, "testcases.csv")
```

#### 生成覆盖所有维度的测试用例

```python
from testcase_generator import TestCaseGenerator, IntentType, Category

generator = TestCaseGenerator()
all_testcases = []

# 遍历所有维度组合
for intent_type in IntentType:
    for category in Category:
        for _ in range(3):  # 每个组合生成3个
            tc = generator.generate_testcase(
                intent_type.value, 
                category.value
            )
            all_testcases.append(tc)

generator.export_to_json(all_testcases, "testcases_full.json")
```

### 3. 运行示例

直接运行主程序查看示例：

```bash
python testcase_generator.py
```

## 维度说明

### 维度一：意图类型

1. **意图推测** - 识别和推测用户的意图
2. **分析识别** - 数据分析和内容识别
3. **归档任务** - 数据归档和任务管理

### 维度二：场景和明细

根据不同的分类（category），场景和明细会有所不同：

- **闲聊**：记账的好处、理财规划、日常开销等
- **app使用**：添加支出、查看报表、设置预算等
- **记账原理**：收入记账、支出记账、转账记录等

## 输出格式

### JSON格式示例

```json
[
  {
    "question": "如何使用添加支出功能？具体操作步骤",
    "answer": "要使用添加支出功能，您可以具体操作步骤。具体步骤是：1. 打开相应页面 2. 选择功能 3. 完成操作。",
    "category": "app使用",
    "intent_type": "意图推测",
    "scenario": "添加支出",
    "detail": "具体操作步骤",
    "metadata": {
      "generated_at": "2024-01-01T12:00:00",
      "template_used": {...}
    }
  }
]
```

### CSV格式示例

| question | answer | category | intent_type | scenario | detail |
|----------|--------|----------|-------------|----------|--------|
| 如何使用添加支出功能？具体操作步骤 | 要使用添加支出功能，您可以... | app使用 | 意图推测 | 添加支出 | 具体操作步骤 |

## 自定义配置

可以通过修改 `config.py` 文件来自定义：

- 添加新的场景和明细
- 修改问题模板
- 调整生成权重
- 配置导出格式

## 扩展开发

### 添加新的分类

1. 在 `testcase_generator.py` 的 `Category` 枚举中添加新分类
2. 在 `config.py` 的 `CATEGORIES` 中添加对应的场景和明细
3. 在 `_load_templates()` 方法中添加对应的模板

### 添加新的意图类型

1. 在 `testcase_generator.py` 的 `IntentType` 枚举中添加新类型
2. 在 `config.py` 的 `INTENT_TYPES` 中添加定义
3. 在 `_load_templates()` 方法中添加对应的模板

## 注意事项

- 生成的测试用例基于模板，可以根据实际需求调整模板内容
- 建议根据实际业务场景修改场景和明细列表
- 导出CSV文件使用UTF-8-BOM编码，可在Excel中正常打开

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！