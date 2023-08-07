from robot import AI
from robot import config
from robot.sdk import SparkApi as spark

if __name__ == "__main__":

    # spark API test
    CONFIG = config.get("spark", {})
    wsParam = spark.Ws_Param(CONFIG['appid'], 
                       CONFIG['api_key'], 
                       CONFIG['api_secret'], 
                       "wss://spark-api.xf-yun.com/v1.1/chat")
    # messages = [{"role": "user", "content": "说你好"}]
    messages = [{"role": "user", "content": "你好我叫秦睦然，我喜欢猫"},
                {"role": "assistant", "content": "你好秦睦然，我叫悟空"},
                {"role": "user", "content": "你刚才说了什么"}]
    res = spark.getMessage(wsParam, messages)
    print(res)
    
    # # spark AI instance test
    # spark = AI.get_robot_by_slug("spark")
    # while True:
    #     try:
    #         q = input("用户：").rstrip()
    #         res = spark.chat(q)
    #         print(res)
    #     except EOFError:
    #         break
    
    