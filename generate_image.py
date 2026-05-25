import google.genai as genai
from google.genai import types
from PIL import Image
import io
import time
import os

# --- 1. 配置你的 API 密钥 ---
# 确保这里是你自己的密钥
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

# --- 2. 定义图片生成函数 ---
def generate_and_save_image(prompt):
    """使用最新的 SDK 客户端来生成并保存图片。"""
    print(f"正在使用最新版 SDK 生成图片...")
    print(f"提示: '{prompt}'")

    try:
        # 这是最新版库的正确调用方式！
        # 我们通过 client.models 来调用 generate_images
        response = client.models.generate_images(
            model='imagen-4.0-generate-001', # 使用 Imagen 4 模型
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1, # 先生成一张来测试
                aspect_ratio="16:9",
                # sample_image_size="2K",
                person_generation="allow_adult"
            )
        )

        # 检查是否有图片生成
        if not response.generated_images:
            print("错误：API 未返回任何图片。请检查你的提示词是否违反了安全策略。")
            return

        print("图片生成成功！正在保存...")

        # 遍历生成的每张图片并保存
        for i, generated_image in enumerate(response.generated_images):
            # 使用 Pillow 将字节数据转换为图片对象
            image_data = Image.open(io.BytesIO(generated_image.image.image_bytes))
            
            timestamp = int(time.time())
            filename = f"generated_image_{timestamp}_{i+1}.png"

            image_data.save(filename)
            print(f"图片已保存为: {os.path.abspath(filename)}")
            # image_data.show() # 如果你想自动打开图片，可以取消这行的注释

    except Exception as e:
        print(f"生成图片时发生错误: {e}")
        print("这可能是因为 API 密钥无效、模型名称错误或网络问题。")

# --- 3. 主程序入口 ---
if __name__ == "__main__":
    # 使用一个简单的英文提示词开始
    image_prompt = "Ginny Weasley looking brave. Cinema style and character, side view"
    
    generate_and_save_image(image_prompt)