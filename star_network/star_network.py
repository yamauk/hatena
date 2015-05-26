import redis
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

if __name__=='__main__':
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)

    G=nx.DiGraph()


    keys=red.keys()
    for key in keys:
        nodes = {k:int(v) for k,v in red.hgetall(key).items()}
        for k,v in nodes.items():
            if v>5 and k!='kiya2015' and k!='kiya2016':
                G.add_edge(k,key,weight=v)

    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=19)
    nx.draw_networkx_edges(G,pos,alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="g")
    pagerank=nx.pagerank_scipy(G,alpha=0.9)
    for k, v in sorted(pagerank.items(),key=lambda x:x[1]):
        print k, v

    # A=nx.to_agraph(G)
    # A.node_attr['shape']='circle'
    # A.node_attr['style']='filled'
    # A.node_attr['width']='0.05'
    # A.node_attr['label']=''
    # A.node_attr['fixedsize']=True
    #
    # A.layout(prog='neato')
    # A.draw('file.png')
    
    plt.axis('off')
    # plt.show()