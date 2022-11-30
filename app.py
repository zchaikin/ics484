from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as pl
from plotly.subplots import make_subplots
import pandas as pd

app = Dash(__name__)

### header END

### DATASET import and prep START
### DATASET import and prep END

### FIGURE Vendor Market Share START
### FIGURE Vendor Market Share END

### FIGURE nvidia line chart START
### FIGURE nvidia line chart END

### FIGURE amd line chart START
### FIGURE amd line chart END

### FIGURE intel line chart START
### FIGURE intel line chart END

### WEBSITE header, nav and footer START
### WEBSITE header, nav and footer END

### WEBSITE Tab Switching Navigation Callback Logic START
### WEBSITE Tab Switching Navigation Callback Logic END

### DASH footer START

if __name__ == '__main__':
    app.run_server(debug=True)