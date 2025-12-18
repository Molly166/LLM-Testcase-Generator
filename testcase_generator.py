"""
大模型测试样例生成器 - AI记账App
支持多维度测试用例生成，输出question、answer、category
"""

import json
import csv
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import random
from datetime import datetime


class Category(Enum):
    """分类枚举"""
    CHAT = "闲聊"
    APP_USAGE = "app使用"
    ACCOUNTING_PRINCIPLE = "记账原理"


class IntentType(Enum):
    """维度一：意图类型"""
    INTENT_INFERENCE = "意图推测"
    ANALYSIS_RECOGNITION = "分析识别"
    ARCHIVE_TASK = "归档任务"


@dataclass
class TestCase:
    """测试用例数据类"""
    question: str
    answer: str
    category: str
    intent_type: str
    scenario: str
    detail: str
    metadata: Optional[Dict[str, Any]] = None


class TestCaseGenerator:
    """测试样例生成器"""
    
    def __init__(self):
        """初始化生成器，加载测试数据模板"""
        self.templates = self._load_templates()
        self.scenarios = self._load_scenarios()
        self.details = self._load_details()
    
    def _load_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """加载测试数据模板"""
        return {
            IntentType.INTENT_INFERENCE.value: {
                Category.CHAT.value: [
                    {
                        "question_template": "我想了解一下{scenario}，{detail}",
                        "answer_template": "关于{scenario}，{detail}，我可以为您提供相关信息。"
                    },
                    {
                        "question_template": "{scenario}是什么意思？{detail}",
                        "answer_template": "{scenario}是指{detail}，在记账中起到重要作用。"
                    }
                ],
                Category.APP_USAGE.value: [
                    {
                        "question_template": "如何使用{scenario}功能？{detail}",
                        "answer_template": "要使用{scenario}功能，您可以{detail}。具体步骤是：1. 打开相应页面 2. 选择功能 3. 完成操作。"
                    },
                    {
                        "question_template": "{scenario}在哪里？{detail}",
                        "answer_template": "{scenario}位于{detail}，您可以通过主菜单找到它。"
                    }
                ],
                Category.ACCOUNTING_PRINCIPLE.value: [
                    {
                        "question_template": "{scenario}的记账原理是什么？{detail}",
                        "answer_template": "{scenario}的记账原理基于{detail}，遵循复式记账法的基本原则。"
                    },
                    {
                        "question_template": "为什么{scenario}要这样记账？{detail}",
                        "answer_template": "{scenario}的记账方式是为了{detail}，确保账目的准确性和可追溯性。"
                    }
                ]
            },
            IntentType.ANALYSIS_RECOGNITION.value: {
                Category.CHAT.value: [
                    {
                        "question_template": "帮我分析一下{scenario}，{detail}",
                        "answer_template": "根据您提供的信息，{scenario}的情况是{detail}。建议您关注以下几个方面。"
                    },
                    {
                        "question_template": "这个{scenario}怎么样？{detail}",
                        "answer_template": "从{detail}来看，{scenario}的情况比较正常，您可以继续观察。"
                    }
                ],
                Category.APP_USAGE.value: [
                    {
                        "question_template": "如何查看{scenario}的分析报告？{detail}",
                        "answer_template": "要查看{scenario}的分析报告，您可以{detail}。报告会显示详细的数据分析结果。"
                    },
                    {
                        "question_template": "{scenario}的数据分析功能怎么用？{detail}",
                        "answer_template": "{scenario}的数据分析功能可以帮助您{detail}，在分析页面选择相应选项即可。"
                    }
                ],
                Category.ACCOUNTING_PRINCIPLE.value: [
                    {
                        "question_template": "如何分析{scenario}的账目？{detail}",
                        "answer_template": "分析{scenario}的账目需要{detail}，通过对比收支情况来判断财务状况。"
                    },
                    {
                        "question_template": "{scenario}的记账数据如何识别？{detail}",
                        "answer_template": "{scenario}的记账数据识别基于{detail}，系统会自动分类和标记。"
                    }
                ]
            },
            IntentType.ARCHIVE_TASK.value: {
                Category.CHAT.value: [
                    {
                        "question_template": "关于{scenario}，{detail}，能保存吗？",
                        "answer_template": "可以的，{scenario}相关的{detail}可以保存到您的账户中，方便以后查看。"
                    },
                    {
                        "question_template": "我想记录{scenario}，{detail}",
                        "answer_template": "好的，我会帮您记录{scenario}，{detail}已保存到系统中。"
                    }
                ],
                Category.APP_USAGE.value: [
                    {
                        "question_template": "如何归档{scenario}？{detail}",
                        "answer_template": "要归档{scenario}，您可以{detail}。归档后的数据可以在历史记录中查看。"
                    },
                    {
                        "question_template": "{scenario}的归档功能在哪里？{detail}",
                        "answer_template": "{scenario}的归档功能在{detail}，您可以选择要归档的内容并确认。"
                    }
                ],
                Category.ACCOUNTING_PRINCIPLE.value: [
                    {
                        "question_template": "{scenario}应该如何归档？{detail}",
                        "answer_template": "{scenario}的归档应该遵循{detail}的原则，确保账目完整性和可追溯性。"
                    },
                    {
                        "question_template": "归档{scenario}时需要注意什么？{detail}",
                        "answer_template": "归档{scenario}时需要注意{detail}，包括时间、金额、分类等信息的准确性。"
                    }
                ]
            }
        }
    
    def _load_scenarios(self) -> Dict[str, List[str]]:
        """加载场景数据"""
        return {
            Category.CHAT.value: [
                "记账的好处", "理财规划", "日常开销", "收入管理", "预算控制",
                "财务健康", "消费习惯", "储蓄目标", "投资理财", "债务管理"
            ],
            Category.APP_USAGE.value: [
                "添加支出", "添加收入", "查看报表", "设置预算", "分类管理",
                "数据导出", "账单提醒", "账户管理", "统计分析", "历史记录"
            ],
            Category.ACCOUNTING_PRINCIPLE.value: [
                "收入记账", "支出记账", "转账记录", "借贷关系", "资产统计",
                "负债管理", "收支平衡", "科目分类", "凭证管理", "账本核对"
            ]
        }
    
    def _load_details(self) -> Dict[str, List[str]]:
        """加载明细数据"""
        return {
            Category.CHAT.value: [
                "能详细说说吗", "有什么建议", "需要注意什么", "有什么技巧",
                "如何开始", "有什么好处", "适合我吗", "难度大吗"
            ],
            Category.APP_USAGE.value: [
                "具体操作步骤", "需要哪些信息", "如何修改", "如何删除",
                "如何筛选", "如何排序", "如何搜索", "如何分享"
            ],
            Category.ACCOUNTING_PRINCIPLE.value: [
                "记账规则", "分类标准", "时间要求", "金额精度",
                "凭证要求", "审核流程", "归档标准", "核对方法"
            ]
        }
    
    def generate_testcase(
        self,
        intent_type: str,
        category: str,
        scenario: Optional[str] = None,
        detail: Optional[str] = None,
        custom_question: Optional[str] = None,
        custom_answer: Optional[str] = None
    ) -> TestCase:
        """
        生成单个测试用例
        
        Args:
            intent_type: 意图类型（意图推测、分析识别、归档任务）
            category: 分类（闲聊、app使用、记账原理）
            scenario: 场景（可选，不提供则随机选择）
            detail: 明细（可选，不提供则随机选择）
            custom_question: 自定义问题（可选）
            custom_answer: 自定义答案（可选）
        
        Returns:
            TestCase对象
        """
        # 验证参数
        if intent_type not in [e.value for e in IntentType]:
            raise ValueError(f"无效的意图类型: {intent_type}")
        if category not in [e.value for e in Category]:
            raise ValueError(f"无效的分类: {category}")
        
        # 选择场景和明细
        if scenario is None:
            scenario = random.choice(self.scenarios[category])
        if detail is None:
            detail = random.choice(self.details[category])
        
        # 选择模板
        templates = self.templates[intent_type][category]
        template = random.choice(templates)
        
        # 生成问题和答案
        if custom_question:
            question = custom_question
        else:
            question = template["question_template"].format(
                scenario=scenario,
                detail=detail
            )
        
        if custom_answer:
            answer = custom_answer
        else:
            answer = template["answer_template"].format(
                scenario=scenario,
                detail=detail
            )
        
        return TestCase(
            question=question,
            answer=answer,
            category=category,
            intent_type=intent_type,
            scenario=scenario,
            detail=detail,
            metadata={
                "generated_at": datetime.now().isoformat(),
                "template_used": template
            }
        )
    
    def generate_batch(
        self,
        count: int,
        intent_types: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        scenarios: Optional[Dict[str, List[str]]] = None,
        details: Optional[Dict[str, List[str]]] = None
    ) -> List[TestCase]:
        """
        批量生成测试用例
        
        Args:
            count: 生成数量
            intent_types: 意图类型列表（可选，不提供则使用全部）
            categories: 分类列表（可选，不提供则使用全部）
            scenarios: 场景字典（可选，覆盖默认场景）
            details: 明细字典（可选，覆盖默认明细）
        
        Returns:
            TestCase列表
        """
        if intent_types is None:
            intent_types = [e.value for e in IntentType]
        if categories is None:
            categories = [e.value for e in Category]
        
        # 覆盖场景和明细
        if scenarios:
            self.scenarios.update(scenarios)
        if details:
            self.details.update(details)
        
        testcases = []
        for _ in range(count):
            intent_type = random.choice(intent_types)
            category = random.choice(categories)
            testcase = self.generate_testcase(intent_type, category)
            testcases.append(testcase)
        
        return testcases
    
    def export_to_json(self, testcases: List[TestCase], filename: str):
        """导出测试用例到JSON文件"""
        data = [asdict(tc) for tc in testcases]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已导出 {len(testcases)} 个测试用例到 {filename}")
    
    def export_to_csv(self, testcases: List[TestCase], filename: str):
        """导出测试用例到CSV文件"""
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['question', 'answer', 'category', 'intent_type', 'scenario', 'detail']
            )
            writer.writeheader()
            for tc in testcases:
                writer.writerow({
                    'question': tc.question,
                    'answer': tc.answer,
                    'category': tc.category,
                    'intent_type': tc.intent_type,
                    'scenario': tc.scenario,
                    'detail': tc.detail
                })
        print(f"已导出 {len(testcases)} 个测试用例到 {filename}")


