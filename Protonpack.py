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
    results = bon.check_accounts_in(accounts)
    print ("Cheking Accounts, please wait :)")
    resultsBots = list(results)
    jsonStr = json.dumps(resultsBots, sort_keys=False, indent=1)
    print ("You have results")

    resultJson = json.loads(jsonStr)

    with open("data.json", "w") as outf:
       outf.write(str(resultJson))

    resultCounter = 0

    print('\nAccounts analyzed\n')

    for results in resultJson:
        currentJson = results[1]
        print (str(results[0]) +": " + str(currentJson['score']) + '\n')
        resultCounter = resultCounter + 1

#Por hacer: Guardar CSV con datos de botornot y graficar la distribución de los bots de 0 a 1

if __name__ == '__main__':
    main()
