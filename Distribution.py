import matplotlib.pyplot as plt
import pandas as pd


def getScoresFrequency():
    df = pd.read_csv(input('Please insert the name of the csv file: ')) #df = DataFrame
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

def plotScores():
    scoresData = getScoresFrequency()
    plt.scatter(*zip(*scoresData))
    plt.title('Accounts distribution for bot probability\n')
    plt.xlabel("Bot Probability")
    plt.ylabel("Accounts")
    plt.show()


def main():
    plotScores()

if __name__ == '__main__':
    main()
