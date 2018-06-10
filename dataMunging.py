import pandas as pd


data = pd.read_csv('Lekagul Sensor Data.csv')
data = data[data['car-type'] == '3'] # test out data only on car type 3
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
# -----------------------------------------------
# now initialise a dictionary to contain  nodes
gates = {}
fill = {}

for item in set(data['gate-name']):
    if 'gate' in item and 'general-gate' not in item:
        gates[item] = 1
        fill[item] = '#333232'

    elif 'general-gate' in item:
        gates[item] = 2
        fill[item] = '#F7B2AD'
    elif 'entrance' in item:
        gates[item] = 3
        fill[item] = '#CEB7B3'

    elif 'camping' in item:
        gates[item] = 4
        fill[item] = '#B7B7B7'

    elif 'ranger-stop' in item:
        gates[item] = 5
        fill[item] = '#9ABCA7'
dat = {}
dat['nodes'] = [] # init empty list for nodes
for key in gates.keys():
    infoDic = {'nodeName': key, 'group': gates[key]}  # get a dictionary to store node name and group
    dat['nodes'].append(infoDic)
# -------------------------------------------------

clearedData = data.dropna(axis=0) # remove those at the end of their journey
links_df = clearedData.groupby(['gate-name', 'next-gate']).size().reset_index().rename(columns={0: 'count'})

links_df['group_x'] = links_df['gate-name'].map(gates) # group of the first gate
links_df['group_y'] = links_df['next-gate'].map(gates) # group of the second gate

links_df = links_df[links_df['count'] > 5] # only select those with more than 5 transactions
links_df = links_df[links_df['gate-name'] != links_df['next-gate']]

from bokeh.charts import output_file, Chord
from bokeh.io import show
import bokeh

chord_from_df = Chord(links_df, source='gate-name', target='next-gate', value='count')
chord_from_df.plot_height = 1000
chord_from_df.plot_width = 1000
output_file('chord-diagram.html')
show(chord_from_df)

# okay so this kinda looks pretty crap
# plan 2: assign each gate name an index
gateIndex = {}
for i, j in enumerate(gates.keys()):
    gateIndex[j] = i

links_df['source'] = links_df['gate-name'].map(gateIndex)
links_df['target'] = links_df['next-gate'].map(gateIndex)

links_df.reset_index(inplace=True, drop=True)

dat['links'] = []
for i in range(links_df.shape[0]):
    link = {'source': links_df['source'][i], 'target': links_df['target'][i], 'value': links_df['count'][i]}
    dat['links'].append(link)

import json
nodes_json = json.dumps(dat['nodes'])
with open('nodes.json', 'w') as outfile:
    json.dump(nodes_json, outfile)

links_json = json.dumps(dat['links'])
with open('links.json', 'w') as outfile:
    json.dump(links_json, outfile)

# plan 3 - convert everything to a networkx file
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 5))
G = nx.from_pandas_dataframe(links_df, 'gate-name', 'next-gate', ['count']) # set number of flows as weight, and id of first gate
nx.set_node_attributes(G, 'group', gates) # set a node attribute for each node
nx.set_node_attributes(G, 'fill', fill) # set a fill color
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


# plan 4 now to work on the arc diagram
print("\n".join(nx.generate_gml(G)))
# save to gml
nx.write_gml(G, 'car3.txt')