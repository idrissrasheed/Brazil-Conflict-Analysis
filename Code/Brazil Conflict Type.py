#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import pandas as pd
import folium as flm
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import seaborn as sns


# In[2]:


# import data
## brazil conflict data
conflicts = pd.read_csv('Brazil Political Violence and Protests Dataset.csv')


# In[3]:


conflicts.head()


# In[4]:


conflicts.info()


# In[5]:


conflicts.describe()


# In[6]:


#rename the EVENT_TYPE column to Conflict and SUB_EVENT_TYPE column to Subconflict.
conflicts = conflicts.rename(columns={'EVENT_TYPE': 'CONFLICT', 'SUB_EVENT_TYPE': 'SUBCONFLICT'})


# In[7]:


# types of subconflicts
conflict_type = conflicts['CONFLICT'].unique()
conflict_type


# In[8]:


# types of subconflicts
subconflict_type = conflicts['SUBCONFLICT'].unique()
subconflict_type


# In[9]:


# get value counts of event types
conflict_counts = conflicts['CONFLICT'].value_counts()

# create pie chart
plt.pie(conflict_counts, labels=conflict_counts.index, autopct='%1.1f%%')
plt.title('Conflict Types')

# display the plot
plt.show()
conflict_counts


# In[10]:


# total fatalities in total
fat_count = conflicts['FATALITIES'].sum()
print(fat_count, 'fatalities')


# In[11]:


# extract year from event date column
conflicts['YEAR'] = pd.to_datetime(conflicts['EVENT_DATE']).dt.year

# group by year and total fatalities
fat_by_year = conflicts.groupby('YEAR')['FATALITIES'].sum()

# create datetime objects for x-axis
x = [mdates.datetime.datetime(year, 1, 1) for year in fat_by_year.index]

# plot line chart
fig, ax = plt.subplots()
ax.plot_date(x, fat_by_year.values, linestyle='--')

# format x-axis as years
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# label axes and title
plt.xlabel('Year')
plt.ylabel('Fatalities')
plt.title('Number of Fatalities by Year')

# add the number of fatalities to each plot point
for i, j in enumerate(fat_by_year.values):
    ax.text(x[i], j, str(j), ha='left', va='bottom', weight='bold')

plt.show()


# In[12]:


# fatalities by conflict event type
fat_by_event_type = conflicts.groupby('CONFLICT')['FATALITIES'].sum().reset_index()

# total sum of fatalities
fat_count = fat_by_event_type['FATALITIES'].sum()

# add a new column for percentage of fatalities for each event type
fat_by_event_type['FATALITY_PERCENTAGE'] = round(fat_by_event_type['FATALITIES'] / fat_count * 100,2).astype(str) + '%'
fat_by_event_type


# In[13]:


# plot bar chart
plt.bar(fat_by_event_type['CONFLICT'], fat_by_event_type['FATALITIES'])

# format rotation on x-axis
plt.xticks(rotation=90)

# label axes and title
plt.xlabel('Event Type')
plt.ylabel('Fatalities')
plt.title('Number of Fatalities by Conflict')

# add the number of fatalities to each bar
for i, j in enumerate(fat_by_event_type['FATALITIES']):
    plt.text(i, j, str(j), ha='center', va='bottom')
    
# display the plot
plt.show()


# In[14]:


# fatalities by conflict event type
fat_by_subevent_type = conflicts.groupby('SUBCONFLICT')['FATALITIES'].sum().reset_index()

# total sum of fatalities
fat_count_sub = fat_by_subevent_type['FATALITIES'].sum()

# add a new column for percentage of fatalities for each event type
fat_by_subevent_type['FATALITY_PERCENTAGE'] = round(fat_by_subevent_type['FATALITIES'] / fat_count_sub * 100,2).astype(str) + '%'
fat_by_subevent_type


# In[15]:


# plot bar chart
plt.bar(fat_by_subevent_type['SUBCONFLICT'], fat_by_subevent_type['FATALITIES'])

# format rotation on x-axis
plt.xticks(rotation=90)

# label axes and title
plt.xlabel('Subevent Type')
plt.ylabel('Fatalities')
plt.title('Number of Fatalities by Subconflict Type')

# Add the number of fatalities to each bar
for i, j in enumerate(fat_by_subevent_type['FATALITIES']):
    plt.text(i, j, str(j), ha='center', va='bottom')
    
# Display the plot
plt.show()


# In[ ]:


corr = conflicts['ACTOR1'].corr(conflicts['FATALITIES'])
import numpy as np
from scipy.stats import pointbiserialr
# print the correlation coefficient

# convert actor column to numeric
conflicts['ACTOR1'] = pd.factorize(df['ACTOR1'])[0]
conflicts['ACTOR2'] = pd.factorize(df['ACTOR2'])[0]
# calculate point biserial correlation between actor_num and fatalities
corr, p_value = pointbiserialr(df['ACTOR1'], df['FATALITIES'])
print('Point Biserial Correlation:', corr)
print('p-value:', p_value)


# In[25]:


# top 10 cities with the most fatalities
top_ten_fat = conflicts.groupby('LOCATION')['FATALITIES'].sum().nlargest(10)
top_ten_fat_df = pd.DataFrame(top_ten_conflicts)


# In[17]:


# Create a map centered on Brazil
map = flm.Map(location=[-10.788497,-42.879873], zoom_start=4.2)

# create a marker for each city in the top 10
for city, fatalities in top_ten_fat.items():
    # get latitude and longitude for city
    lat, long = conflicts.loc[conflicts['LOCATION'] == city, ['LATITUDE', 'LONGITUDE']].iloc[0]
    
    # convert lat and long to floats
    lat = float(lat)
    long = float(long)

    # Create marker for city with bold text
    popup_str = "<strong>{}</strong><br>{} fatalities".format(city, fatalities)
    flm.Marker(location=[lat, long],
                  popup=popup_str,
                  icon=flm.Icon(color='red', icon='info-sign')).add_to(map)
    
# save the map as an HTML file
map.save('top_fatalities.html')
map


# In[18]:


# top 10 cities with the most conflicts
top_ten_conflicts = conflicts.groupby('LOCATION')['CONFLICT'].count().nlargest(10)


# In[19]:


# group conflicts by year and event type
conflict_counts = conflicts.groupby(['YEAR', 'CONFLICT']).size().reset_index(name='COUNT')

# create pivot table with year as rows and event types as columns
pivot_table = conflict_counts.pivot_table(index='YEAR', columns='CONFLICT', values='COUNT', aggfunc='sum')

# create heatmap using seaborn
sns.set(style='white')
plt.figure(figsize=(12,8))
sns.heatmap(pivot_table, cmap='YlOrRd', annot=True, fmt='d', linewidths=.5)
plt.title('Number of Conflicts by Type and Year')
plt.show()

