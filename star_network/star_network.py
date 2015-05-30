import redis
import networkx as nx

if __name__ == '__main__':
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)

    G = nx.DiGraph()

    keys = red.keys()
    for key in keys:
        nodes = {k: int(v) for k, v in red.hgetall(key).items()}
        for k, v in nodes.items():
            G.add_edge(k, key, weight=v)

    pagerank = nx.pagerank_scipy(G, alpha=0.9)
    for k, v in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
        print  k, v

