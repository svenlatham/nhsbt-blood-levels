import pandas as pd
import plotly.express as px
from jinja2 import Template, Environment, FileSystemLoader
from datetime import datetime
import pytz



# Set up Jinja2 environment to load templates from the 'templates' folder
env = Environment(loader=FileSystemLoader('templates'))

# Get the current date for the footer
london_tz = pytz.timezone("Europe/London")
current_date = datetime.now(london_tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')

def generate_file(item, label):
    # Blood
    input_src = "%s.csv" % (item)
    print("Loading from %s" % (input_src))
    df = pd.read_csv("%s.csv" % (item))
    most_recent_data = df.iloc[-1]
    last_updated = most_recent_data['date']
    most_recent_data = most_recent_data.drop('date')
    df_melted = df.melt(id_vars=['date'], var_name='Blood Group', value_name='Stock Level')
    fig = px.line(df_melted, x='date', y='Stock Level', color='Blood Group',
                title='%s Over Time' % (label), labels={'Stock Level': label})
    fig.write_html('docs/%s_stock_chart.html' % (item), include_plotlyjs='cdn')
    template = env.get_template('%s.html' % (item))
    html_content = template.render({'generated': current_date, 'date_most_recent': last_updated, 'most_recent_data': most_recent_data.to_dict()})
    with open('docs/%s.html' % (item), 'w') as f:
        f.write(html_content)

generate_file('blood','Blood Stock Levels')
generate_file('platelets','Platelets Stock Levels')


# Update the index last:
template = env.get_template('index.html')
html_content = template.render({'generated': current_date})
with open('docs/index.html', 'w') as f:
    f.write(html_content)