# Brazil Conflict Analysis Report

## Data Description
[The Brazil Conflict Tracker (2018-2023) Kaggle dataset](https://www.kaggle.com/datasets/justin2028/brazil-conflict-tracker-20182023) provides a comprehensive record of both violent and non-violent conflicts in Brazil since 2018. The data source is from the Armed Conflict Location & Event Data Project (ACLED), which tracks real-global political violence and protest in real-time. The last data update was on January 20th, 2023, and the dataset uploader Justin Oh removed ID-related variables and conflicts outside of Brazil provided by ACLED from the original dataset. 

## Questions

* How are various types of conflicts and fatalities spread out annually?
* Which types of conflicts have the highest amount of deaths?
* Which locations in Brazil tend to have the highest death tolls?

## Python Libraries Deployed

* pandas
* folium
* matplotlib
* seaborn

## Analysis
The analysis includes the following steps:

1. Import the necessary libraries and data and clean the data. 

```python
# Import libraries
import pandas as pd
import folium as flm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
```

```python
# Import data
conflicts = pd.read_csv('Brazil Political Violence and Protests Dataset.csv')

# Clean data
conflicts = conflicts.rename(columns={'EVENT_TYPE': 'CONFLICT', 'SUB_EVENT_TYPE': 'SUBCONFLICT'})

# Extract year from event date column for later
conflicts['YEAR'] = pd.to_datetime(conflicts['EVENT_DATE']).dt.year
```

2. Explore the data by printing the first few rows and information about the data, print unique conflict and subconflict types, and obtain the value counts of conflict types. Create a pie chart to visualize the number of conflicts by type and provide tables for conflict and subconflict types.

```python
# Explore data
## Print first few rows and info of the data
print(conflicts.head())
print(conflicts.info())
```

```python
# Print unique conflict and subconflict types
conflict_types = conflicts['CONFLICT'].unique()
subconflict_types = conflicts['SUBCONFLICT'].unique()
print(conflict_types)
print(subconflict_types)
```

```python
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
plt.title('Main Conflict Types')

# Display the plot
plt.show()

# Display the conflict stats
print(conflict_pc)
```

![alt text](https://github.com/idrissrasheed/Brazil-Conflict-Analysis/blob/main/Outputs/Plots/Main%20Conflict%20Type%20Pie%20Chart.png)

```python
# Get value counts of subconflict types
subconflict_counts = conflicts['SUBCONFLICT'].value_counts()

# Calculate percentage of each subconflict type
subconflict_p = round(subconflict_counts / subconflict_counts.sum() * 100,2).astype(str) + '%'

# Combine count and percentage into a dataframe
subconflict_pc = pd.DataFrame({'COUNT': subconflict_counts, 'PERCENTAGE': subconflict_p})

# Rename the index column
subconflict_pc = subconflict_pc.rename_axis('SUBCONFLICT TYPE')

# No pie chart because there are too many categories

# Display the conflict stats
print(subconflict_pc)
```

3. Group conflicts by year and event type, create a pivot table with years as rows and event types as columns, and output a heatmap to visualize the number of conflicts by type per year.

```python
# Group conflicts by year and event type
conflict_counts = conflicts.groupby(['YEAR', 'CONFLICT']).size().reset_index(name='COUNT')

# Create pivot table with year as rows and event types as columns
pivot_table = conflict_counts.pivot_table(index='CONFLICT', columns='YEAR', values='COUNT', aggfunc='sum')

# Create heatmap using seaborn
plt.figure(figsize=(12,8))
sns.heatmap(pivot_table, cmap='Blues', annot=True, fmt='d', linecolor='black', linewidths=1)
plt.title('Number of Main Conflicts by Year')
plt.show()
```

![alt text](https://github.com/idrissrasheed/Brazil-Conflict-Analysis/blob/main/Outputs/Plots/Number%20of%20Main%20Conflicts%20by%20Year%20Heatmap.png)

4. Print the total number of fatalities and plot a line chart to visualize the number of fatalities per year.

```python
# Print total number of fatalities
total_fatalities = conflicts['FATALITIES'].sum()
print(f'Total number of fatalities: {total_fatalities:,}')
```

```python
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
plt.xlabel('YEAR')
plt.ylabel('FATALITIES')
plt.title('Number of Fatalities by Year')

# Add the number of fatalities to each plot point
for i, j in enumerate(fat_by_year.values):
    ax.text(x[i], j, str(j), ha='center', va='bottom', weight='bold')

plt.show()
```

![alt text](https://github.com/idrissrasheed/Brazil-Conflict-Analysis/blob/main/Outputs/Plots/Number%20of%20Fatalities%20by%20Year%20Plot.png)

5. Create a pivot table with main conflicts as rows, year as columns and fatalities as values, and output a heatmap to visualize the number of conflicts by type per year.

```python
# create pivot table for num of fatalities by main conflict by year
pivot_table2 = conflicts.pivot_table(index='CONFLICT', columns='YEAR', values='FATALITIES', aggfunc=sum)

# Create heatmap using seaborn
plt.figure(figsize=(12,8))
sns.heatmap(pivot_table2, cmap='Reds', annot=True, fmt='d', linecolor='black', linewidths=1)
plt.title('Number of Fatalities by Main Conflict and Year')
plt.show()
```

![alt text](https://github.com/idrissrasheed/Brazil-Conflict-Analysis/blob/main/Outputs/Plots/Number%20of%20Fatalities%20by%20Main%20Conflict%20and%20Year%20Heatmap.png)

6. Group fatalities by conflict type, plot a bar chart of fatalities by conflict type, and add the number of fatalities to each plot point.

```python
# Group data fatalities by conflict type
fat_by_conflict_type = conflicts.groupby('CONFLICT')['FATALITIES'].sum().reset_index()
fat_count = fat_by_conflict_type['FATALITIES'].sum()
fat_by_conflict_type['FATALITY_PERCENTAGE'] = round(fat_by_conflict_type['FATALITIES'] / fat_count * 100, 2).astype(str) + '%'

# Plot bar chart of fatalities by conflict type
plt.bar(fat_by_conflict_type['CONFLICT'], fat_by_conflict_type['FATALITIES'])
plt.xticks(rotation=90)
plt.xlabel('Conflict Type')
plt.ylabel('Fatalities')
plt.title('Number of Fatalities by Conflict')
for i, j in enumerate(fat_by_conflict_type['FATALITIES']):
    plt.text(i, j, str(j), ha='center', va='bottom')
plt.show()

print(fat_by_conflict_type)
```

![alt text](https://github.com/idrissrasheed/Brazil-Conflict-Analysis/blob/main/Outputs/Plots/Number%20of%20Fatalities%20by%20Main%20Conflict%20Barplot.png)

7. Group fatalities by subconflict type, plotting a bar chart of fatalities by subconflict type, and adding the number of fatalities to each plot point.

```python
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
```

![alt text](https://github.com/idrissrasheed/Brazil-Conflict-Analysis/blob/main/Outputs/Plots/Number%20of%20Fatalities%20by%20Subconflict%20Barplot.png)

8. Group the top 10 locations with the most fatalities and create a folium map to visualize their geographic locations.

```python
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
```

![image](https://user-images.githubusercontent.com/25093626/222829748-96a6599c-21ea-413e-adbb-0f669673aacc.png)

9.  Export the data

```python
# Export data tables
conflict_pc.to_csv('Breakdown of Types of Main Conflicts.csv', index=True)
subconflict_pc.to_csv('Breakdown of Types of Subconflicts.csv', index=True)
fat_by_conflict_type.to_csv('Fatalities by Main Conflict Type.csv', index=False)
fat_by_subconflict_type.to_csv('Fatalities by Subconflict Type.csv', index=False)
top_ten_fat.to_csv('Top 10 Locations with the Highest Fatalities.csv', index=True)             
```
## Key Findings

* Battles (32.4%) and Protests (32.2%) make up the majority of main conflicts 
* Protests decreased between 2019 and 2020 by 61.86% and increased by 62.53% between 2020 and 2021 
* Remote violence and explosives have the rarest occurences out of the other main conflicts
* Strategic development is the only main conflict that contributed to 0 fatalities while making up 3.7% of conflicts
* Violence against civilians (52.61%) has the highest rate of fatalities for main conflicts, attacks (52.46%) have the highest rate of fatalities out of any subconflict
* Manaus has the highest amount of fatalities in the country at a total of 2,344 fatalities 

## Further Considerations
* Create a diagram to investigation the association between "ACTOR1" and "ACTOR" and in relation to fatality rates 
* Build a map to show which "CONFLICT" category is the most prevalent in certain parts of Brazil 
