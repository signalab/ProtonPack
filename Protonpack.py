""" BotOrNot implementation to catch ghosts in Twitter Universe"""

import botornot
import json
import ast
from pprint import pprint

# Twitter keys, place them in config folder
KEYFILE = "config/mykey.json"
accounts_file = open("config/accounts.txt", "r")
accounts = accounts_file.read().split(',')


__author__ = "Luis Natera"
__credits__ = "BotOrNot" "Adrián Toscano"
__license__ = "GPL"
__version__ = "0.5"
__maintainer__ = "Luis Natera"
__email__ = "nateraluis@gmail.com"
__status__ = "Prototype"


def main():
    #Authenticate with Twitter
    key = get_key(KEYFILE)
    print("Succesfully authenticated as " + key["account"])
    bon = botornot.BotOrNot(**key)
    checkbot(bon)


# Load the twitter keys
def get_key(keyfile):
    try:
        with open(keyfile) as fin:
            key = json.load(fin)
    except FileNotFoundError as e:
        print("Key not found")
        print(e)
        sys.exit(1)
    return key

def checkbot(bon):
    with open ("Accounts_info" + ".csv", 'w') as file:
        file.write("Id,Score" + '\n')
        for account in accounts:
            try:
                print ("Account to check: " + account)
                result = bon.check_account(account)
                jsonStr = json.dumps(result, sort_keys=False, indent=1)
                resultJson = json.loads(jsonStr)
                score = str(resultJson['score'])
                file.write(account + "," + score + '\n')
                print ("Score: " + str(resultJson['score']))
                print ("------")
            except Exception as e:
                print ("An exception occurred with account: " + account)
                print (e)
                print ("------")
                file.write(account +"," + "Error" + '\n')
                pass

#Por hacer: Graficar la distribución de los bots de 0 a 1

if __name__ == '__main__':
    main()
