import pandas as pd
import random as rand
from datetime import datetime
from time import sleep

FILE_PATH = "C:/Users/frisa/Documents/Record Collection/Record-Collection-20240713.xlsx"

def record_select(df, selection_list):
    selection = df.loc[[rand.randrange(len(df))]]
    slct_list = selection.values.tolist()[0]
    slct_data = {
        'Title': slct_list[0], 
        'Artist': slct_list[1],
        }
    selection_list.append(slct_data)


def main():
    xls_file = pd.ExcelFile(FILE_PATH)

    time_and_date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    selection_list = []

    summary_df = pd.read_excel(xls_file, 'Summary')

    year_select = input('Are you looking for a specific year? (y/n) ')

    while year_select not in ['y', 'n']:
        year_select = input('Invalid input... Are you looking for a specific year? (y/n) ')

    if year_select == 'y':
        year_input = input('Enter the year you are thinking of: ')
        sleep(2)

        while not int(year_input) or len(year_input) > 4:
            year_input = input('Invalid input... Enter the year you are thinking of: ')

        rslt_df = summary_df[summary_df['Release'] == int(year_input)]
        rslt_df = rslt_df.reset_index(drop=True)
        rslt_df = rslt_df.drop(columns=rslt_df.loc[:, 'Release':'Label'])

        while len(selection_list) < 3:
            if len(rslt_df) > 3:
                print(f'\nGot it! There are {len(rslt_df)} vinyls in the collection from that year!')
                print('I will retrieve 3 records from that year...\n')
                sleep(5)
                for i in range(0,3):
                    record_select(summary_df, selection_list)
                    #print(selection_list)
            elif len(rslt_df) < 3 and len(rslt_df) > 0:
                print('\nLess than 3 records exist from that year; so I will retrieve those...')
                sleep(2)
                for i in range(0,len(rslt_df)):
                    selection = rslt_df.loc[[i]]
                    selection_vals = selection.values.tolist()[0]
                    slct_data = {
                        'Title': selection_vals[0], 
                        'Artist': selection_vals[1],
                        }
                    selection_list.append(slct_data)
                #print(selection_list)
                break
            else:
                print('\nHmm...no records exist from that year. Sorry!')
                break
                #input('Please enter a different year or continue.')

        print(f'\nRetrieved {len(selection_list)} records for year {year_input}')
        print('I will now pull some from the rest of the collection')
        sleep(2)
    else:
        print('\nNo worries! Let me pull a few records from the collection...')
        sleep(2)

    for j in range(len(selection_list),5):
        record_select(summary_df, selection_list)

    select_df = pd.DataFrame(selection_list)
    #print(select_df)

    print('\n-------------------------------------')
    print('YOUR MUSIC RECOMMENDATIONS FOR TODAY:')
    print('-------------------------------------\n')
    for i in range(0,len(select_df)):
        print(select_df.loc[[i]])
        sleep(1)

    print('\nYour recommendations have been logged!')

    ####select_df.to_csv(f'recommendations/vinyl_recommendations_{time_and_date}.csv', index=False)


    select_df.to_csv(f'test_recs/vinyl_recommendations_{time_and_date}.csv', index=False)

if __name__ == '__main__':
    main()