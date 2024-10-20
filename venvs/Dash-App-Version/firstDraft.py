import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np


app = dash.Dash(__name__)

initial = True

app.layout = html.Div([

    #this is the title of the app and the subheading for the variable adjustment section on the left of the screen

    html.H1("Marx's Reproduction Schema", style={'textAlign': "center"}),

    html.H2("Adjust Variables", style={'textAlign': 'left'}),


        #this div below is the section where I add the sliders and the input boxes for each variable
    html.Div([
        html.Div([

                #slider and input box for rate of exploitation
            html.Div([
            html.Label(" Rate of exploitation e:"),
            dcc.Slider(id='slider-e', min=0, max=10, step=None, value=1, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Input(id='input-e', type='number', min=0, max=10, step=0.1, value=1, style={'marginLeft': '2px', 'width': '40px'})
            ],style={'alignItems': 'center'}),

            html.Br(),
            

            #slider and input box for composition of capital k1

            html.Div([
            html.Label("Composition of Capital for Department 1 k_1:"),
            dcc.Slider(id='slider-k1', min=0, max=10, step=None, value=1.5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
             dcc.Input(id='input-k1', type='number', min=0, max=10, step=0.1, value=1, style={'marginLeft': '2px', 'width': '40px'})
            ],style={'alignItems': 'center'}),

            html.Br(),


             #slider and input box for composition of capital k2

             html.Div([
            html.Label("Composition of Capital for Department 2 k_2:"),
            dcc.Slider(id='slider-k2', min=0, max=10, step=None, value=3.2, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
             dcc.Input(id='input-k2', type='number', min=0, max=10, step=0.1, value=1, style={'marginLeft': '2px', 'width': '40px'})
            ],style={'alignItems': 'center'}),

            html.Br(),


         #slider and input box for rate of reinvestment

             html.Div([
            html.Label("Rate of reinvestment a:"),
            dcc.Slider(id='slider-a', min=0, max=0.99, step=None, value=0.5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
             dcc.Input(id='input-a', type='number', min=0, max=0.99, step=0.1, value=0.5, style={'marginLeft': '2px', 'width': '40px'})
            ],style={'alignItems': 'center'}),


             #slider and input box for initial value output y1i

            html.Div([
            html.Label("Initial Value Output for Department 1 y_1i:"),
            dcc.Slider(id='slider-y1i', min=0, max=10, step=None, value=1, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Input(id='input-y1i', type='number', min=0, max=10, step=0.1, value=1, style={'marginLeft': '2px', 'width': '40px'}),
              html.Button(
                'Balanced Growth y1i', 
                id='balanced-growth-button-y2i',
                n_clicks=0,
                style={
                    'backgroundColor': '#28a745',  # Green background
                    'color': 'white',  # White text
                    'border': 'none',  # No border
                    'padding': '10px 20px',  # Padding
                    'textAlign': 'center',
                    'textDecoration': 'none', 
                    'display': 'inline-block',
                    'fontSize': '16px',  # Font size
                    'margin': '10px 0',  # Margin
                    'cursor': 'pointer',  # Pointer cursor on hover
                    'borderRadius': '5px',  # Rounded corners
                }
            )
             ]),


             #slider and input box for initial value output y2i

            html.Div([
            html.Label("Initial Value Output for Department 2 y_2i:"),
            dcc.Slider(id='slider-y2i', min=0, max=10, step=None, value=1, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Input(id='input-y2i', type='number', min=0, max=10, step=0.1, value=1, style={'marginLeft': '2px', 'width': '40px'}), 
             html.Button(
                'Balanced Growth y2i', 
                id='balanced-growth-button-y1i',
                n_clicks=0,
                style={
                    'backgroundColor': '#28a745',  # Green background
                    'color': 'white',  # White text
                    'border': 'none',  # No border
                    'padding': '10px 20px',  # Padding
                    'textAlign': 'center',
                    'textDecoration': 'none', 
                    'display': 'inline-block',
                    'fontSize': '16px',  # Font size
                    'margin': '10px 0',  # Margin
                    'cursor': 'pointer',  # Pointer cursor on hover
                    'borderRadius': '5px',  # Rounded corners
                }
            ), 
             ]),


                #this is the button to achieve balanced growth
                #the eventual function of this is to set k1 and k2 equal to one another
                #balanced growth, just like in the desmos app

                #this is the button to reset the viewport of the graph
            html.Button(
                'Reset View', 
                id='reset-view-button',
                n_clicks=0,
                style={
                    'backgroundColor': '#c61a09',  # Red background
                    'color': 'white',  # White text
                    'border': 'none',  # No border
                    'padding': '10px 20px',  # Padding
                    'textAlign': 'center', 
                    'textDecoration': 'none', 
                    'display': 'inline-block', 
                    'fontSize': '16px',  # Font size
                    'margin': '10px 0',  # Margin
                    'cursor': 'pointer',  # Pointer cursor on hover
                    'borderRadius': '5px',  # Rounded corners
                }
            ),

        ], style={'width': '30%', 'padding': '5px', 'display': 'flex', 'flexDirection': 'column'}),

      

    #Graph details, most importantly the bar at the top right
    #What is shown on the bar
    #How you can move around on the graph, what is the user able to do and what action does what
        html.Div(id='graph-container', children=[
            dcc.Graph(
                id='graph',
                style={'height': '80vh'},
                config={
                    'scrollZoom': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                   'modeBarButtonsToRemove': ['zoom2d','autoscale','resetscale2d','pan','zoomin2d','zoomout2d','toImage'],
                }
            ),
        ], style={'width': '70%'}),
    ], style={'display': 'flex'}),
])


# Define the callback to update the graph
#  When a value changes the callback will be activated to update what the graph looks like according to the new values
@app.callback(
    Output('graph', 'figure'),

    Output('balanced-growth-button-y1i', 'n_clicks'),
    Output('balanced-growth-button-y2i', 'n_clicks'),

    Output('slider-y1i', 'value'),
    Output('slider-y2i', 'value'),

    Output('slider-e', 'value'),
    Output('input-e', 'value'),

    Output('slider-k1', 'value'),
    Output('input-k1', 'value'),

    Output('slider-k2', 'value'),
    Output('input-k2', 'value'),

    Output('slider-a','value'),
    Output('input-a','value'),

    #below are the values used to get the initial graph by feeding them into the equations
    Input('slider-e','value'),
    Input('slider-k1', 'value'),
    Input('slider-k2', 'value'),
    Input('slider-a', 'value'),

    Input('slider-y1i', 'value'),
    Input('slider-y2i', 'value'),
    
    Input('balanced-growth-button-y1i', 'n_clicks'),
    Input('balanced-growth-button-y2i', 'n_clicks'),

    Input('slider-e','value'),
    Input('input-e','value'),
    
    Input('slider-k1', 'value'),
    Input('input-k1', 'value'),

    Input('slider-k2', 'value'),
    Input('input-k2', 'value'),

    Input('slider-a','value'),
    Input('input-a','value')
)


# Update graph function, basically copied off of the tkinter version
def update_graph(e, k_1, k_2, a, y_1i, y_2i, bg1clicks, bg2clicks, slider_e, input_e, slider_k1, input_k1, slider_k2, input_k2, slider_a, input_a):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]


    slidery1i = y_1i
    slidery2i = y_2i

    c_1 = k_1 / (1 + e + k_1)
    v_1 = (1 - c_1) / (1 + e)
    s_1 = e * v_1
    c_2 = k_2 / (1 + e + k_2)
    v_2 = (1 - c_2) / (1 + e)
    s_2 = e * v_2
    b = 1 - a
    golden_pi = 1 / ((0.5) * (c_1 + v_2 + ((c_1 - v_2) ** 2 + 4 * v_1 * c_2) ** 0.5)) - 1

    M_11 = c_1
    M_12 = c_2
    M_21 = (b * s_1 * c_1 + v_1) / (1 - b * s_2)
    M_22 = (b * s_1 * c_2 + v_2) / (1 - b * s_2)

    mu_1 = 0.5 * (M_11 + M_22 + np.sqrt((M_11 - M_22) ** 2 + 4 * M_12 * M_21))
    mu_2 = 0.5 * (M_11 + M_22 - np.sqrt((M_11 - M_22) ** 2 + 4 * M_12 * M_21))
    m_11 = 1
    m_12 = (mu_1 - M_11) / M_12 * m_11
    m_21 = 1
    m_22 = -(M_11 - mu_2) / M_12 * m_21
    bg1 = (m_12/m_11)*y_1i
    bg2 = (m_11/m_12)*y_2i

    if bg1clicks > 0:
        y_2i = bg1
        slidery2i = bg1
        bg1clicks = 0

    if bg2clicks > 0:
        y_1i = bg2
        slidery1i = bg2
        bg2clicks = 0


    P = np.array([[m_11, m_21], [m_12, m_22]])
    P_inverse = np.linalg.inv(P)
    y_vec = np.array([[y_1i], [y_2i]])
    eta_vec = np.matmul(P_inverse, y_vec)

    r_l = (m_22 * y_1i - m_21 * y_2i) / (m_11 * m_22 - m_12 * m_21)

    t_range = np.linspace(-3, 14, 1000)

    inpute = input_e if trigger_id == 'input-e' else slider_e
    slidere = slider_e if trigger_id == 'slider-e' else input_e

    inputk1 = input_k1 if trigger_id == 'input-k1' else slider_k1
    sliderk1 = slider_k1 if trigger_id == 'slider-k1' else input_k1

    inputk2 = input_k2 if trigger_id == 'input-k2' else slider_k2
    sliderk2 = slider_k2 if trigger_id == 'slider-k2' else input_k2

    inputa = input_a if trigger_id == 'input-a' else slider_a
    slidera = slider_a if trigger_id == 'slider-a' else input_a


    #sets the initial value for the sliders to be returned later in case the user doesn't click the growth path buttons at all


    #if the user clicks the balanced growth button, they would set both of these values equal to one another achieving the
    #desired balanced growth, clicks is then set back to 0 to make the change impermanent and the cycle can repeat

    #sets one value on to the other depending on which was clicked on the app below
    #different if clause is activated depending on k1 or k2 click

    exp_1 = (1 / mu_1) ** t_range
    if k_2 > k_1:
        exp_2 = (-1 / mu_2) ** t_range
        exp_2 = exp_2 * np.cos(np.pi * t_range)
    else:
        exp_2 = 1 / mu_2 ** t_range
    z_l1 = r_l * m_11 * exp_1
    z_l2 = r_l * m_12 * exp_1

    y_1 = (exp_1 * eta_vec[0] * m_11) + (exp_2 * eta_vec[1] * m_21)
    y_2 = (exp_1 * eta_vec[0] * m_12) + (exp_2 * eta_vec[1] * m_22)

    # Create traces
    trace_y1 = go.Scatter(x=t_range, y=y_1.flatten(), mode='lines', name='y_1', line=dict(color='blue'))
    trace_y2 = go.Scatter(x=t_range, y=y_2.flatten(), mode='lines', name='y_2', line=dict(color='red'))
    trace_zl1 = go.Scatter(x=t_range, y=z_l1.flatten(), mode='lines', name='z_l1', line=dict(color='blue', dash='dash'))
    trace_zl2 = go.Scatter(x=t_range, y=z_l2.flatten(), mode='lines', name='z_l2', line=dict(color='red', dash='dash'))

    # Define the figure layout
    layout = go.Layout(title=None,
                       xaxis=dict(),
                       yaxis=dict(title=None, range = [-4,20]),
                       showlegend=True, dragmode='pan')
    
    #Defining the lines that eventually show up on the graph based on the traces defined using the equations above

    fig = go.Figure(data=[trace_y1, trace_y2, trace_zl1, trace_zl2], layout=layout)
    

    #this is for the y=0 aka the x axis line 
    fig.update_yaxes(
    showline=False,
    linewidth=2,
    linecolor='black',
    zeroline=True,       # Show the zero line
    zerolinewidth=2,
    zerolinecolor='black'
)
    #resets the view to a reasonable range of view, default
    return fig, bg1clicks, bg2clicks, slidery1i, slidery2i, slidere, inpute, sliderk1, inputk1, sliderk2, inputk2, slidera, inputa


if __name__ == '__main__':
    app.run_server(debug=True)


#the main problems that I am experiencing 
# 1. when I don't touch the sliders for k_1 k_2 they change based on the values of initial output of each department
# 2. Extending the graph infinitely and keeping it scaled
# 3. When the user exits the input box there is a division by zero error a lot of the time
# 4. How do I split my code into separate files?
# 5. What other stuff should I add to make it more complete?