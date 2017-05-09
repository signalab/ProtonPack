""" BotOrNot implementation to catch ghosts in Twitter Universe"""

import botornot
import json
from pprint import pprint

# Twitter keys, place them in config folder
KEYFILE = "config/mykey.json"
accounts_file = open("config/accounts.txt", "r")
accounts = accounts_file.read().split(',')


__author__ = "Luis Natera"
__credits__ = "BotOrNot"
__license__ = "GPL"
__version__ = "0.5"
__maintainer__ = "Luis Natera"
__email__ = "nateraluis@gmail.com"
__status__ = "Prototype"



def main():
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


"""def checkbot(bon):
    results = list(bon.check_accounts_in(accounts))
    #print(results)
"""
for bot in accounts:
    def checkbot(bon):
        #results = list(bon.check_accounts_in(accounts))
        results = bon.check_account("natera")
        with open("data.json", "w") as outf:
            outf.write(str(results))

        print(json.dumps(results, sort_keys=False, indent=1))
        print(results["screen_name"] + ": " + results["score"])

        """
        with open("data.json") as data_file:
            databot = json.load(data_file)
        pprint(databot)
"""



if __name__ == '__main__':
    main()


#bon = botornot.BotOrNot(*key)
