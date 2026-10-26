import os
import json
import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.getenv("ZHIPU_API_KEY")
if not key:
    raise SystemExit("请在 .env 中设置 ZHIPU_API_KEY")

client = OpenAI(api_key=key, base_url="https://open.bigmodel.cn/api/paas/v4")
MODEL = "glm-4-flash"


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_file(path):
    base = os.path.abspath(".")
    target = os.path.abspath(os.path.join(base, path))
    if not target.startswith(base):
        return "错误：只能读取项目目录内的文件"
    if not os.path.isfile(target):
        return "错误：文件不存在 " + path
    with open(target, "r", encoding="utf-8") as f:
        return f.read()[:2000]


TOOLS_IMPL = {
    "get_current_time": get_current_time,
    "read_file": read_file,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前本地日期和时间。用户问现在几点、今天几号时必须调用，不要猜测。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取项目目录内的文本文件内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "相对项目根目录的路径，例如 README.md",
                    }
                },
                "required": ["path"],
            },
        },
    },
]


def run_tool(name, args_json):
    try:
        args = json.loads(args_json) if args_json else {}
    except json.JSONDecodeError:
        return "错误：参数不是合法 JSON"
    if name not in TOOLS_IMPL:
        return "错误：未知工具 " + name
    try:
        return str(TOOLS_IMPL[name](**args))
    except Exception as e:
        return "工具执行出错：" + str(e)


messages = [
    {
        "role": "system",
        "content": "你是一个能使用工具的助手。需要时间或文件内容时调用工具，不要凭空编造。",
    }
]

print("工具调用演示，输入 exit 退出")

while True:
    user_input = input("\n你: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit", "退出"):
        break

    messages.append({"role": "user", "content": user_input})

    for _ in range(5):
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )
        msg = resp.choices[0].message

        if not msg.tool_calls:
            print("\nAI:", msg.content)
            messages.append({"role": "assistant", "content": msg.content or ""})
            break

        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
        )

        for tc in msg.tool_calls:
            print("\n[模型请求调用]", tc.function.name, "参数:", tc.function.arguments)
            result = run_tool(tc.function.name, tc.function.arguments)
            print("[工具返回]", result[:200])
            messages.append(
                {"role": "tool", "tool_call_id": tc.id, "content": result}
            )
