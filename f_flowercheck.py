import pandas as pd
import os
from dotenv import load_dotenv

def flowercheck(char, df):
    flowerdf = pd.read_table('flowers.csv')    
    #check which flowers character has
    print('###Check-for-Flowers###')
    filterflower = df[(df['charn']== char) & df['Name'].str.contains('Black Flower|Blue Flower|Green Flower|White Flower|Red Flower')]
    #print(filterflower)
    filterflower = pd.DataFrame(filterflower)
    filterflower.drop(['Location','ID', 'Count','Slots','charn'], axis=1, inplace=True)
    print('###')
    print(f'{char} got\n{filterflower.to_string(index=False, header=False)} \n### \nCards to finish all missing Flowerquests:')
    #remove these flowers from item_counts table where flowername is matching, remove whole row
    flowerdf = flowerdf[~flowerdf['Flowername'].isin(filterflower['Name'])]
    
    #compute
    # Remove leading and trailing whitespace and convert to lowercase
    flowerdf['Card1'] = flowerdf['Card1'].str.strip().str.lower()
    flowerdf['Card2'] = flowerdf['Card2'].str.strip().str.lower()
    flowerdf['Card3'] = flowerdf['Card3'].str.strip().str.lower()
    flowerdf['Card4'] = flowerdf['Card4'].str.strip().str.lower()

##future? Define a function to strip whitespace from a string
#def strip_whitespace(x):
#    if isinstance(x, str):
#        return x.strip().lower()
#    else:
#        return x

## Apply the function to all cells in the dataframe
#flowerdf = flowerdf.applymap(strip_whitespace)
    
    # Concatenate the Card1 to Card4 columns into a single column
    concatenated = pd.concat([flowerdf['Card1'], flowerdf['Card2'], flowerdf['Card3'], flowerdf['Card4']])

    # Count the occurrences of each item
    item_counts = concatenated.value_counts().reset_index()
    
    #stashdf
    stashdf = df.drop(['ID','Slots','Location','charn'], axis=1)
    
    df_filtered = stashdf[stashdf['Name'].str.contains('Squire|Knight|Crown|Throne') & ~stashdf['Name'].str.contains("Tranix|Forlorn")]
    df_filtered = df_filtered.copy()
    df_filtered['Name'] = df_filtered['Name'].str.strip().str.lower()
    df_filtered['Name'] = df_filtered['Name'].str.replace('a ', '')
    df_filtered_grouped = df_filtered.groupby('Name')['Count'].sum().reset_index()
    
    # Rename the columns
    item_counts.columns = ['Item', 'Count']
    item_counts = pd.DataFrame(item_counts)
    item_counts['Count']= item_counts['Count'].apply(lambda x: -x)
    merged_table = pd.merge(item_counts, df_filtered_grouped, left_on='Item', right_on='Name', how='left')
    merged_table['Name'].fillna(merged_table['Item'], inplace=True)
    merged_table['Count_y'].fillna(0, inplace=True)
    merged_table['toget'] = merged_table['Count_x'] + merged_table['Count_y']
    merged_table.drop(['Name','Count_x', 'Count_y'], axis=1, inplace=True)
    merged_table.sort_values(by='toget', ascending=True, inplace=True)
    merged_table = merged_table[merged_table['toget'] < 0]
    merged_table.reset_index(drop=True, inplace=True)
    merged_table['toget'] = merged_table['toget'].astype(int).abs()
    print(merged_table.to_string(index=False, header=False))
    print('###')
    flowneed= merged_table.copy()
    print(f'###Check for Flowers done on {char}###')
    print('######')
    print('######')
    return flowneed