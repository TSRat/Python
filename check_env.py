import sys
import os

print("--- Python Environment Check ---")

# 1. 打印当前正在执行此脚本的 Python 解释器的路径
print(f"Python Executable: {sys.executable}")
print("-" * 20)

# 2. 尝试导入 google.generativeai 并打印它的文件位置
try:
    import google.generativeai as genai
    print("Successfully imported 'google.generativeai'")
    
    # 获取模块的安装位置
    # __file__ 属性指向模块的 __init__.py 文件
    module_path = genai.__file__
    print(f"Module Location: {module_path}")
    print("-" * 20)
    
    # 打印出模块的所有可用属性，让我们看看里面到底有什么
    print("Available attributes in 'genai':")
    print(dir(genai))
    
except ImportError:
    print("ERROR: Failed to import 'google.generativeai'.")
    print("This means the library is not installed in the environment above.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("\n--- End of Check ---")