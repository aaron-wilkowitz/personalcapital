from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
import getpass
import json
import logging
import os
from datetime import datetime, timedelta

# Python 2 and 3 compatibility
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

class PewCapital(PersonalCapital):
    """
    Extends PersonalCapital to save and load session
    So that it doesn't require 2-factor auth every time
    """
    def __init__(self):
        PersonalCapital.__init__(self)
        self.__session_file = 'session.json'

    def load_session(self):
        try:
            with open(self.__session_file) as data_file:    
                cookies = {}
                try:
                    cookies = json.load(data_file)
                except ValueError as err:
                    logging.error(err)
                self.set_session(cookies)
        except IOError as err:
            logging.error(err)

    def save_session(self):
        with open(self.__session_file, 'w') as data_file:
            data_file.write(json.dumps(self.get_session()))

## test 2234
os.environ["PEW_EMAIL"] = "aaron.wilkowitz@gmail.com"
os.environ["PEW_PASSWORD"] = "uncasl55"

def get_email():
    email = os.getenv('PEW_EMAIL')
    if not email:
        print('You can set the environment variables for PEW_EMAIL and PEW_PASSWORD so the prompts don\'t come up every time')
        return input('Enter email:')
    return email

def get_password():
    password = os.getenv('PEW_PASSWORD')
    if not password:
        return getpass.getpass('Enter password:')
    return password

def main():
    email, password = get_email(), get_password()
    pc = PewCapital()
    pc.load_session()

    try:
        pc.login(email, password)
    except RequireTwoFactorException:
        pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
        pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, input('code: '))
        pc.authenticate_password(password)


    holdings_response = pc.fetch('/invest/getHoldings')

    holdings_xyz = holdings_response.json()['spData']
 
    number_holdings = len(holdings_xyz['holdings'])

    for x in range(0,number_holdings):
        print(
                holdings_xyz['holdings'][(x)]['accountName'], '|'
            ,   holdings_xyz['holdings'][(x)]['description'], '|'
            # ,   holdings_xyz['holdings'][(x)]['type'], '|'
            ,   holdings_xyz['holdings'][(x)]['price'], '|'
            ,   holdings_xyz['holdings'][(x)]['value'], '|'
            # ,   holdings_xyz['holdings'][(x)]['fundFees'], '|'
            # ,   holdings_xyz['holdings'][(x)]['originalDescription'], '|'
            ,   holdings_xyz['holdings'][(x)]['quantity'], '|'
            # ,   holdings_xyz['holdings'][(x)]['feesPerYear'], '|'
            ,   holdings_xyz['holdings'][(x)]['external']
        )

if __name__ == '__main__':
    main()

    # accounts_response = pc.fetch('/newaccount/getAccounts')
    
    # now = datetime.now()
    # date_format = '%Y-%m-%d'
    # days = 90
    # start_date = (now - (timedelta(days=days+1))).strftime(date_format)
    # end_date = (now - (timedelta(days=1))).strftime(date_format)
    # transactions_response = pc.fetch('/transaction/getUserTransactions', {
    #     'sort_cols': 'transactionTime',
    #     'sort_rev': 'true',
    #     'page': '0',
    #     'rows_per_page': '100',
    #     'startDate': start_date,
    #     'endDate': end_date,
    #     'component': 'DATAGRID'
    # })
    # pc.save_session()

    # accounts = accounts_response.json()['spData']
    # print('Networth: {0}'.format(accounts['networth']))

    # transactions = transactions_response.json()['spData']
    # print('Number of transactions between {0} and {1}: {2}'.format(transactions['startDate'], transactions['endDate'], len(transactions['transactions'])))