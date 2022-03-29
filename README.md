# energy_network_visualization

Visualization task of energy network flow. Data are stored in energyNetwork_24h.hdf5 file. There are 24 folders for each hour in day.

Solution was based on MVC design pattern. 

Each class contains:
- DataLoader - functions to load data
- Server is a GUI - functions to control visualization
- ViewVisualization - functions to wrap data for visualization in GUI


###  Data structure:
- results/hour_1/
     - nodes       -> node_id, node_type, demand [MW]
     - gens         -> node_id, generation [MW], cost [zł]
     - branches  -> node_from, node_to, flow [MW]
- results/hour_2/
- ...
- results/hour_24/

### Implemented functionality
- Differences in the flows on the edges 
     - Draw arrows on edges which show direction of flow
- Differences in the operation of nodes (the node gets power from others, the node generates power for others) 
     - Black node (gets power from others
     - Green node (generates power)
     - Yellow node (consume more power than is generating)
- Clustering edges by value of flow
     - Edges are colored with the same color if are in the same group
     - TextArea displays created groups
- distinguishing the amount of generated power 
     - Size of the node show how much power it generates. The bigger the more 
- Histogram of consumed power
     - Display histogram with consumed power of each node
     - Clicking a node will change a color of column on a histogram showing where the node is 

### Example of a graph


<img src="https://github.com/Falien164/energy_network_visualization/blob/main/images/graph.png" width="400" height="400">


### how to run:
> python run_server.py --filename
for instance:
> python .\run_server.py --filename=energyNetwork_24h.hdf5
