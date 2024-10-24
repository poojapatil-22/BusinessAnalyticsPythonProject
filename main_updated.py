import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("dataset.csv", header=0)  # Replace "dataset.csv" with your actual dataset file path

# Initialize the Dash app
app = dash.Dash(__name__)

# Define custom CSS styles with the updated color scheme
custom_styles = {
    'background': {
        'background-color': '#e6e6fa',  # Light pink background
        'padding': '20px',  # Add padding for content
        'font-family': 'Arial, sans-serif'  # Change font family for a professional look
    },
    'header': {
        'text-align': 'center',
        'color': '#333',  # Dark gray for text
        'margin-bottom': '20px',
        'font-size': '36px',  # Increase font size for heading
        'font-weight': 'bold',  # Make heading bold
        'text-shadow': '2px 2px 2px #cccccc'  # Add shadow effect
    },
    'filters-container': {
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'margin-bottom': '20px'
    },
    'label': {
        'font-weight': 'bold',
        'margin-right': '10px',
        'color': '#666'  # Dark gray for text
    },
    'input': {
        'padding': '8px',  # Increase padding for input fields
        'border-radius': '5px',
        'border': '1px solid #ccc',
        'margin-right': '10px',
        'font-size': '14px'  # Adjust font size for inputs
    },
    'dropdown': {
        'padding': '8px',  # Increase padding for dropdowns
        'border-radius': '5px',
        'border': '1px solid #ccc',
        'margin-right': '10px',
        'width': '200px',  # Adjust width of dropdown menu
        'font-size': '14px'  # Adjust font size of dropdown options
    },
    'graph-container': {
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '0 0 10px rgba(0, 0, 0, 0.1)',
        'margin-bottom': '20px',
        'background-color': 'white'  # White background for graphs
    },
    'wordcloud-container': {
        'text-align': 'center'
    }
}

# Define dropdown options for visualization
dropdown_options = [
    {'label': 'Gender Distribution', 'value': 'gender-dist'},
    {'label': 'Industry Distribution', 'value': 'industry-dist'},
    {'label': 'Company Distribution', 'value': 'company-dist'},
    {'label': 'Skills Word Cloud', 'value': 'skills-wordcloud'},
    # Add more options as needed
]

# Get unique values for Division/Department column
division_department_options = [{'label': department.upper(), 'value': department} for department in df['Division/Department'].dropna().unique()]
location_options = [{'label': location.upper(), 'value': location} for location in df['Current Location'].dropna().unique()]

# Define app layout
app.layout = html.Div(style=custom_styles['background'], children=[
    html.H1("Parameterized Visualization Dashboard", style=custom_styles['header']),
    
    html.Div([
        html.Div([
            html.Label('Select Visualization:', style=custom_styles['label']),
            dcc.Dropdown(
                id='dropdown',
                options=dropdown_options,
                value='gender-dist',  # Default value
                style=custom_styles['dropdown']
            ),
        ], style={'margin-right': '20px'}),
        
        html.Div([
            html.Label('Year of Graduation Range:', style=custom_styles['label']),  # Updated label
            dcc.Input(
                id='year-graduation-min',
                type='number',
                value=df['Year of Graduation'].min(),
                placeholder='Min Year',
                style=custom_styles['input']
            ),
            dcc.Input(
                id='year-graduation-max',
                type='number',
                value=df['Year of Graduation'].max(),
                placeholder='Max Year',
                style=custom_styles['input']
            ),
        ], style={'margin-right': '20px'}),
        
        html.Div([
            html.Label('Select Division/Department:', style=custom_styles['label']),
            dcc.Dropdown(
                id='division-department-dropdown',
                options=division_department_options,
                value=[department['value'] for department in division_department_options],  # Default: All selected
                multi=True,
                style=custom_styles['dropdown']
            ),
        ], style={'margin-right': '20px'}),
        
        html.Div([
            html.Label('Select Location:', style=custom_styles['label']),
            dcc.Dropdown(
                id='location-dropdown',
                options=location_options,
                value=[location['value'] for location in location_options],  # Default: All selected
                multi=True,
                style=custom_styles['dropdown']
            ),
        ], style={'margin-right': '20px'})
    ], style=custom_styles['filters-container']),
    
    html.Div(id='graph-container', style=custom_styles['graph-container']),
    html.Div(id='skills-wordcloud-container', style=custom_styles['wordcloud-container'])
])

# Define callback to update visualization based on dropdown selection, year of graduation range, and selected divisions/departments
@app.callback(
    [Output('graph-container', 'children'),
     Output('skills-wordcloud-container', 'children')],
    [Input('dropdown', 'value'),
     Input('year-graduation-min', 'value'),
     Input('year-graduation-max', 'value'),
     Input('division-department-dropdown', 'value'),
     Input('location-dropdown', 'value')]
)
def update_graph(selected_option, min_year, max_year, selected_departments, selected_locations):
    filtered_df = df[(df['Year of Graduation'] >= min_year) & (df['Year of Graduation'] <= max_year)]
    
    if selected_departments:
        filtered_df = filtered_df[filtered_df['Division/Department'].isin(selected_departments)]
    
    if selected_locations:
        filtered_df = filtered_df[filtered_df['Current Location'].isin(selected_locations)]

    if selected_option == 'gender-dist':
        graph_output = dcc.Graph(
            id='gender-dist',
            figure=px.pie(filtered_df, names='Gender', title='Gender Distribution')
        )
        return graph_output, None
    elif selected_option == 'industry-dist':
        graph_output = dcc.Graph(
            id='industry-dist',
            figure=px.bar(filtered_df['Work Industry'].value_counts(), title='Industry Distribution', labels={'index': 'Industry', 'value': 'Count'})
        )
        return graph_output, None
    elif selected_option == 'company-dist':
        graph_output = dcc.Graph(
            id='company-dist',
            figure=px.bar(filtered_df['Current Designation'].value_counts(), title='Current Designation Distribution')
        )
        return graph_output, None
    elif selected_option == 'skills-wordcloud':
        skills_text = ' '.join(filtered_df['Skills'].dropna())
        # Generate word cloud here
        # For now, return a placeholder text
        return None, html.Div("Word cloud placeholder")
    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