def main():
    """主函数 - 示例用法"""
    generator = TestCaseGenerator()
    
    print("=" * 60)
    print("大模型测试样例生成器 - AI记账App")
    print("=" * 60)
    
    # 示例1: 生成单个测试用例
    print("\n【示例1】生成单个测试用例")
    testcase = generator.generate_testcase(
        intent_type="意图推测",
        category="app使用",
        scenario="添加支出",
        detail="具体操作步骤"
    )
    print(f"问题: {testcase.question}")
    print(f"答案: {testcase.answer}")
    print(f"分类: {testcase.category}")
    print(f"意图类型: {testcase.intent_type}")
    
    # 示例2: 批量生成测试用例
    print("\n【示例2】批量生成测试用例（10个）")
    testcases = generator.generate_batch(
        count=10,
        intent_types=["意图推测", "分析识别"],
        categories=["闲聊", "app使用"]
    )
    print(f"生成了 {len(testcases)} 个测试用例")
    
    # 示例3: 导出到文件
    print("\n【示例3】导出测试用例")
    generator.export_to_json(testcases, "testcases.json")
    generator.export_to_csv(testcases, "testcases.csv")
    
    # 示例4: 生成覆盖所有维度的测试用例
    print("\n【示例4】生成覆盖所有维度的测试用例")
    all_testcases = []
    for intent_type in [e.value for e in IntentType]:
        for category in [e.value for e in Category]:
            for _ in range(3):  # 每个组合生成3个
                tc = generator.generate_testcase(intent_type, category)
                all_testcases.append(tc)
    
    print(f"生成了 {len(all_testcases)} 个覆盖所有维度的测试用例")
    generator.export_to_json(all_testcases, "testcases_full.json")
    
    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

