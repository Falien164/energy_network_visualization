# energy_network_visualization

It's visualization task of energy network flow. Data are stored in task_data.hdf5 file. There are 24 folders for each hour in day.

Solution was based on MVC design pattern. 

Each class contains:
- DataLoader - functions to load data
- Server is a GUI - functions to control visualization
- ViewVisualization - functions to wrap data for GUI


### Data structure:
> results/hour_1/
> 
> results/hour_2/
> 
> ...
> 
> results/hour_24/

dataset   ->  columns[unit]

results/hour_1/nodes       -> node_id, node_type, demand [MW]

results/hour_1/gens         -> node_id, generation [MW], cost [zł]

results/hour_1/branches  -> node_from, node_to, flow [MW]



### how to run:
> python server.py

### GUI
<img src="https://github.com/Falien164/energy_network_visualization/blob/main/images/graph.png" width="400" height="400">
