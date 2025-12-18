"""
使用示例脚本 - 展示各种使用场景
"""

from testcase_generator import TestCaseGenerator, IntentType, Category
import json


def example_1_basic_usage():
    """示例1: 基本使用"""
    print("\n" + "="*60)
    print("示例1: 基本使用 - 生成单个测试用例")
    print("="*60)
    
    generator = TestCaseGenerator()
    
    testcase = generator.generate_testcase(
        intent_type="意图推测",
        category="app使用",
        scenario="添加支出",
        detail="具体操作步骤"
    )
    
    print(f"\n问题: {testcase.question}")
    print(f"答案: {testcase.answer}")
    print(f"分类: {testcase.category}")
    print(f"意图类型: {testcase.intent_type}")
    print(f"场景: {testcase.scenario}")
    print(f"明细: {testcase.detail}")


def example_2_batch_generation():
    """示例2: 批量生成"""
    print("\n" + "="*60)
    print("示例2: 批量生成测试用例")
    print("="*60)
    
    generator = TestCaseGenerator()
    
    # 生成20个测试用例，覆盖指定的意图类型和分类
    testcases = generator.generate_batch(
        count=20,
        intent_types=["意图推测", "分析识别", "归档任务"],
        categories=["闲聊", "app使用", "记账原理"]
    )
    
    print(f"\n生成了 {len(testcases)} 个测试用例")
    
    # 统计各分类的数量
    category_count = {}
    intent_count = {}
    for tc in testcases:
        category_count[tc.category] = category_count.get(tc.category, 0) + 1
        intent_count[tc.intent_type] = intent_count.get(tc.intent_type, 0) + 1
    
    print("\n分类统计:")
    for cat, count in category_count.items():
        print(f"  {cat}: {count}个")
    
    print("\n意图类型统计:")
    for intent, count in intent_count.items():
        print(f"  {intent}: {count}个")
    
    # 导出
    generator.export_to_json(testcases, "example_batch.json")
    generator.export_to_csv(testcases, "example_batch.csv")


def example_3_full_coverage():
    """示例3: 全覆盖生成"""
    print("\n" + "="*60)
    print("示例3: 生成覆盖所有维度的测试用例")
    print("="*60)
    
    generator = TestCaseGenerator()
    all_testcases = []
    
    # 遍历所有维度组合，每个组合生成2个测试用例
    for intent_type in IntentType:
        for category in Category:
            for i in range(2):
                tc = generator.generate_testcase(
                    intent_type.value,
                    category.value
                )
                all_testcases.append(tc)
                print(f"生成: [{intent_type.value}] + [{category.value}] - {tc.question[:30]}...")
    
    print(f"\n总共生成了 {len(all_testcases)} 个测试用例")
    print(f"维度组合数: {len(IntentType) * len(Category)}")
    print(f"每个组合生成: 2个")
    
    generator.export_to_json(all_testcases, "example_full_coverage.json")


def example_4_custom_scenarios():
    """示例4: 自定义场景和明细"""
    print("\n" + "="*60)
    print("示例4: 使用自定义场景和明细")
    print("="*60)
    
    generator = TestCaseGenerator()
    
    # 自定义场景和明细
    custom_scenarios = {
        "app使用": ["自定义功能1", "自定义功能2", "自定义功能3"]
    }
    custom_details = {
        "app使用": ["自定义明细1", "自定义明细2"]
    }
    
    testcases = generator.generate_batch(
        count=10,
        intent_types=["意图推测"],
        categories=["app使用"],
        scenarios=custom_scenarios,
        details=custom_details
    )
    
    print(f"\n生成了 {len(testcases)} 个使用自定义场景的测试用例")
    for i, tc in enumerate(testcases[:3], 1):
        print(f"\n{i}. 问题: {tc.question}")
        print(f"   场景: {tc.scenario}")
        print(f"   明细: {tc.detail}")
    
    generator.export_to_json(testcases, "example_custom.json")


def example_5_category_focused():
    """示例5: 针对特定分类生成"""
    print("\n" + "="*60)
    print("示例5: 针对特定分类生成测试用例")
    print("="*60)
    
    generator = TestCaseGenerator()
    
    # 只生成"app使用"分类的测试用例
    testcases = generator.generate_batch(
        count=15,
        intent_types=["意图推测", "分析识别", "归档任务"],
        categories=["app使用"]
    )
    
    print(f"\n生成了 {len(testcases)} 个'app使用'分类的测试用例")
    
    # 按意图类型分组显示
    grouped = {}
    for tc in testcases:
        if tc.intent_type not in grouped:
            grouped[tc.intent_type] = []
        grouped[tc.intent_type].append(tc)
    
    for intent_type, tcs in grouped.items():
        print(f"\n{intent_type} ({len(tcs)}个):")
        for tc in tcs[:2]:  # 只显示前2个
            print(f"  - {tc.question}")
    
    generator.export_to_json(testcases, "example_app_usage.json")


def example_6_statistics():
    """示例6: 生成统计报告"""
    print("\n" + "="*60)
    print("示例6: 生成测试用例统计报告")
    print("="*60)
    
    generator = TestCaseGenerator()
    
    # 生成大量测试用例用于统计
    testcases = generator.generate_batch(count=100)
    
    # 统计信息
    stats = {
        "total": len(testcases),
        "by_category": {},
        "by_intent": {},
        "by_combination": {}
    }
    
    for tc in testcases:
        # 按分类统计
        stats["by_category"][tc.category] = stats["by_category"].get(tc.category, 0) + 1
        
        # 按意图类型统计
        stats["by_intent"][tc.intent_type] = stats["by_intent"].get(tc.intent_type, 0) + 1
        
        # 按组合统计
        combo = f"{tc.intent_type}+{tc.category}"
        stats["by_combination"][combo] = stats["by_combination"].get(combo, 0) + 1
    
    print(f"\n总测试用例数: {stats['total']}")
    
    print("\n按分类分布:")
    for cat, count in sorted(stats["by_category"].items()):
        percentage = (count / stats["total"]) * 100
        print(f"  {cat}: {count}个 ({percentage:.1f}%)")
    
    print("\n按意图类型分布:")
    for intent, count in sorted(stats["by_intent"].items()):
        percentage = (count / stats["total"]) * 100
        print(f"  {intent}: {count}个 ({percentage:.1f}%)")
    
    print("\n维度组合分布 (前10个):")
    sorted_combos = sorted(stats["by_combination"].items(), key=lambda x: x[1], reverse=True)
    for combo, count in sorted_combos[:10]:
        print(f"  {combo}: {count}个")
    
    # 保存统计报告
    with open("statistics_report.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print("\n统计报告已保存到 statistics_report.json")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("大模型测试样例生成器 - 使用示例")
    print("="*60)
    
    try:
        example_1_basic_usage()
        example_2_batch_generation()
        example_3_full_coverage()
        example_4_custom_scenarios()
        example_5_category_focused()
        example_6_statistics()
        
        print("\n" + "="*60)
        print("所有示例运行完成！")
        print("="*60)
        print("\n生成的文件:")
        print("  - example_batch.json / example_batch.csv")
        print("  - example_full_coverage.json")
        print("  - example_custom.json")
        print("  - example_app_usage.json")
        print("  - statistics_report.json")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

