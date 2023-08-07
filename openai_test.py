import datetime
import openai

from robot import config

if __name__ == "__main__":

    # Load config
    CONFIG = config.get("openai", {})
    openai.api_key = CONFIG['openai_api_key']
    model = CONFIG['model']
    max_tokens = CONFIG['max_tokens']
    
    context = []
    max_hist = 6 # 2 rounds of conversation. The first one is system message, second one is assistant notice.

    sys_prompt_string = "ETC欠费情况是因为车辆经过ETC的时候,就算账户里没有钱,杆子也会先抬起来以保证交通畅通。" + \
                    "你是一个专业的智能催收客服,你的目标是告诉客户他们欠费了。并让他们在短时间内还款以便不" + \
                    "影响以后的ETC使用。你还会回答任何跟ETC有关的问题,并把回答控制在一两句话以内。如果用户" + \
                    "问了不相关的问题，请不要回答并告诉他们你是个专门负责催收的客服。"
    ast_prompt_string = "您好, 我是你的智能助手。您于7月11日在北京南收费站欠款200元,请通过ETC小程序及时还款," + \
                        "以免影响以后的ETC使用。如有疑问,请您在提示音播放后回复。"
    system_prompt = {"role": "system", "content": sys_prompt_string}
    ast_prompt = {"role": "assistant", "content": ast_prompt_string}
    context.append(system_prompt)
    context.append(ast_prompt)
    print(context)
    exit()
    
    while True:
        try:
            q = input("用户：").rstrip()
            if q == 'q':
                break
            context.append({"role": "user", "content": q})
            while len(context) > max_hist:
                context.pop(2)
            completion = openai.ChatCompletion.create(
                model=model,
                messages= context,
                max_tokens=max_tokens
            )
            response = completion.choices[0].message.content
            print(f"客服: {response}")
            context.append({"role": "assistant", "content": response})
            usage = completion.usage
            with open('openai_usage.txt', 'a') as f: 
                timestamp = datetime.datetime.now()
                f.write(f"{usage['prompt_tokens']}, {usage['completion_tokens']}, {timestamp}\n") 
        except EOFError:
            break
        
