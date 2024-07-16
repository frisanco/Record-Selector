import pandas as pd
import random as rand
from datetime import datetime

FILE_PATH = "C:/Users/frisa/Documents/Record Collection/Record-Collection-20240713.xlsx"

xls_file = pd.ExcelFile(FILE_PATH)

time_and_date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

tabs = xls_file.sheet_names

# to read all sheets to a map
sheet_to_df_map = {}
for sheet_name in tabs:
    sheet_to_df_map[sheet_name] = xls_file.parse(sheet_name)

selection_list = []

for i in range(0,5):
    selection = sheet_to_df_map['Summary'].loc[[rand.randrange(len(sheet_to_df_map['Summary']))]]
    slct_list = selection.values.tolist()
    title_artist = {'Title': slct_list[0][0], 'Artist': slct_list[0][1]}
    selection_list.append(title_artist)

select_df = pd.DataFrame(selection_list)


print('-------------------------------')
print('YOUR MUSIC RECOMMENDATIONS FOR TODAY: \n')
for i in range(0,len(select_df)):
    print(select_df.loc[[i]])

print('\nYour recommendations have been logged!')

select_df.to_csv(f'recommendations/vinyl_recommendations_{time_and_date}.csv', index=False)
