import dash
import dash_cytoscape as cyto

from viewVisualizer import ViewVisualizer

class Gui:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.viewVisualizer = ViewVisualizer()

        self.app.layout = self.build_layout()

        self.app.callback(dash.dependencies.Output('cytoscape', 'elements'),
            dash.dependencies.Output('cytoscape', 'stylesheet'),
            dash.dependencies.Input('hour-dropdown', 'value'))(self.changed_hour)

        self.app.callback(dash.dependencies.Output('text-cluster-output', 'value'),
        dash.dependencies.Input('hour-dropdown', 'value'),
        dash.dependencies.Input('cluster-input', 'value'))(self.changed_num_of_groups)
    
    def build_layout(self):
        hours = self.viewVisualizer.dataLoader.load_hours_from_h5()

        layout = dash.html.Div(
            children=[
                dash.html.Div([
                    dash.dcc.Dropdown( id='hour-dropdown', 
                        options= hours,
                        value = hours[0],
                    )],
                style={'width': '50%'}
                ),

                dash.html.Div([
                    "Number of clusters: ",
                    dash.dcc.Slider(1,10,
                        step=1, value=2,id='cluster-input'
                    )],
                    style={'width': '50%'}
                ),
                
                cyto.Cytoscape(
                    id = 'cytoscape',
                    layout = {'name': 'breadthfirst'},
                    userZoomingEnabled  = False,
                    style = {'width': '800px', 'height': '800px'},                    
                ),
                
                dash.dcc.Textarea(
                    id='text-cluster-output',
                    value='',
                    readOnly=True,
                    style={'width': '100%', 'height': 300},
                ),
            ]
        )
        return layout

    def changed_hour(self,hour):
        self.viewVisualizer.group_edges(hour, 2)
        return (self.viewVisualizer.load_nodes(hour),
                self.viewVisualizer.create_stylesheet(hour)
        )
    def changed_num_of_groups(self,hour, num_of_groups):
        return self.viewVisualizer.group_edges(hour, num_of_groups)

if __name__ == '__main__':
    gui = Gui()
    gui.app.run_server(debug=True)