from openai import OpenAI


# my api is sk-83d911caad734810a0b087c99e57b562

class AI:
    def __init__(self, initial_command: str, api: str):
        self.content = [{"role":"system", "content":initial_command}]
        self.client = OpenAI(
            api_key=api,
            base_url="https://api.deepseek.com")
    
    def chat(self, message: str, role = "user", content = [], temp = 0.7, stream = False):
        if (content == []):
            content = self.content

        content.append({"role":role,"content":message})
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=content,
            temperature=temp,
            stream=stream
        )

        return response
    
    def premanage():
        pass




# 使用示例
if __name__ == "__main__":
    ai = AI("你是一个指令解析器，有如下指令：o(x,y,z)相对坐标系下移动, p(x,y,z)绝对坐标系下移动", 
            "sk-83d911caad734810a0b087c99e57b562")
    
    