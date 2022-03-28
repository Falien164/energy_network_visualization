import numpy as np
from sklearn.cluster import KMeans

from dataLoader import DataLoader

class ViewVisualizer():

    def __init__(self):
        self.dataLoader = DataLoader("task_data.hdf5")

    def create_stylesheet(self, hour):
        stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(id)'
                }
            }
        ]
        
        stylesheet += self.color_nodes(hour, stylesheet)
        stylesheet += self.draw_arrows_on_edges(hour, stylesheet)

        return stylesheet

    def load_nodes(self, hour):
        elements = []
        for node in self.dataLoader.get_data(hour, 'nodes'):
            elements.append({'data': {'id' : str(int(node[0])), 'label' : str(int(node[0])) }})

        for branch in self.dataLoader.get_data(hour, 'branches'):
            a = str(int(branch[0]))
            b = str(int(branch[1]))
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
                            'background-color': 'red',
                            
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
                                'background-color': 'yellow',
                                'width': f"{5*gen[1]}%",
                                'height': f"{5*gen[1]}%"
                            }
                            },
                        )
                        
        return stylesheet

    def draw_arrows_on_edges(self, hour, stylesheet):
        branches = self.dataLoader.get_data(hour, "branches")
        for branch in branches:
            if branch[2] > 0:
                stylesheet.append(                       
                    {
                        'selector': f'#{int(branch[0])}_{int(branch[1])}',
                        'style': {
                            'mid-target-arrow-color': 'red',
                            'mid-target-arrow-shape': 'vee',
                            'arrow-scale': 3,
                            'line-color': 'blue'
                        }
                    }
                )
            elif branch[2] < 0:   
                stylesheet.append(                     
                    {
                        'selector': f'#{int(branch[0])}_{int(branch[1])}',
                        'style': {
                            'mid-source-arrow-color': 'red',
                            'mid-source-arrow-shape': 'vee',
                            'arrow-scale': 3,
                            'line-color': 'blue'
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
        flow = np.array([branch[2] for branch in branches]).reshape(-1,1)
        clustering = KMeans(n_clusters=num_groups).fit(flow)

        res = ''
        for group in range(0,num_groups):
            res += f'Grupa: {group} o punkcie centralnym: {np.round(clustering.cluster_centers_[group][0],2)} \n'
            for idx, label in enumerate(clustering.labels_):
                if label == group:
                    res += f"Linia '{int(branches[idx][0])}-{int(branches[idx][1])}' {np.round(branches[idx][2],2)}MW, "
            res = res[:-2]
            res += '\n\n'
        return res