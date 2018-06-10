import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('Lekagul Sensor Data.csv')
data = data[data['car-type'] == '2P'] # test out data only on car type 3
# sort by car-id then timestamp
data.sort_values(['car-id', 'Timestamp'], inplace=True)

# get the next gate that the car went to
data['next-gate'] = None
data.reset_index(inplace=True, drop=True)

for i in range(data.shape[0]):
    try:
        if data['car-id'][i] == data['car-id'][i + 1]: # if the car id of the current row is the same as the next row
            data['next-gate'][i] = data['gate-name'][i + 1] # get the next gate the car has arrived at
    except:
        pass


clearedData = data.dropna(axis=0) # remove those at the end of their journey
links_df = clearedData.groupby(['gate-name', 'next-gate']).size().reset_index().rename(columns={0: 'count'})



# -----------------------------------------------
# now initialise a dictionary to contain  nodes information
gates = {}
fill = {}

for item in set(links_df['gate-name']):
    if 'camping' in item:
        gates[item] = 1
        fill[item] = '#B7B7B7'

    if 'entrance' in item:
        gates[item] = 2
        fill[item] = '#CEB7B3'

    if 'general-gate' in item:
        gates[item] = 3
        fill[item] = '#F7B2AD'


    if 'ranger-stop' in item:
        gates[item] = 4
        fill[item] = '#9ABCA7'

    if 'gate' in item and 'general-gate' not in item:
        gates[item] = 5
        fill[item] = '#333232'

dat = {}
dat['nodes'] = [] # init empty list for nodes
for key in gates.keys():
    infoDic = {'nodeName': key, 'group': gates[key]}  # get a dictionary to store node name and group
    dat['nodes'].append(infoDic)
# -------------------------------------------------

# links_df = links_df[links_df['count'] > 100] # only select those with more than 5 transactions
links_df = links_df[links_df['gate-name'] != links_df['next-gate']]

links_df.sort_values(['next-gate'], inplace=True)
# draw networkx diagram

G = nx.from_pandas_dataframe(links_df, source='gate-name', target='next-gate', edge_attr=['count'])
nx.set_node_attributes(G, 'group', gates) # set a node attribute for each node
nx.set_node_attributes(G, 'fill', fill) # set a fill color

"""
edges, weights = zip(*nx.get_edge_attributes(G, 'count').items())
carac = pd.DataFrame(dat['nodes']) # set group for each node

nx.draw_networkx(G, edge_color=weights, edge_cmap=plt.cm.hot, node_color = carac['group'], cmap=plt.cm.tab10, font_size=8, node_size = 100)
sns.set_style('white')
sns.despine()
plt.axis('off')
plt.legend()
fig = plt.gcf()
plt.savefig('car3-network.png')
plt.show()
"""

print("\n".join(nx.generate_gml(G)))
nx.write_gml(G, 'car2P.txt')

