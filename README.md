# PDDS Final Project Dashboard
This is a Dash application developed for the PDDS final project.
The application provides an interactive dashboard to visualize e-commerce sales data, grouped by categories and countries, using an SQLite database as the data source.

# Project Overview
This project is an interactive dashboard built with Dash and Plotly.
The dashboard visualizes e-commerce sales data with options to filter and drill down into specific categories, countries, and minor categories. Users can explore data via interactive dropdowns, bar charts, line charts, and a data table.

# Setup Instructions
Clone the repository (or download the files directly)

Install dependencies: Make sure you have Python 3.10 (or aboved) installed.
Install the necessary Python packages:
```pip install -r requirements.txt```
Database setup: Ensure ecom_data.sqlite3 (or the appropriate SQLite database file) is present in the project directory. This database file contains the e-commerce sales data used by the application.

Run the application: Start the Dash server by running:
```python dash_test.py```
The application will be available at http://127.0.0.1:8050 in your web browser.

# Application Structure
## Layout Components
- **Logo**: Displays the company logo at the top of the page.
## Dropdowns:
- **Major Category Select**: Selects the major category for filtering.
- **Minor Category Select**: Populated based on the selected major category.
## Graphs:
- **Total Sales by Country**: A bar chart that shows total sales for each country.
- **Sales by Month for Minor Category**: A line chart that shows total sales over time for a selected minor category.
- **Sales Volume vs. Total Sales**: A scatter plot comparing sales volume and total sales by country.
## Data Table:
Displays summary statistics for each country, including sales volume, total sales, average order value, and median order value.

# Data Structure
The data is stored in an SQLite database (ecom_data.sqlite3). Key tables and columns include:

- **Country**: The country where the sales took place.
- **OrderValue**: The total value of orders.
- **Major Category and Minor Category**: Product categories to filter data.
- **Year-Month**: Used to group sales data by month.

# Callbacks and Interactions
The application includes several Dash callbacks for interactive data updates:

- **Filter Minor Category Dropdown**:
Based on the selected major category in the Major Category Select dropdown, updates the Minor Category Select dropdown.
- **Update Line Chart**:
Displays total sales over time for the selected minor category.
- **Scatter Plot**:
Updates based on the selected column in the data table (Total Sales, Average Order Value, or Median Order Value).
- **Update Minor Category Chart on Hover**:
When hovering over a country in the bar chart, updates the minor category bar chart for the hovered country.

# Deployment
Reference: https://dash.plotly.com/deployment
