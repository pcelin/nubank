import pandas as pd
from datetime import date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_CREDENTIAL_FILE', scope) # You must create a credential file at https://console.cloud.google.com/
gc = gspread.authorize(credentials)

nuconta = pd.read_excel('nuconta.xlsx')
credcard = pd.read_excel('credcard.xlsx')

nuconta.loc[nuconta['title'] == 'Transferência enviada', 'amount'] *= -1 # Amounts from pynubank are always positive.
nuconta.rename(columns={'postDate': 'date'}, inplace=True)
nuconta = nuconta[['date', 'amount', 'detail']] # Detail column will help to fill out the spending classification.

credcard['amount'] *= -1/100 # Credit card expenses are positive and in cents.
credcard.rename(columns={'time': 'date', 'description': 'detail'}, inplace=True)
credcard = credcard[['date', 'amount', 'detail']]

print(nuconta.columns)
print(credcard.columns)

transactions = pd.concat([credcard, nuconta], ignore_index=True)
transactions['date'] = pd.to_datetime(transactions['date']).dt.date
transactions = transactions.sort_values('date', ascending=False)
transactions.to_excel('transactions.xlsx', index=False)

wks = gc.open_by_key('YOUR_SPREADSHEET_KEY') # You should replace this string with generated spreadsheet key.
worksheet = wks.worksheet('transactions')
df = pd.DataFrame(worksheet.get_all_records())
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
max_date = df['date'].max()
yesterday = date.today() - timedelta(days=1)
if max_date == yesterday:
	print('Transactions data are up to date')
else:
	transactions['date'] = pd.to_datetime(transactions['date'])
	transactions = transactions[transactions['date'] > max_date]
	transactions = pd.concat([transactions, df], ignore_index=True)

	transactions['date'] = transactions['date'].dt.strftime('%Y-%m-%d')
	transactions = transactions.fillna('')
	
	worksheet.clear()
	worksheet.update([transactions.columns.tolist()]+transactions.values.tolist())
