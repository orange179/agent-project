import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print("脚本已运行")
print("读到密钥：" + (key[:6] + "..." if key else "未读到"))
