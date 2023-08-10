import pinecone

from robot import config
from ernie import Ernie

def read_data(path):
    prompts, ids = [], []
    with open(path, "r") as f:
        for line in f:
            idx, prompt = line.rstrip().split("###")
            prompts.append(prompt)
            ids.append(idx)
    return prompts, ids

if __name__ == "__main__":

    # Init vector DB and connect to the "ccb-etc-assisstant" index
    CONFIG = config.get("pinecone", {})
    env = CONFIG['env']
    api_key = CONFIG['api_key']
    pinecone.init(api_key=api_key, environment=env)
    index = pinecone.Index("ccb-etc-assisstant")
    
    # Load config and init LLM
    CONFIG = config.get("ernie", {})
    appid = CONFIG['appid']
    api_key = CONFIG['api_key']
    secret_key = CONFIG['secret_key']
    
    ernie = Ernie(api_key, secret_key)
    
    # # Read data from txt file
    # path = "knowledge.txt"
    
    # prompts, ids = read_data(path)
    
    # # Embedd the prompts
    # embeddings = ernie.embedd(prompts)
    
    # # Upsert into db
    # metadatas = [{'text': prompt} for prompt in prompts]
    # data = zip(ids, embeddings, metadatas)
    # index.upsert(data)
    
    # Query a prompt
    query = "我想要人工客服"
    query_embedding = ernie.embedd([query])[0]
    result = index.query(
        vector=query_embedding,
        top_k=2,
        include_metadata=True
    )
    informations = [item['metadata']['text'] for item in result['matches']]
    print(informations)
    
    
