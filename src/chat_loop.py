import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.getenv("ZHIPU_API_KEY")
if not key:
    raise SystemExit("请在 .env 中设置 ZHIPU_API_KEY")

client = OpenAI(api_key=key, base_url="https://open.bigmodel.cn/api/paas/v4")

messages = [
    {"role": "system", "content": "你是一个简洁、准确的中文助手。"}
]

print("开始对话，输入 exit 退出")

while True:
    user_input = input("\n你: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit", "退出"):
        break

    messages.append({"role": "user", "content": user_input})

    try:
        resp = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
        )
        reply = resp.choices[0].message.content
    except Exception as e:
        print("调用失败:", e)
        messages.pop()
        continue

    print("AI:", reply)
    messages.append({"role": "assistant", "content": reply})

