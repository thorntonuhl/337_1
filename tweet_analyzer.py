from awards_database import awards_database
import nltk

#with open('globestweets.txt', 'r') as tweetsfile:
 #   tweets = tweetsfile.readlines()
  #  tweetsClean = [x.strip() for x in tweets]


##feel free to add to this
testTweetSet = ["RT @goldenglobes: Congratulations to Zootopia (@DisneyZootopia) - Best Animated Feature Film - #GoldenGlobes https://t.co/QKhrkwZvzS",
                "RT @goldenglobes: Congrats to @RyanGosling, who won #GoldenGlobes Best Performance by an Actor in a Motion Picture - Musical or Comedy! htt\u2026",
                "RT @goldenglobes: Casey Affleck shares how he feels after that #GoldenGlobes win for Best Actor in a Motion Picture - Drama! https://t.co/z\u2026",
                "Thank you Meryl Streep for sharing this. Words to live by. \ud83d\ude4c https://t.co/4wL5scJZiL by #ruffoaholic via @c0nvey",
                "Golden Globes: 11 Secrets From Inside the Ballroom https://t.co/R4A3i9WCqg via @variety",
                "Obama thanks Hollywood in note to Golden Globes nominees \nhttps://t.co/GvzBMQDpLB",
                "Congratulations to Damien Chazelle - Best Screenplay - La La Land (@LaLaLand) - #GoldenGlobes https://t.co/rgOcFEiD2r"]


AwardsDatabase = awards_database("",[])
MovieAwardsList = ["Best Motion Picture - Drama","Best Motion Picture - Musical or Comedy","Best Director - Motion Picture","Best Performance by an Actor in a Motion Picture - Drama","Best Performance by an Actor in a Motion Picture - Comedy Or Musical","Best Performance by an Actress in a Motion Picture - Drama","Best Performance by an Actress in a Motion Picture - Comedy Or Musical","Best Performance by an Actor In A Supporting Role In a Motion Picture","Best Performance by an Actress In a Supporting Role In a Motion Picture","Best Screenplay - Motion Picture","Best Original Score - Motion Picture","Best Original Song - Motion Picture","Best Foreign Language Film","Best Animated Feature Film","Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures"]
MovieAwardsKeyWordSets = []
for i in MovieAwardsList:
    j = i.lower()
    j = j.replace("best ", "")
    j = j.replace(" by ", " ")
    j = j.replace(" in ", " ")
    j = j.replace(" a ", " ")
    j = j.replace(" an ", " ")
    MovieAwardsKeyWordSets.append(j.split())

for award in MovieAwardsList:
    AwardsDatabase.add_category(award,[])

##checks if the word "best" shows up. If it does, then it finds which award out of the awards list above is the tweet talking about
def awardCheck(tweet):
    lowerCaseTweet = tweet.lower()
    bestWordIndex = lowerCaseTweet.find("best")
    if (bestWordIndex != -1) and (bestWordIndex + 4 < len(tweet)):
        remainingTweet =  lowerCaseTweet[bestWordIndex+4:]
        remainingTweetWords = remainingTweet.split()
        remainingTweetWordsLength = len(remainingTweetWords)
        if remainingTweetWordsLength >= 10:
            awardWords = remainingTweetWords[:10]
        else:
            awardWords = remainingTweetWords
        awardWordsSet = set(awardWords)
        similarityScores = [0 for i in MovieAwardsList]
        similarWords = [[] for i in MovieAwardsList]
        for i in range(0,len(MovieAwardsList)):
            awardKeyset = MovieAwardsKeyWordSets[i]
            similarWords[i] = [val for val in awardKeyset if val in awardWordsSet]
            similarity = len(similarWords[i])
            similarityScores[i] = similarity#*1.0/len(awardKeyset)
        maxScore = max(similarityScores)
        awardIndex = similarityScores.index(max(similarityScores))
        awardWordsFound = similarWords[awardIndex]
        return (awardIndex, awardWordsFound)
    else:
        print "Useless tweet for awards purposes"
        return (-1, [])

##basically gives you the first n proper nouns that appear at the beginning of the string
def getFollowingRecipientHandleOrName(tweet):
    tk = nltk.word_tokenize(tweet)
    posTaggedTweet = nltk.pos_tag(tk)
    if posTaggedTweet[0][0] == '@':
        twitterHandle = '@' + posTaggedTweet[1][0]
        return (1,twitterHandle)
    i = 0
    recipientName = ''
    while (i < len(posTaggedTweet)) and (posTaggedTweet[i][1] == 'NNP'):
        recipientName += (posTaggedTweet[i][0] + ' ')
        i += 1
    if recipientName != '':
        recipientName = recipientName[:-1]
    return (0,recipientName)

##looks for proper nouns that come after phrases like "congrats to"
def findRecipient(tweet):
    searchPhrases = ["congratulations to", "congrats to"]
    for searchPhrase in searchPhrases:
        index = tweet.lower().find(searchPhrase)
        remainingIndex = index + len(searchPhrase)
        if index != -1 and remainingIndex < len(tweet):
            remainingTweet = tweet[remainingIndex:]
            recipient = getFollowingRecipientHandleOrName(remainingTweet)
            return recipient
    return None

##main function
for tweet in testTweetSet:
    awardCheckResult = awardCheck(tweet)
    if awardCheckResult[0] != -1:
        findRecipientResult = findRecipient(tweet)
        if findRecipientResult != None:
            print MovieAwardsList[awardCheckResult[0]] + "-------" + findRecipientResult[1]
        else:
            print "No recipient found"

