import numpy as np
import plotly.graph_objects as go
from skimage.color import hsv2rgb

from sklearn.cluster import KMeans

from dataLoader import DataLoader

class ViewVisualizer():

    def __init__(self, filename):
        self.dataLoader = DataLoader(filename)
        self.clusteredLabels = []

    def create_stylesheet(self, hour, num_of_groups):
        stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(id)'
                }
            }
        ]
        
        stylesheet += self.color_nodes(hour, stylesheet)
        stylesheet += self.direct_edges(stylesheet, num_of_groups)

        return stylesheet

    def load_nodes(self, hour):
        elements = []
        for node in self.dataLoader.get_data(hour, 'nodes'):
            elements.append({'data': {'id' : str(int(node[0])), 'label' : str(int(node[0])) }})

        for branch in self.dataLoader.get_data(hour, 'branches'):
            a, b = str(int(branch[0])), str(int(branch[1]))
            elements.append({'data': {'id': f'{a}_{b}', 'source' : a, 'target' : b }})
        return elements

    def color_nodes(self,hour, stylesheet):
        """
            color red - only use power
            color green - generate power
            color red - use more power than generate
            
            Not every node generate power. Only those which node_type are greater than 1 do it. Size of nodes which can
            generate is modified by a generated power factor  
        """
        nodes = self.dataLoader.get_data(hour, "nodes")
        gens = self.dataLoader.get_data(hour, "gens")

        for node in nodes:
            if node[1] == 1:
                stylesheet.append(
                    {
                        'selector': f'#{int(node[0])}',
                        'style': {
                            'background-color': 'black',
                            
                        }
                    },
                )
            else:
                for gen in gens:
                    if node[0] == gen[0] and gen[1] - node[2] > 0:
                        stylesheet.append(
                            {
                            'selector': f'#{int(node[0])}',
                            'style': {
                                'background-color': 'green',
                                'width': f"{5*gen[1]}%",
                                'height': f"{5*gen[1]}%"
                            }
                        },
                    )
                    elif node[0] == gen[0]:                       
                        stylesheet.append(
                            {
                            'selector': f'#{int(node[0])}',
                            'style': {
                                'background-color': '#ecb500',
                                'width': f"{5*gen[1]}%",
                                'height': f"{5*gen[1]}%"
                            }
                        },
                    )

        return stylesheet

    def direct_edges(self, stylesheet, num_of_groups):
        colors = self.get_random_set_of_colors(num_of_groups)
        for id1,id2,flow,label in self.clusteredLabels:
            color = self.rgb_to_hex(colors[label][0],colors[label][1],colors[label][2])
            if flow > 0:
                stylesheet.append(                       
                    {
                        'selector': f'#{int(id1)}_{int(id2)}',
                        'style': {
                            'mid-target-arrow-shape': 'vee',
                            'mid-target-arrow-color': f'#{color}',
                            'arrow-scale': 3,
                            'line-color': f'#{color}'
                        }
                    }
                )
            elif flow < 0:   
                stylesheet.append(                     
                    {
                        'selector': f'#{int(id1)}_{int(id2)}',
                        'style': {
                            'mid-source-arrow-shape': 'vee',
                            'mid-source-arrow-color': f'#{color}',
                            'arrow-scale': 3,
                            'line-color': f'#{color}'
                        }
                    }
                )
        return stylesheet

    def group_edges(self,hour, num_groups):
        """
            KMeans algorithm was used because it execute 0.05-0.02 seconds for this dataset
        """
        num_groups = int(num_groups)

        branches = self.dataLoader.get_data(hour, "branches")
        flow = branches[:,2].reshape(-1,1)
        clustering = KMeans(n_clusters=num_groups).fit(flow)

        self.clusteredLabels = []       # save clustered edges to color them later
        for idx, branch in enumerate(branches):
            self.clusteredLabels.append([int(branch[0]), int(branch[1]), branch[2], clustering.labels_[idx]])

        res = ''
        for group in range(num_groups):
            res += f'Grupa: {group} o punkcie centralnym: {np.round(clustering.cluster_centers_[group][0],2)} \n'
            for idx, label in enumerate(clustering.labels_):
                if label == group:
                    res += f"Linia '{int(branches[idx][0])}-{int(branches[idx][1])}' {np.round(branches[idx][2],2)}MW, "
            res = res[:-2]
            res += '\n\n'

        return res

    def rgb_to_hex(self, r, g, b):
        return ('{:02X}{:02X}{:02X}').format(r, g, b)

    def get_random_set_of_colors(self, n):
        '''Returns a list of distinct RGB color'''
        h = np.arange(1,n+1).reshape(n,1)/(n+1) # [1,2,...,n]/(n+1)
        s = np.random.uniform(low=0.5, high=1, size=(n,1))
        v = np.random.uniform(low=0.8, high=1, size=(n,1))
        hsv_colors = np.transpose([h, s, v], (1, 2, 0))
        rgb_colors = hsv2rgb(hsv_colors)
        rgb_colors = (255*(rgb_colors - np.min(rgb_colors))/np.ptp(rgb_colors)).astype(int)  
        return rgb_colors[:,0,:]
    
    def highlight_histogram(self, hour, node):
        nodes = self.dataLoader.get_data(hour, 'nodes')
        demand = nodes[:,2]

        bins = np.histogram_bin_edges(demand)
        counts, bins = np.histogram(demand, bins=bins)
        colors = ['blue',] * len(bins)

        if node:
            clicked_node = int(node['id'])-1
            for idx, value in enumerate(bins):
                if nodes[clicked_node][2] <= value:
                    if  idx == 0:
                        colors[idx] = 'yellow'
                    else:
                        colors[idx-1] = 'yellow'
                    break
        
        fig = go.Figure(data=[go.Bar(
            x=bins, y=counts,
            marker_color=colors)])
        return fig
