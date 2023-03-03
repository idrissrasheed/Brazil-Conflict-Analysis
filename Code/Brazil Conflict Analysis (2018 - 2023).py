#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import libraries
import pandas as pd
import folium as flm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


# In[ ]:


# Import data
conflicts = pd.read_csv('Brazil Political Violence and Protests Dataset.csv')

# Clean data
conflicts = conflicts.rename(columns={'EVENT_TYPE': 'CONFLICT', 'SUB_EVENT_TYPE': 'SUBCONFLICT'})


# In[29]:


# Explore data
## Print first few rows and info of the data
print(conflicts.head())
print(conflicts.info())


# In[28]:


# Print unique conflict and subconflict types
conflict_types = conflicts['CONFLICT'].unique()
subconflict_types = conflicts['SUBCONFLICT'].unique()
print(conflict_types)
print(subconflict_types)


# In[75]:


# Get value counts of conflict types
conflict_counts = conflicts['CONFLICT'].value_counts()

# Calculate percentage of each conflict type
conflict_p = round(conflict_counts / conflict_counts.sum() * 100,2).astype(str) + '%'

# Combine count and percentage into a dataframe
conflict_pc = pd.DataFrame({'COUNT': conflict_counts, 'PERCENTAGE': conflict_p})

# Rename the index column
conflict_pc = conflict_pc.rename_axis('CONFLICT TYPE')

# Create pie chart
plt.pie(conflict_counts, labels=conflict_counts.index, autopct='%1.1f%%')
plt.title('Conflict Types')

# Display the plot
plt.show()

# Display the conflict stats
print(conflict_pc)


# In[74]:


# Get value counts of subconflict types
subconflict_counts = conflicts['SUBCONFLICT'].value_counts()

# Calculate percentage of each subconflict type
subconflict_p = round(subconflict_counts / subconflict_counts.sum() * 100,2).astype(str) + '%'

# Combine count and percentage into a dataframe
subconflict_pc = pd.DataFrame({'COUNT': conflict_counts, 'PERCENTAGE': conflict_p})

# Rename the index column
subconflict_pc = subconflict_pc.rename_axis('SUBCONFLICT TYPE')

# No pie chart because there are too many categories

# Display the conflict stats
print(subconflict_pc)


# In[76]:


# group conflicts by year and event type
conflict_counts = conflicts.groupby(['YEAR', 'CONFLICT']).size().reset_index(name='COUNT')

# create pivot table with year as rows and event types as columns
pivot_table = conflict_counts.pivot_table(index='CONFLICT', columns='YEAR', values='COUNT', aggfunc='sum')

# create heatmap using seaborn
sns.set(style='white')
plt.figure(figsize=(12,8))
sns.heatmap(pivot_table, cmap='YlOrRd', annot=True, fmt='d', linewidths=.5)
plt.title('Number of Conflicts by Type per Year')
plt.show()


# In[39]:


# Print total number of fatalities
total_fatalities = conflicts['FATALITIES'].sum()
print(f'Total number of fatalities: {total_fatalities:,}')


# In[57]:


# Extract year from event date column
conflicts['YEAR'] = pd.to_datetime(conflicts['EVENT_DATE']).dt.year

# Group by year and total fatalities
fat_by_year = conflicts.groupby('YEAR')['FATALITIES'].sum()

# Create datetime objects for x-axis
x = [mdates.datetime.datetime(year, 1, 1) for year in fat_by_year.index]

# Plot line chart
fig, ax = plt.subplots()
ax.plot_date(x, fat_by_year.values, linestyle='--')

# Format x-axis as years
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Label axes and title
plt.xlabel('Year')
plt.ylabel('Fatalities')
plt.title('Number of Fatalities per Year')

# Add the number of fatalities to each plot point
for i, j in enumerate(fat_by_year.values):
    ax.text(x[i], j, str(j), ha='center', va='bottom', weight='bold')

plt.show()


# In[77]:


# Group data fatalities by conflict type
fat_by_conflict_type = conflicts.groupby('CONFLICT')['FATALITIES'].sum().reset_index()
fat_count = fat_by_conflict_type['FATALITIES'].sum()
fat_by_conflict_type['FATALITY_PERCENTAGE'] = round(fat_by_conflict_type['FATALITIES'] / fat_count * 100, 2).astype(str) + '%'

# Plot bar chart of fatalities by conflict type
plt.bar(fat_by_conflict_type['CONFLICT'], fat_by_conflict_type['FATALITIES'])
plt.xticks(rotation=90)
plt.xlabel('Conflict Type')
plt.ylabel('Fatalities')
plt.title('b')
for i, j in enumerate(fat_by_conflict_type['FATALITIES']):
    plt.text(i, j, str(j), ha='center', va='bottom')
plt.show()

print(fat_by_conflict_type)


# In[71]:


# Group fatalities by subconflict type
fat_by_subconflict_type = conflicts.groupby('SUBCONFLICT')['FATALITIES'].sum().reset_index()
fat_count_sub = fat_by_subconflict_type['FATALITIES'].sum()
fat_by_subconflict_type['FATALITY_PERCENTAGE'] = round(fat_by_subconflict_type['FATALITIES'] / fat_count_sub * 100, 2).astype(str) + '%'

# Plot bar chart of fatalities by subconflict type
plt.bar(fat_by_subconflict_type['SUBCONFLICT'], fat_by_subconflict_type['FATALITIES'])
plt.xticks(rotation=90)
plt.xlabel('Subconflict Type')
plt.ylabel('Fatalities')
plt.title('Number of Fatalities by Subconflict')
for i, j in enumerate(fat_by_subconflict_type['FATALITIES']):
    plt.text(i, j, str(j), ha='center', va='bottom')
plt.show()

print(fat_by_subconflict_type)


# In[54]:


# Group top 10 locations with the most fatalities
top_ten_fat = conflicts.groupby('LOCATION')['FATALITIES'].sum().nlargest(10)  

# Create a map centered on Brazil using country capital's lat and long
map = flm.Map(location=[-10.788497,-42.879873], zoom_start=4.2)

# Create a marker for each city in the top 10
for city, fatalities in top_ten_fat.items():
    # get lat and long for each city
    city_rows = conflicts.loc[conflicts['LOCATION'] == city, ['LATITUDE', 'LONGITUDE']]
    if not city_rows.empty:
        lat, long = city_rows.iloc[0]
        
        # convert lat and long to floats
        lat = float(lat)
        long = float(long)

        # create marker for city with bold text
        popup_str = "<strong>{}</strong><br>{} fatalities".format(city, fatalities)
        flm.Marker(location=[lat, long],
                      popup=popup_str,
                      icon=flm.Icon(color='red', icon='info-sign')).add_to(map)
    
# Save the map as an HTML file
map.save('top_fatalities.html')
map


# In[80]:


# Export data tables
conflict_pc.to_csv('Breakdown of Types of Conflicts.csv', index=False)
subconflict_pc.to_csv('Breakdown of Types of Subconflicts.csv', index=False)
fat_by_conflict_type.to_csv('Fatalities Conflict Type.csv', index=False)
fat_by_subconflict_type.to_csv('Fatalities Subconflict Type.csv', index=False)
top_ten_fat.to_csv('Top 10 Locations with the Highest Fatalities.csv', index=False)        

