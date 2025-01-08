import pandas as pd
import os
import shutil
from datetime import datetime
from time import sleep

def center_text(text):
	"""Centers text in the terminal based on the current terminal width."""
	terminal_width = shutil.get_terminal_size().columns
	return text.center(terminal_width)

def select_random_vinyl(excel_file, log_file):
	# Load vinyl records from the Excel workbook
	try:
		vinyl_df = pd.read_excel(excel_file, 'Summary')
	except Exception as e:
		print(f"Error loading Excel file: {e}")
		return

	# Check if the required columns exist
	required_columns = {'Title', 'Artist'}
	if not required_columns.issubset(vinyl_df.columns):
		print(f"The Excel file must contain the following columns: {required_columns}")
		return

	# Load the log file if it exists
	if os.path.exists(log_file):
		log_df = pd.read_csv(log_file)
		# Exclude previously recommended records
		vinyl_df = vinyl_df.merge(log_df, on=['Title', 'Artist'], how='left', indicator=True)
		vinyl_df = vinyl_df[vinyl_df['_merge'] == 'left_only'].drop(columns=['_merge'])

	# Check if there are any records left to recommend
	if vinyl_df.empty:
		print(center_text("No more vinyl records left to recommend!"))
		return

	# Randomly select a vinyl record
	selected_record = vinyl_df.sample(1).iloc[0]
	
	# Add the current date
	today_date = datetime.now().strftime('%Y-%m-%d')
	selected_record['Date Recommended'] = today_date

	# Print the selected record
	# Centered output
	print("\n" * 2)
	print(center_text("*" * 50))
	print(center_text("Welcome to RAV!"))
	print(center_text("We think you should listen to:"))
	print("\n")
	sleep(5)
	print(center_text(f"Title: {selected_record['Title']}"))
	print(center_text(f"Artist: {selected_record['Artist']}"))
	print(center_text("*" * 50))
	print("\n" * 2)

	# Log the selected record
	selected_log_df = pd.DataFrame([selected_record])

	if not os.path.exists('recommendations'):
		current_dir = os.getcwd()
		path = os.path.join(current_dir, 'recommendations')
		os.mkdir(path)
		os.chdir(f'{os.getcwd()}/recommendations')
	else:
		os.chdir(f'{os.getcwd()}/recommendations')
		
	if os.path.exists(log_file):
		selected_log_df.to_csv(log_file, mode='a', header=False, index=False)
	else:
		selected_log_df.to_csv(log_file, index=False)

	print(f"\nLogged recommendation to {log_file}")

# Example usage
excel_file = 'Record-Collection-20250103.xlsx'  # Replace with the path to your Excel file
log_file = 'recommended_vinyls.csv'  # Replace with the path to your log file
select_random_vinyl(excel_file, log_file)
