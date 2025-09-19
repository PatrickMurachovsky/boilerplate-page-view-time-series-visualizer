# Importing required libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()  # Allows plotting with time-based pandas indexes

# Compatibility fix for deprecated np.float in newer NumPy versions
if not hasattr(np, 'float'):
    np.float = float

# Load CSV file and parse dates in 'date' column, setting it as the index
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    parse_dates=['date'],
    index_col='date'
)

# Remove outliers outside the 2.5th and 97.5th percentiles
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)
df = df[(df['value'] >= lower) & (df['value'] <= upper)]


# Function to draw the line plot
def draw_line_plot():
    # Create a line plot of daily page views
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    return fig


# Function to draw the bar plot
def draw_bar_plot():
    # Copy and prepare the data
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Full month name

    # Define month order to ensure proper sorting in the plot
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Group data by year and month, calculate the average page views
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

    # Pivot the table to have months as columns and years as rows
    df_pivot = df_grouped.pivot(index='year', columns='month', values='value')

    # Plot the bar chart
    ax = df_pivot.plot(kind='bar', figsize=(12, 10))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Adjust layout and return the figure
    fig = ax.get_figure()
    fig.tight_layout()

    fig.savefig('bar_plot.png')
    return fig


# Function to draw the box plots
def draw_box_plot():
    # Copy and prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]  # Abbreviated month name

    sns.set_style('whitegrid')  # Set seaborn plot style
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    # Year-wise box plot (to show trend over years)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise box plot (to show seasonality across months)
    month_order_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order_abbr, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()  # Adjust layout for better spacing

    fig.savefig('box_plot.png')
    return fig