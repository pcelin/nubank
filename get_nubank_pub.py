from pynubank import Nubank
import pandas as pd
from datetime import datetime, date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode

# It should be created a virutal environment for running this script.
# This environment will be used to install pynubank. 
# Documentation can be found in: https://github.com/andreroggeri/pynubank

nu = Nubank()
nu.authenticate_with_cert('YOUR_CPF', 'YOUR_PASSWORD', 'YOUR_CERT.p12')

# Getting statements from NuConta.
nuconta = nu.get_account_statements()
nuconta = pd.DataFrame(nuconta)
nuconta['postDate'] = pd.to_datetime(nuconta['postDate']).dt.date
nuconta = nuconta[nuconta['postDate'] > pd.to_datetime('2020-06-01').date()] # Period of interest. You should change it if necessary.
nuconta.to_excel('nuconta.xlsx', index=False)

# Getting credit cardt statements.
credcard = nu.get_card_statements()
credcard = pd.DataFrame(credcard)
credcard['time'] = pd.to_datetime(credcard['time'])
credcard['time'] = pd.to_datetime(credcard['time'].dt.strftime('%Y-%m-%d'), format='%Y-%m-%d')
credcard = credcard[credcard['time'] > '2020-06-01']
credcard.to_excel('credcard.xlsx', index=False)


