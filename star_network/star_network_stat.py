import redis
import networkx as nx
from collections import Counter

if __name__ == '__main__':
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)

    G = nx.DiGraph()
    count=Counter()
    keys = red.keys()
    for key in keys:
        nodes = {k: int(v) for k, v in red.hgetall(key).items()}
        count+=Counter(nodes)
        for k, v in nodes.items():
            G.add_edge(k, key, weight=v)

    for k,v in count.most_common():
        print k,v

