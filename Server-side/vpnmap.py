
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from pyparsing import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

# Pyparsing syntaxis stuff declaration
digits = "0123456789"
colon,semi,period,comma,lbrace,rbrace,quote = map(Literal,':;.,{}"')
number = Word(digits)
hexint = Word(hexnums,exact=2)
dnschars = Word(alphanums + '-') # characters permissible in DNS names

mac = Combine(hexint + (":" + hexint) * 5)("mac_address")
ip = Combine(number + period + number + period + number + period + number)
ips = delimitedList(ip)("ip_addresses")
hardware_ethernet  = Literal('hardware') + Literal('ethernet') + mac + semi
hostname = dnschars
domainname = dnschars + OneOrMore("." + dnschars)
fqdn = Word(alphanums+'-_.').setName('fqdn')("fqdn") #= Combine(hostname + period + domainname)("fqdn")

fixed_address  = Literal('fixed-address') + ips + semi
ddns_hostname = Literal('ddns-hostname') + hostname + semi
ddns_domainname = Literal('ddns-domainname') + quote + domainname + quote + semi

# Put the grammar together to define a host declaration
host = Literal('host') + fqdn + lbrace + Optional(ddns_hostname) + Optional(ddns_domainname) + Optional(hardware_ethernet) + Optional(fixed_address) + rbrace

# Variable that stores list of hosts
hostslist = [['','',''] for i in range(255)]

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
def main():
    #parsing of dhcpd.conf
    ##reading from file to string
    f = open('/etc/dhcp/dhcpd.conf', 'r')
    filestring =  f.read()
    ##parsing
    results = host.scanString(filestring)
    ##converting from ParseResult to array of arrays of strings with appropriate positions of records in list
    for result in results:
        hostslist[int(((result[0].ip_addresses[0]).split('.'))[3])]=[str(result[0].fqdn), str(result[0].mac_address), str(result[0].ip_addresses[0])]
    f.close()
    print ("dhcpd.conf parsed successfully")
    #authorization in Google SpreadsheetAPI
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    spreadsheetId = '1dOkIhJ8JMMQTRHrk6PxNo-Qgc3XRzGvw0w-VPKPiUYU' 
    rangeName = 'Hosts!A2:C255'
    #writing to spreadsheet
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": rangeName,
         "majorDimension": "ROWS",
         "values": hostslist[2:]},
]
}).execute()
    #reading from spreadsheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    #printing results of reading from spreadsheet
    if not values:
        print('No data found.')
    else:
        #print('Name, Major:')
        i = 0
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('row number %s' % i)
            if row:
                print('%s, %s, %s' % (row[0], row[1], row[2]))
            i+=1

if __name__ == '__main__':
    main()
