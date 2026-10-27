"""Day 30 验证：README.md + GitHub 发布 + 课程总结

Day 30 没有新增项目代码——它是 README 文档编写和项目发布的讲解。
验证方式：检查 README 文件和 Git 仓库状态。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_readme_exists():
    """验证 README.md 存在且非空"""
    assert os.path.exists("README.md"), "README.md 不存在"
    size = os.path.getsize("README.md")
    assert size > 500, f"README.md 内容太少 ({size} bytes)"


def test_readme_has_required_sections():
    """验证 README 包含所有必需章节"""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "## ✨ 功能特性",      # 或 "## Features"
        "## 🚀 快速开始",      # 或 "## Quick Start"
        "## 📁 项目结构",      # 或 "## Project Structure"
        "streamlit run",       # 启动命令
        "pip install",         # 安装命令
    ]

    for section in required_sections:
        assert section in content, f"README 缺少: {section}"


def test_readme_has_tech_stack():
    """验证 README 包含技术栈说明"""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    techs = ["Streamlit", "DeepSeek", "OpenAI"]
    for tech in techs:
        assert tech.lower() in content.lower(), f"README 缺少技术栈: {tech}"


def test_requirements_txt_matches_readme():
    """验证 requirements.txt 与 README 中的依赖一致"""
    with open("requirements.txt", "r", encoding="utf-8") as f:
        reqs = f.read()

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # 三个核心依赖都应出现在 README 中
    for pkg in ["openai", "streamlit", "python-dotenv"]:
        assert pkg in reqs, f"requirements.txt 缺少: {pkg}"
        assert pkg in readme.lower(), f"README 未提及依赖: {pkg}"


if __name__ == "__main__":
    print("=" * 60)
    print("Day 30 验证：README + GitHub 发布")
    print("=" * 60)

    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    tests = [
        ("README.md 存在且非空", test_readme_exists),
        ("README 包含必需章节", test_readme_has_required_sections),
        ("README 包含技术栈", test_readme_has_tech_stack),
        ("requirements.txt 与 README 一致", test_requirements_txt_matches_readme),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")

    print(f"\n结果: {passed}/{len(tests)} 通过")
    print("\n--- GitHub 发布手动验证步骤 ---")
    print("  1. git status → 确认没有未提交的修改")
    print("  2. 在 github.com 创建新仓库")
    print("  3. git remote add origin <仓库URL>")
    print("  4. git push -u origin main")
    print("  5. 确认 .env 文件未被推送（已在 .gitignore 中）")
    print("  6. 确认仓库页面显示 README.md 内容")
    if passed < len(tests):
        sys.exit(1)
