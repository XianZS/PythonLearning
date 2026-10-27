"""运行所有 Day 11-30 的测试

用法：
    cd Intelligent_Chat_Programming_Assistant
    python tests/run_all.py
"""

import subprocess
import sys
import os

# 确保在项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_files = [
    ("Day 11: deepseek_client.py", "tests/test_day11_deepseek_client.py"),
    ("Day 12: 异常处理验证", "tests/test_day12_exceptions.py"),
    ("Day 13: Streamlit 骨架", "tests/test_day13_streamlit_skeleton.py"),
    ("Day 14: Markdown 练习", "tests/test_day14_markdown.py"),
    ("Day 15: ui/utils.py", "tests/test_day15_ui_utils.py"),
    ("Day 16: chat_input", "tests/test_day16_chat_input.py"),
    ("Day 17-20: chat_area.py", "tests/test_day17_20_chat_area.py"),
    ("Day 21: session_state", "tests/test_day21_session_state.py"),
    ("Day 22-24: chat_manager.py", "tests/test_day22_24_chat_manager.py"),
    ("Day 25-27: sidebar.py", "tests/test_day25_27_sidebar.py"),
    ("Day 28: stream_handler.py", "tests/test_day28_stream_handler.py"),
    ("Day 29: app.py 编排", "tests/test_day29_app_integration.py"),
    ("Day 30: README 验证", "tests/test_day30_readme.py"),
]

print("=" * 60)
print("Running All Day 11-30 Tests")
print("=" * 60)

passed = 0
failed = 0

for day_label, test_file in test_files:
    print(f"\n{'-' * 40}")
    print(f"[{day_label}]")
    print(f"   {test_file}")

    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode == 0:
        print("   [PASS]")
        passed += 1
    else:
        print(f"   [FAIL] (exit code: {result.returncode})")
        # 打印最后几行输出看错误信息
        stderr_lines = result.stderr.strip().split("\n")
        stdout_lines = result.stdout.strip().split("\n")
        for line in (stderr_lines[-5:] + stdout_lines[-5:]):
            if line.strip():
                print(f"      {line}")
        failed += 1

print(f"\n{'=' * 60}")
print(f"Result: {passed} passed, {failed} failed, {len(test_files)} total")
print(f"{'=' * 60}")

if failed > 0:
    sys.exit(1)
