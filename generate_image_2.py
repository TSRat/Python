import google.genai as genai
from google.genai import types
import os

# --- 1. 配置你的 API 密钥 ---
try:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("未找到环境变量 GOOGLE_API_KEY")
        exit()

    client = genai.Client(api_key=api_key) 
except Exception as e:
    print(f"API 密钥配置或客户端创建失败: {e}")
    print("请确保你已经将 'YOUR_API_KEY' 替换为你的真实密钥。")
    exit()

# --- 2. 定义一个只用于诊断的函数 ---
def inspect_the_response(prompt):
    """
    这个函数的目标不是保存图片，而是打印出成功返回的图片对象的内部结构。
    """
    print("--- 正在启动最终诊断程序 ---")
    print(f"提示: '{prompt}'")

    try:
        # 再次调用 API 获取图片
        response = client.models.generate_images(
            model='imagen-4.0-generate-001', 
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1)
        )

        if not response.generated_images:
            print("错误：API 未返回任何图片。")
            return

        print("\n>>> 诊断关键点：图片已成功生成并返回！ <<<")

        # 获取返回的第一个图片对象
        generated_image = response.generated_images[0]

        # --- 开始打印诊断信息 ---
        print("\n--- 对象结构分析 ---")
        
        # 打印 generated_image.image 变量的类型
        print(f"变量 'generated_image.image' 的确切类型是: {type(generated_image.image)}")
        
        # 打印出这个对象内部所有的属性和方法！
        print("\n'generated_image.image' 对象拥有的所有属性和方法列表:")
        print(dir(generated_image.image))
        
        print("\n--- 诊断结束 ---")
        print("\n请将上面从 '--- 对象结构分析 ---' 开始的全部内容复制并回复给我。")
        print("这个列表里一定包含着我们需要的那个正确的名字。")

    except Exception as e:
        print(f"在诊断过程中发生错误: {e}")

# --- 3. 运行诊断程序 ---
if __name__ == "__main__":
    # 使用一个最简单的提示词来确保成功返回
    inspect_the_response("a circle")