""" BotOrNot implementation to catch ghosts in Twitter Universe"""

import tweepy
import botornot
import json
import ast
from pprint import pprint
import time
import sys

# Twitter keys, place them in config folder
KEYFILE = "config/mykey.json"
accounts_file = open("config/accounts.txt", "r")
accounts = accounts_file.read().split(',')


def menu ():
    print('Please select an option:\n')
    print('1.- Search an account.\n')
    print('2.- Search an account and her followers.\n')
    print('3.- Search the list of accounts in the "accounts.txt" file.\n')
    print('4.- I have no idea what I\'m doing, take me out\n')
    op = input()
    print ('\n')

    if op == '1':
        botAccount()
    elif op == '2':
        botFollowers()
    elif op == '3':
        accountList(bon)
    elif op == '4':
        exit()

# Option 1
def botAccount():
    accountCheck = input('Please type the username to check: @')
    result = bon.check_account(accountCheck)
    try:
        jsonStr = json.dumps(result, sort_keys=False, indent=1)
        resultJson = json.loads(jsonStr)
        score = str(resultJson['score'])
        print ('\n'
               + '------'
               + '\n'
               + '@' + accountCheck + " has a bot probability of: " + str(resultJson['score'])
               + '\n'
               + '------'
               + '\n')
#        print ("Score: " + str(resultJson['score']) + '\n')
    except Exception as e:
        print ('An exception ocurred:')
        print (e) # Error, not printing the returned error

# Option 2
def botFollowers():
    accountCheck = input ('Please type the username to check: @')

    #Create file to store the followers network
    listFollowers = open (accountCheck + '_Followers.csv', 'w')
    listFollowers.write('Source,Target\n')

    # Create a file to store the scores of the followers
    followersScore = open(accountCheck + '_Followers_BotScore.csv', 'w')
    followersScore.write('Id,Score\n')

    # Check the account score
    result = bon.check_account(accountCheck)
    jsonStr = json.dumps(result, sort_keys=False, indent=1)
    resultJson = json.loads(jsonStr)
    score = str(resultJson['score'])
    followersScore.write (accountCheck +','+ score)
    print ('\n'
           + '------'
           + '\n'
           + '@' + accountCheck + " has a bot probability of: " + str(resultJson['score'])
           + '\n'
           + 'Cheking the followers of ' + accountCheck
           + '\n'
           + '------'
           + '\n')
    # users = tweepy.Cursor(api.followers, screen_name = accountCheck).items()
    # user_followers = api.get_user(screen_name=accountCheck)
    # no_followers = accountCheck.followers_count
    # print (no_followers)

    # Sera necesario autenticarlo con tweepy también para que pueda acceder a la lista de seguidores de las cuentas y comparar cada uno. Está dando un error con la variable api que depende de la autetificación de tweepy.
    # Queda pendiente que revise los seguidores, vaya escribiendo el archivo csv con las cuentas para la red de seguidores y el archivo csv en el que ponga los usuarios y su score. También será necesario imprimir los resultados y poner el conteo de tiempo que falta para la descarga.

# Option 3
def accountList(bon):
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

# Option 4
def exit():
    print('Have a nive day!\n')
    sys.exit()

# Authenticate with twitter and BotorNot
def authenticate():
    key = get_key(KEYFILE)
    global bon
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

def main():
    print ('\n'
           + "------------------"
           + '\n'
           + "Welcome to Proton Pack. Ready to catch some bots?" + '\n'
           + "------------------"
           + '\n')
    bon = authenticate()
    menu()


# Execute code
if __name__ == '__main__':
    main()
