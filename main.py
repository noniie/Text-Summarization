import json 
import re
import string

class Graph:
    def __init__(self, Nodes = []) -> None:
        self.Nodes = Nodes
        self.adj_list = {}

    def add_edge(self, u, v):
        if u not in self.Nodes:
            self.Nodes.append(u)
            self.adj_list[u] = []

        self.adj_list[u].append(v)
    
    def print_adj_list(self):
        for vertex in self.adj_list:
            print(vertex, "->", self.adj_list[vertex])

def read_json(dir):
    with open(dir, 'r') as file:
        data = json.load(file)
    return data

def clean_data(data):
    texts = []
    for msg in data:
        texts.append(msg["full_text"])
    return texts

def text_processing(texts):
    result = []

    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF" 
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
                      "]+", re.UNICODE)
    translator = str.maketrans('', '', string.punctuation)
    
    for text in texts:
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(emoj, '', text)
        text = text.split()
        result.append(text)
    return result

def create_trigramGraph(texts):
    graph = Graph()
    for post in texts:
        for i in range(len(post) - 2):
            bigram1 = post[i] + "-" + post[i+1]
            bigram2 = post[i+1] + "-" + post[i+2]
            graph.add_edge(bigram1, bigram2)

    return graph

def main():
    data = read_json('./data/Itaewon_tragedy.json')
    texts = clean_data(data)
    texts = text_processing(texts)
    graph = create_trigramGraph(texts)
    graph.print_adj_list()

if __name__ == "__main__":
    main()
