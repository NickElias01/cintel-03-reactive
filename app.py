# Additional Python Notes
# ------------------------

# Capitalization matters in Python. Python is case-sensitive: min and Min are different.
# Spelling matters in Python. You must match the spelling of functions and variables exactly.
# Indentation matters in Python. Indentation is used to define code blocks and must be consistent.

# Functions
# ---------
# Functions are used to group code together and make it more readable and reusable.
# We define custom functions that can be called later in the code.
# Functions are blocks of logic that can take inputs, perform work, and return outputs.

# Defining Functions
# ------------------
# Define a function using the def keyword, followed by the function name, parentheses, and a colon. 
# The function name should describe what the function does.
# In the parentheses, specify the inputs needed as arguments the function takes.

# For example:
#    The function filtered_data() takes no arguments.
#    The function between(min, max) takes two arguments, a minimum and maximum value.
#    Arguments can be positional or keyword arguments, labeled with a parameter name.

# The function body is indented (consistently!) after the colon. 
# Use the return keyword to return a value from a function.

# Calling Functions
# -----------------
# Call a function by using its name followed by parentheses and any required arguments.
    
# Decorators
# ----------
# Use the @ symbol to decorate a function with a decorator.
# Decorators a concise way of calling a function on a function.
# We don't typically write decorators, but we often use them.


import plotly.express as px
import seaborn as sns
from shiny.express import input, ui, render
from shinywidgets import render_plotly, render_widget
from palmerpenguins import load_penguins

# Load the penguins dataset
penguins_df = load_penguins()

# Define UI with Shiny Express
ui.page_opts(title="Elias Analytics - Penguin Data", fillable=True)

# Sidebar for user interactions
with ui.sidebar(open="open", bg="#CCE7FF"):
    ui.h2("Options")

    # Dropdown for selecting penguin attributes
    ui.input_selectize(
        "selected_attribute",
        "Select Penguin Attribute:",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Numeric input for the number of Plotly histogram bins
    ui.input_numeric(
        "plotly_bin_count",
        "Number of Plotly Bins:",
        10,  # Default value
        min=1,
        max=100,
    )

    # Slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins:", min=5, max=50, value=20)

    # Checkbox group for filtering by species
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter by Species:",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    # Horizontal rule
    ui.hr()

    # Link to GitHub
    ui.a(
        "GitHub", href="https://github.com/NickElias01/cintel-02-data", target="_blank"
    )

# Main content area for the plots and data table
with ui.layout_columns():

    ui.h2("Palmer Penguins")

    # Data Table
    @render.data_frame  
    def penguins_datatable():
        return render.DataTable(penguins_df) 

    # Data Grid
    @render.data_frame  
    def penguins_datagrid():
        return render.DataGrid(penguins_df)

    # Plotly histogram
    @render_widget  
    def histogram_plot():  
        plotly_histogram = px.histogram(
            data_frame=penguins_df,
            x=input.selected_attribute(),
            nbins=input.plotly_bin_count(),
            color="species"
        ).update_layout(
            title={"text": "Penguin Attribute Histogram", "x": 0.5},
            yaxis_title="Count",
            xaxis_title=input.selected_attribute().replace("_", " ").title(),
        )
    
        return plotly_histogram

    # Plotly scatter plot
    @render_widget  
    def scatter_plot():  
        plotly_scatterplot = px.scatter(
            data_frame=penguins_df,
            x=input.selected_attribute(),
            y="body_mass_g",
            color="species"
        ).update_layout(
            title={"text": "Penguin Attribute vs Body Mass", "x": 0.5},
            yaxis_title="Body Mass (g)",
            xaxis_title=input.selected_attribute().replace("_", " ").title(),
        )
        return plotly_scatterplot

    # Seaborn Histogram
    @render.plot(alt="A Seaborn histogram showing distribution by species.")  
    def plot():  
     
        # Create the histogram
        ax = sns.histplot(
            data=penguins_df, 
            x=input.selected_attribute(), 
            bins=input.seaborn_bin_count(), 
            hue="species", 
            element="step",
            kde=True
        )
        
        # Set title and labels
        ax.set_title("Distribution of " + input.selected_attribute().replace("_", " ").title())
        ax.set_xlabel(input.selected_attribute().replace("_", " ").title())
        ax.set_ylabel("Count")
        return ax
