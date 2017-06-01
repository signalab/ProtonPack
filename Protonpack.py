""" BotOrNot implementation to catch ghosts in Twitter Universe"""

import botornot
import json
import ast
from pprint import pprint
import time

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
    print ("Welcome to Proton Pack. Ready to catch some bots?" + '\n'
           + "------------------"
           + '\n')

    bon = authenticate()
    checkbot(bon)



def checkbot(bon):
    countAccounts = len(accounts)
    with open ("Accounts_Bots" + ".csv", 'w') as file:
        file.write("Id,Score" + '\n')
        global accountsDone
        accountsDone = 0
        startTime = time.time()
        for account in accounts:
            try:
                print ("Account to check: " + account)
                result = bon.check_account(account)
                jsonStr = json.dumps(result, sort_keys=False, indent=1)
                resultJson = json.loads(jsonStr)
                score = str(resultJson['score'])
                file.write(account + "," + score + '\n')
                accountsDone = accountsDone + 1
                print ("Score: " + str(resultJson['score']))
                print ("Accounts done: " + str(accountsDone) + "/" + str(countAccounts))
                print ("Elapsed Time: " + str((time.time() - startTime) / 60) + " min")
                print ("Aproximate time to go: "+ str((((time.time() - startTime)/accountsDone) * (countAccounts - accountsDone) / 60)) + " min")
                print ("------")

            except Exception as e:
                print ("An exception occurred:")
                print (e)
                file.write(account +"," + "Null" + '\n')
                accountsDone = accountsDone + 1
                print ("Accounts done: " + str(accountsDone) + "/" + str(countAccounts))
                print ("Elapsed Time: " + str((time.time() - startTime) / 60) + " min")
                print ("Aproximate time to go: "+ str((((time.time() - startTime)/accountsDone) * (countAccounts - accountsDone) / 60)) + " min")
                print ("------")
                pass


def authenticate():
    #Authenticate with Twitter
    key = get_key(KEYFILE)
    #print("Succesfully authenticated as " + key["account"])
    bon = botornot.BotOrNot(**key)
    return bon

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
#Por hacer: Graficar la distribución de los bots de 0 a 1

if __name__ == '__main__':
    main()
