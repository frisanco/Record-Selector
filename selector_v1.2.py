import pandas as pd
import random as rand
import os
import csv
from datetime import datetime
from time import sleep

FILE_PATH = "C:/Users/frisa/Documents/Record Collection/Record-Collection-20240713.xlsx"

def record_select(df, selection_list, past_recs_values):
	selection = df.loc[[rand.randrange(len(df))]]
	slct_list = selection.values.tolist()[0]
	slct_data = {
		'Title': slct_list[0], 
		'Artist': slct_list[1],
		'Times Selected': 0,
		}
	
	if past_recs_values is not None:
		for i in range(0,len(past_recs_values)):
			if slct_data['Title'] == past_recs_values[i]['Title']:
				if slct_data['Artist'] == past_recs_values[i]['Artist']:
					slct_data['Times Selected'] = int(past_recs_values[i]['Times Selected']) + 1
					print(f'\nTitle: {slct_data['Title']}')
					print(f'Artist: {slct_data['Artist']}')
					dup_rec = input('Oops, I already gave this recommendation to you. Do you want to listen again? (y/n) ')

					while dup_rec not in ['y', 'n']:
						dup_rec = input('Invalid input... I previously gave this recommendation to you. Do you want to listen again? (y/n) ')
						print(f'\nTitle: {slct_data['Title']}, Artist: {slct_data['Artist']}')

					if dup_rec == 'y':
						selection_list.append(slct_data)
		else:
			slct_data['Times Selected'] += 1
			selection_list.append(slct_data)
				
	else:
		slct_data['Times Selected'] += 1
		selection_list.append(slct_data)


def filter_selections(filter_rule, summary_df):
	if filter_rule == 'a':
		artist_input = input('Enter the artist you are thinking of: ')
		rslt_df = summary_df[summary_df['Artist'] == artist_input]
	elif filter_rule == 't':
		title_input = input('Enter the album title you are thinking of: ')
		rslt_df = summary_df[summary_df['Title'] == title_input]
	elif filter_rule == 'r':
		release_input = input('Enter the release year you are thinking of: ')

		while not int(release_input) or len(release_input) > 4:
			release_input = input('Invalid input... Enter the year you are thinking of: ')

		rslt_df = summary_df[summary_df['Release'] == int(release_input)]
	
	rslt_df = rslt_df.reset_index(drop=True)
	rslt_df = rslt_df.drop(columns=rslt_df.loc[:, 'Release':'Label'])
	return rslt_df


def main():
	if not os.path.exists('recommendations'):
		current_dir = os.getcwd()
		path = os.path.join(current_dir, 'recommendations')
		os.mkdir(path)
		os.chdir(f'{os.getcwd()}/recommendations')
	else:
		os.chdir(f'{os.getcwd()}/recommendations')

	xls_file = pd.ExcelFile(FILE_PATH)

	selection_list = []

	summary_df = pd.read_excel(xls_file, 'Summary')

	print('\n' + '*'*47)
	print('Good Day! Welcome to the Vinyl Record Selector!')
	print('*'*47)

	usr_filter_select = input('Are you looking to listen to anything in particular? (y/n) ')

	while usr_filter_select not in ['y', 'n']:
		usr_filter_select = input('Invalid input... Are you looking to listen to anything in particular? (y/n) ')

	if usr_filter_select == 'y':
		selected_filter = input('Please enter the filter you would like to apply:\n \
							  a = Artist,\n\
							  t = Album Title,\n\
							  r = Release Year\n')
		
		rslt_df = filter_selections(selected_filter, summary_df)
		sleep(2)

		while len(selection_list) < 2:
			if len(rslt_df) > 2:
				print(f'\nGot it! There are {len(rslt_df)} vinyls in the collection that match the applied filter!')
				print('I will retrieve 2 records with that filter...\n')
				sleep(5)
				for i in range(0,2):
					record_select(summary_df, selection_list)
			elif len(rslt_df) < 2 and len(rslt_df) > 0:
				print('\nLess than 2 records exist from with that filter; so I will retrieve those...')
				sleep(2)
				for i in range(0,len(rslt_df)):
					selection = rslt_df.loc[[i]]
					selection_vals = selection.values.tolist()[0]
					slct_data = {
						'Title': selection_vals[0], 
						'Artist': selection_vals[1],
						}
					selection_list.append(slct_data)
				break
			else:
				print('\nHmm...no records exist from that filter. Sorry!')
				break
				#input('Please enter a different year or continue.')

		print(f'\nRetrieved {len(selection_list)} records for the requested filter')
		print('I will now pull some from the rest of the collection...')
		sleep(2)
	else:
		print('\nNo worries! Let me pull a few records from the collection...')
		sleep(2)

	if os.path.exists('vinyl_recommendations_records.csv'):
		past_recs_values = []
		with open('vinyl_recommendations_records.csv', 'r') as past_recs:
			next(past_recs)
			reader = csv.reader(past_recs)
			for row in reader:
				past_recs_values.append({
					'Title': row[0],
					'Artist': row[1],
					'Times Selected': row[2]
				})
			while len(selection_list) < 4:
				record_select(summary_df, selection_list, past_recs_values)

			print('\n-------------------------------------')
			print('YOUR MUSIC RECOMMENDATIONS FOR TODAY:')
			print('-------------------------------------\n')
			for i in range(0,len(selection_list)):
				print('Title:', selection_list[i]['Title'])
				print('Artist:',  selection_list[i]['Artist'], '\n')
				sleep(1)
			
			print('\nYour recommendations have been logged!')

		with open('vinyl_recommendations_records.csv', 'a', newline='') as updating_recs:
			filewriter = csv.writer(updating_recs)
			for i in selection_list:
				filewriter.writerow(i.values())

	else:
		with open('vinyl_recommendations_records.csv', 'w', newline='') as new_recs:
			filewriter = csv.writer(new_recs)
			filewriter.writerow(['Title', 'Artist', 'Times Recommended'])
			while len(selection_list) < 4:
				record_select(summary_df, selection_list, past_recs_values=None)

			print('\n-------------------------------------')
			print('YOUR MUSIC RECOMMENDATIONS FOR TODAY:')
			print('-------------------------------------\n')
			for i in range(0,len(selection_list)):
				print('Title:', selection_list[i]['Title'])
				print('Artist:',  selection_list[i]['Artist'], '\n')
				sleep(1)
			
			print('\nYour recommendations have been logged! Enjoy your listening!')

			for i in selection_list:
				filewriter.writerow(i.values())


if __name__ == '__main__':
	main()