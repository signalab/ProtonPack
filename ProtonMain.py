""" BotOrNot implementation to catch ghosts in Twitter Universe"""

import tweepy
import botornot
import json
import time
import sys
import matplotlib.pyplot as plt
import pandas as pd
import plotly.plotly as py

__author__ = "Luis Natera"
__credits__ = "BotOrNot" "Adrián Toscano"
__license__ = "GPL"
__version__ = "0.5"
__maintainer__ = "Luis Natera"
__email__ = "nateraluis@gmail.com"
__status__ = "Prototype"

# Twitter keys, place them in config folder
KEYFILE = "config/mykey.json"

# Main menu to execute the code
def menu ():
	print('Please select an option:\n')
	print('1.- Search an account.\n')
	print('2.- Search an account and her followers.\n')
	print('3.- Search the list of accounts in a file.\n')
	print('4.- I have no idea what I\'m doing, take me out\n')
	op = input()
	print ('\n')

	if op == '1':
		botAccount()
	elif op == '2':
		botFollowers()
		global df
		df = pd.read_csv(accountCheck + '_Followers_BotScore.csv') #df = DataFrame
		plotScores()
	elif op == '3':
		accountList(bon)
		df = pd.read_csv('Accounts_Bots.csv') #df = DataFrame
		plotScores()
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
	except Exception as e:
		print ('An exception ocurred:')
		print (e) # Error, not printing the returned error

# Option 2
def botFollowers():
	twitterLogin()
	global accountCheck
	accountCheck = input ('Please type the username to check: @')
	listFollowers = open (accountCheck + '_Followers.csv', 'w')
	global plotTitle
	plotTitle = "for followers of @" + str(accountCheck)

	listFollowers.write('Source,Target\n')
	# Create a file to store the scores of the followers
	followersScore = open(accountCheck + '_Followers_BotScore.csv', 'w')
	followersScore.write('Id,Score\n')
	# Check the account score
	result = bon.check_account(accountCheck)
	jsonStr = json.dumps(result, sort_keys=False, indent=1)
	resultJson = json.loads(jsonStr)
	score = str(resultJson['score'])
	followersScore.write (accountCheck +','+ score + '\n')
	print ('\n'
		   + '------'
		   + '\n'
		   + '@' + accountCheck + " has a bot probability of: " + str(resultJson['score'])
		   + '\n'
		   + '------'
		   + '\n')
	users = tweepy.Cursor(api.followers, screen_name = accountCheck).items()
	user_followers = api.get_user(screen_name=accountCheck)
	no_followers = user_followers.followers_count
	print ("Now we would check the " + str(no_followers) + ' followers of @' + accountCheck)
	count = 0
	startTime = time.time()

	#for follower in no_followers:
	while True:
		try:
			user = next(users)
			listFollowers.write(user.screen_name + "," + accountCheck + '\n')
			count += 1
			print ("Account to check: " + user.screen_name)
			result = bon.check_account(user.screen_name)
			jsonStr = json.dumps(result, sort_keys=False, indent=1)
			resultJson = json.loads(jsonStr)
			score = str(resultJson['score'])
			followersScore.write (user.screen_name +','+ score + '\n')
			print ('Score: ' + score)
			print ('Accounts done: ' + str(count) + "/" + str(no_followers))
			print ("Elapsed Time: " + str((time.time() - startTime)/60) + " min")
			print ("Aproximate time to go: "+ str((((time.time() - startTime)/count) * (no_followers - count) / 60)) + " min")
			print ("------" + '\n')
			time.sleep(3)
			if count == no_followers:
				return followersScore
				break

		# except tweepy.TweepError:
		# 	print ('Getting a time out, wait 15 minutes')
		# 	time.sleep(60 * 15)
		# 	continue

		except Exception as e:
			listFollowers.write(user.screen_name + "," + accountCheck + '\n')
			print ("An exception occurred")
			print (e)
			listFollowers.write(user.screen_name +"," + accountCheck + '\n')
			followersScore.write (user.screen_name +','+ 'Null' + '\n')
			count += 1
			print ('Accounts done: ' + str(count) + "/" + str(no_followers))
			print ("Elapsed Time: " + str((time.time() - startTime)/60) + " min")
			print ("Aproximate time to go: "+ str((((time.time() - startTime)/count) * (no_followers - count) / 60)) + " min")
			print ("------" + '\n')
			time.sleep(3)
			if count == no_followers:
				return followersScore
				break

		except StopIteration:
			break


# Option 3
def accountList(bon):
	accountsFileTxt = input ('Please type the name of the .txt file to analyse: ')
	accounts_file = open(accountsFileTxt, "r")
	global plotTitle
	plotTitle = "of accounts in " + accountsFileTxt
	accounts = accounts_file.read().split(',')
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
				print ("------" + '\n')

			except Exception as e:
				print ("An exception occurred:")
				print (e)
				file.write(account +"," + "Null" + '\n')
				accountsDone = accountsDone + 1
				print ("Accounts done: " + str(accountsDone) + "/" + str(countAccounts))
				print ("Elapsed Time: " + str((time.time() - startTime) / 60) + " min")
				print ("Aproximate time to go: "+ str((((time.time() - startTime)/accountsDone) * (countAccounts - accountsDone) / 60)) + " min")
				print ("------" + '\n')
				pass

# Option 4
def exit():
	print('Have a nive day!\n')
	sys.exit()

# Count Scores frequency
def getScoresFrequency():
	#df = pd.read_csv(accountCheck + '_Followers_BotScore.csv') #df = DataFrame
	scoresColumn = df.Score #scoresColumn = Series
	scoreCountSet = set() # set of tuples
	#Fill the set
	for score in scoresColumn:
		if score != 'Null':
			scoreCountSet.add((score,1))
	#Check frequency for each score
	for score in scoresColumn:
		for tup in scoreCountSet:
			if tup[0] == score:
				scoreValue = tup[1]
				scoreCountSet.remove(tup)
				newTup = (score, scoreValue + 1);
				scoreCountSet.add(newTup)
				break
	return scoreCountSet

# Plot the scores
def plotScores():
	scoresData = getScoresFrequency()
	plt.scatter(*zip(*scoresData))
	plt.title('Bot probability ' + plotTitle + '\n')
	plt.xlabel("Bot Probability")
	plt.ylabel("Accounts")
	plt.savefig('BotProbability_' + plotTitle +'.png')
	plt.show()

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

def get_keyTweepy(keyfile):
	try:
		with open(keyfile) as fin:
			keyTweepy = json.load(fin)
	except FileNotFoundError as e:
		print ("Key not found")
		sys.exit(1)
	return keyTweepy

# Authenticate in twitter
def authenticateTweepy(keyTweepy):
	global api
	api = authenticate(keyTweepy)
	return auth

def twitterLogin():
	key = get_keyTweepy(KEYFILE)
	auth = tweepy.OAuthHandler(key['consumer_key'], key['consumer_secret'])
	auth.set_access_token(key['access_token'], key['access_token_secret'])
	global api
	api = tweepy.API(auth)
	return api

def main():
	print ('\n'
		   + "------------------"
		   + '\n'
		   + "Welcome to Proton Pack. Ready to catch some bots?"
		   + '\n'
		   + "------------------"
		   + '\n')
	bon = authenticate()
	menu()

# Execute code
if __name__ == '__main__':
	main()
