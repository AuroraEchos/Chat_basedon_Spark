import SparkApi

#以下密钥信息从控制台获取
appid = ""    
api_secret = ""   
api_key =""    

#配置大模型版本
domain = "generalv3"   
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  

text =[]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def get_answer(user_input):
    dialog = text.copy()
    dialog.append({"role": "user", "content": user_input})
    question = checklen(dialog)
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    answer = SparkApi.answer
    dialog.append({"role": "assistant", "content": answer})
    getText("assistant", answer)
    return answer


