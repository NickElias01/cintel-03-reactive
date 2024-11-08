import plotly.express as px
import seaborn as sns
from shiny.express import input, ui, render
from shinywidgets import render_plotly, render_widget
from palmerpenguins import load_penguins
from shiny import reactive

# Load the penguins dataset
penguins_df = load_penguins()

# Dictionary for formatting attribute names
attribute_labels = {
    "bill_length_mm": "Bill Length (mm)",
    "bill_depth_mm": "Bill Depth (mm)",
    "flipper_length_mm": "Flipper Length (mm)",
    "body_mass_g": "Body Mass (g)"
}

# Reverse dictionary for mapping formatted labels back to raw attribute names
attribute_reverse_map = {v: k for k, v in attribute_labels.items()}

# Define UI options with Shiny Express and set the main container as scrollable
ui.page_opts(
    title="Elias Analytics - Penguin Data",
    fillable=True,
    style="max-height: 90vh; overflow-y: scroll; padding: 10px;",
    fullwidth=True
)

# Sidebar for user interactions and selections
with ui.sidebar(open="open", bg="#CCE7FF"):
    ui.h2("Options")

    # Dropdown for selecting penguin attributes for analysis
    ui.input_selectize(
        "selected_attribute",
        "Select Penguin Attribute:",
        list(attribute_labels.values()),  # Use the formatted labels
    )

    # Numeric input for controlling the number of bins in the Plotly histogram
    ui.input_numeric(
        "plotly_bin_count",
        "Plotly Histogram Bins:",
        10,  # Default value
        min=1,
        max=100,
    )

    # Slider for setting the number of bins in the Seaborn histogram
    ui.input_slider("seaborn_bin_count", "Seaborn Histogram Bins:", min=5, max=50, value=20)

    # Checkbox group for filtering the dataset by penguin species
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter by Species:",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    # Checkbox group for filtering the dataset by penguin island
    ui.input_checkbox_group(
        "selected_island_list",
        "Filter by Island:",
        ["Biscoe", "Dream", "Torgersen"],  # List of islands in the dataset
        selected=["Biscoe", "Dream", "Torgersen"],  # Default selected islands
        inline=False,  # Set inline to False to stack the checkboxes vertically
    )

    # Horizontal rule for visual separation
    ui.hr()

     # Link to GitHub repository for additional resources
    ui.a(
         "Link to GitHub", href="https://github.com/NickElias01/cintel-03-reactive", target="_blank"
        )

# Main content area: Each visual component is wrapped in a card for better layout on smaller screens
with ui.layout_columns(fill=True):

    # Data Table Card
    with ui.card(full_screen=True):
        ui.h3("Penguin Data Table")
        # Render a data table displaying filtered penguin data
        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data())

    # Data Grid Card
    with ui.card(full_screen=True):
        ui.h3("Penguin Data Grid")
        # Render a data grid displaying the same filtered penguin data
        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data())

ui.hr()

with ui.layout_columns(fill=True):
    # Plotly Histogram Card
    with ui.card(full_screen=True):
        ui.h3("Plotly Histogram")
        # Render a histogram of the selected attribute using Plotly
        @render_widget
        def histogram_plot():  
            plotly_histogram = px.histogram(
                data_frame=filtered_data(),
                x=attribute_reverse_map[input.selected_attribute()],  # Map to raw attribute name
                nbins=input.plotly_bin_count(),
                color="species"
            ).update_layout(
                title={"text": f"{input.selected_attribute()} Distribution", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.selected_attribute(),
            )
            return plotly_histogram

    # Plotly Scatter Plot Card
    with ui.card(full_screen=True):
        ui.h3("Plotly Scatter Plot")
        # Render a scatter plot comparing the selected attribute to body mass using Plotly
        @render_widget
        def scatter_plot():  
            plotly_scatterplot = px.scatter(
                data_frame=filtered_data(),
                x=attribute_reverse_map[input.selected_attribute()],  # Map to raw attribute name
                y="body_mass_g",
                color="species"
            ).update_layout(
                title={"text": f"{input.selected_attribute()} vs Body Mass(g)"},
                yaxis_title="Body Mass (g)",
                xaxis_title=input.selected_attribute(),
            )
            return plotly_scatterplot

    # Seaborn Histogram Card
    with ui.card(full_screen=True):
        ui.h3("Seaborn Histogram")
        # Render a histogram of the selected attribute using Seaborn
        @render.plot(alt="Seaborn histogram of the selected penguin attribute by species, with KDE overlay.")
        def plot():  
            # Create the histogram with Seaborn
            ax = sns.histplot(
                data=filtered_data(), 
                x=attribute_reverse_map[input.selected_attribute()],  # Map to raw attribute name
                bins=input.seaborn_bin_count(), 
                hue="species", 
                element="step",
                kde=True
            )
            
            # Set the title and labels for the histogram
            ax.set_title(f"Distribution of {input.selected_attribute()} by Species")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Count")
            return ax

# --------------------------------------------------------
# Reactive calculations for dynamic filtering based on user selections
# --------------------------------------------------------

# Define a reactive calculation for data filtering
@reactive.calc
def filtered_data():
    """Filter penguins dataset based on selected species and island."""
    # Filter based on selected species list
    filtered_df = penguins_df[penguins_df["species"].isin(input.selected_species_list())]
    
    # Filter based on selected island list
    filtered_df = filtered_df[filtered_df["island"].isin(input.selected_island_list())]
    
    return filtered_df
