import bsinsta as bs
import networkx as nx
import matplotlib.pyplot as plt

# Read instagram data
# ===================
with open('input.txt', 'r') as f:
    inp = f.read().split('\n')

adr = inp[0]
my_username = inp[1]
my_password = inp[2]
fav_list = inp[3:]

my_net, fs_net_dc = bs.get_insta(adr, my_username, my_password, fav_list)

# Create graph
# ============
G = nx.Graph()

nds = fav_list

G.add_nodes_from(nds)

for k,v in fs_net_dc.items():
    eds = [(k, i[1]) for i in v if i[1] in fav_list]
    G.add_edges_from(eds)


nx.draw(G, with_labels=True, font_size=7)
plt.show()
