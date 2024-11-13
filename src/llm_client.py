from zhipuai import ZhipuAI
import json

def load_api_key(platform):
    with open(r"C:\Users\86187\Desktop\api_key.json", "r", encoding="utf-8") as f:
        api_dict = json.load(f)
    return api_dict.get(platform, None)


client = ZhipuAI(api_key=load_api_key("zhipu"))

model="glm-4-plus"