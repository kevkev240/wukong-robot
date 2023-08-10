import requests
import json
from tqdm.auto import tqdm

from robot import config

class Ernie():
    
    def __init__(self, api_key, secret_key, initial_message=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.auth_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}'
        self.access_token = self.get_access_token()
        self.embedd_url = f'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token={self.access_token}'
        self.batch_size = 16 # maximum for the test "Error: 336003: embeddings max batch size is 16, and can not be 0"
        self.chat_url = f'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={self.access_token}'
        self.context = []
        self.max_turn = 3

    def get_access_token(self):
        """
        使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
        Expires every 30 days
        """
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", self.auth_url, headers=headers, data=payload)
        
        return response.json().get("access_token")
        
    def embedd(self, prompts):
        
        L = len(prompts)
        i = 0
        embeddings = []
        
        for i in tqdm(range(0, L, self.batch_size)):
            batch_prompts = prompts[i : i + self.batch_size]
            batch_embeddings = self.embedd_batch(batch_prompts)
            embeddings.extend(batch_embeddings)
            
        return embeddings
    
    def embedd_batch(self, batch_prompts):
        
        payload = json.dumps({
            "input": batch_prompts
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", self.embedd_url, headers=headers, data=payload)
        
        res = response.json()
        
        err_code = res.get("error_code", "ok")
        if err_code != "ok":
            print(f"Error {err_code}: {res.get('error_msg')}")
            
        batch_embeddings = [item['embedding'] for item in res.get('data')]
        
        return batch_embeddings
        
    def chat(self, msg):

        while len(self.context) > (self.max_turn * 2):
            self.context.pop(0)
        
        self.context.append({"role": "user", "content": msg})
    
        payload = json.dumps({
            "messages": self.context
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", self.chat_url, headers=headers, data=payload)
        
        res = response.json()
        
        err_code = res.get("error_code", "ok")
        if err_code != "ok":
            print(f"Error {err_code}: {res.get('error_msg')}")
            
        result = res.get("result")
        
        self.context.append({"role": "assistant", "content": result})
        
        return result
    
if __name__ == "__main__":

    # Load config
    CONFIG = config.get("ernie", {})
    appid = CONFIG['appid']
    api_key = CONFIG['api_key']
    secret_key = CONFIG['secret_key']
    
    ernie = Ernie(api_key, secret_key)
    
    # prompts = ["推荐一些美食","给我讲个故事"]
    # embeddings = ernie.embedd(prompts)
    
    # print(embeddings)
    
    # Sample convo
    res = ernie.chat("你好你是谁")
    print(res)
    res = ernie.chat("我叫孙悟空")
    print(res)
    res = ernie.chat("我叫什么")
    print(res)
    res = ernie.chat("25*20等于几")
    print(res)
    res = ernie.chat("拜拜")
    print(res)
    print(ernie.context)    

    