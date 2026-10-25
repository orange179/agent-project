"""项目入口：验证 .env 能被正确读取。"""
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请先复制 .env.example 为 .env，并填入真实 API Key")
        return
    print(f"骨架启动成功，已读取到密钥（前6位：{api_key[:6]}...）")

if __name__ == "__&#8203;main__":
    main()
