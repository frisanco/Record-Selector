import pandas as pd
import random
import os
from datetime import datetime

# Load the Excel file
def load_records(file_path):
	try:
		# Read the Excel file
		records = pd.read_excel(file_path, 'Summary')
		return records
	except Exception as e:
		print(f"Error loading file: {e}")
		return None

# Save updates to a CSV file
def save_records_to_csv(records, output_path):
	try:
		records.to_csv(output_path, index=False)
		print(f"\nUpdated recommendations saved to {output_path}. Enjoy listening!")
	except Exception as e:
		print(f"Error saving file: {e}")

# Recommend a random record
def recommend_record(records_df):
	if records_df is not None and not records_df.empty:
		# Add a check for previously recommended records
		if 'Last Recommended' not in records_df.columns:
			records_df['Last Recommended'] = None  # Add column if missing
		if 'Recommendation Count' not in records_df.columns:
			records_df['Recommendation Count'] = 0  # Add column if missing

		random_index = random.randint(0, len(records_df) - 1)
		record = records_df.iloc[random_index]
		record_info = {
			'Title': record['Title'],
			'Artist': record['Artist']
		}

		# Update the recommendation date
		current_date = datetime.now().strftime('%Y-%m-%d')
		records_df.at[random_index, 'Last Recommended'] = current_date
		records_df.at[random_index, 'Recommendation Count'] += 1

		return record_info, records_df
	else:
		print("The records database is empty or not loaded.")
		return None

# Main function
def main():
	if not os.path.exists('recommendations'):
		current_dir = os.getcwd()
		path = os.path.join(current_dir, 'recommendations')
		os.mkdir(path)
		os.chdir(f'{os.getcwd()}/recommendations')
	else:
		os.chdir(f'{os.getcwd()}/recommendations')
		  
	file_path = "C:/Users/frisa/Documents/Record Collection/Record-Collection-20250103.xlsx"  # Replace with your actual file path
	output_csv = "updated_vinyl_recommendations.csv"

	records_df = load_records(file_path)
	
	recommended_record, updated_records = recommend_record(records_df)

	if recommended_record is not None:
		print("\nWe recommend you listen to:")
		print('Title:', recommended_record['Title'])
		print('Artist:', recommended_record['Artist'])

		save_records_to_csv(updated_records, output_csv)

if __name__ == "__main__":
	main()
