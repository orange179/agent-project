import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.getenv("ZHIPU_API_KEY")
if not key:
    raise SystemExit("请在 .env 中设置 ZHIPU_API_KEY")

client = OpenAI(
    api_key=key,
    base_url="https://open.bigmodel.cn/api/paas/v4",
)

resp = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {"role": "user", "content": "用一句话解释什么是数据库"}
    ],
)

print(resp.choices[0].message.content)
