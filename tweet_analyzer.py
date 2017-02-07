from awards_database import awards_database
from imdb import IMDb
import nltk

ia = IMDb()

##IMPORTANT: Switch to localdb for faster access
#ia = IMDb('sql',uri='mysql://root:justwannawait@localhost/imdb2')

awardYears = [2016,2017]
with open('globestweets.txt', 'r') as tweetsfile:
    tweets = tweetsfile.readlines()
    tweetsClean = [x.strip() for x in tweets]


##feel free to add to this
testTweetSet = ["RT @goldenglobes: Congratulations to Zootopia (@DisneyZootopia) - Best Animated Feature Film - #GoldenGlobes https://t.co/QKhrkwZvzS",
                "RT @goldenglobes: Congrats to @RyanGosling, who won #GoldenGlobes Best Performance by an Actor in a Motion Picture - Musical or Comedy! htt\u2026",
                "RT @goldenglobes: Casey Affleck shares how he feels after that #GoldenGlobes win for Best Actor in a Motion Picture - Drama! https://t.co/z\u2026",
                "Thank you Meryl Streep for sharing this. Words to live by. \ud83d\ude4c https://t.co/4wL5scJZiL by #ruffoaholic via @c0nvey",
                "Golden Globes: 11 Secrets From Inside the Ballroom https://t.co/R4A3i9WCqg via @variety",
                "Obama thanks Hollywood in note to Golden Globes nominees \nhttps://t.co/GvzBMQDpLB",
                "Congratulations to Damien Chazelle - Best Screenplay - La La Land (@LaLaLand) - #GoldenGlobes https://t.co/rgOcFEiD2r"]


AwardsDatabase = awards_database("",[])
MovieAwardsList = ["Best Motion Picture - Drama",
                   "Best Animated Feature Film",
                   "Best Motion Picture - Musical or Comedy",
                   "Best Director - Motion Picture",
                   "Best Performance by an Actor in a Motion Picture - Drama",
                   "Best Performance by an Actor in a Motion Picture - Comedy Or Musical",
                   "Best Performance by an Actress in a Motion Picture - Drama",
                   "Best Performance by an Actress in a Motion Picture - Comedy Or Musical",
                   "Best Performance by an Actor In A Supporting Role In a Motion Picture",
                   "Best Performance by an Actress In a Supporting Role In a Motion Picture",
                   "Best Screenplay - Motion Picture",
                   "Best Original Score - Motion Picture",
                   "Best Original Song - Motion Picture","Best Foreign Language Film"]

TVAwardsList = ["Best Television Series - Drama",
                "Best Television Series - Comedy Or Musical",
                "Best Performance by an Actor In A Television Series - Drama",
                "Best Performance by an Actor In A Television Series - Comedy Or Musical",
                "Best Performance by an Actress In A Television Series - Drama",
                "Best Performance by an Actress In A Television Series - Comedy Or Musical",
                "Best Television Mini-Series or Motion Picture made for Television limited series ",
                "Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television limited series ",
                "Best Performance by an Actress In A Mini-series or Motion Picture Made for Television limited series ",
                "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television limited series",
                "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television limited series"]

FullAwardsList = MovieAwardsList + TVAwardsList
for award in FullAwardsList:
    AwardsDatabase.add_category(award,[])
AwardsKeyWordSets = []
for i in FullAwardsList:
    j = i.lower()
    j = j.replace("best ", "")
    j = j.replace(" by ", " ")
    j = j.replace(" in ", " ")
    j = j.replace(" a ", " ")
    j = j.replace(" an ", " ")
    AwardsKeyWordSets.append(j.split())

for award in MovieAwardsList:
    AwardsDatabase.add_category(award,[])

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk

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
        similarityScores = [0 for i in FullAwardsList]
        similarWords = [[] for i in FullAwardsList]
        for i in range(0,len(FullAwardsList)):
            awardKeyset = AwardsKeyWordSets[i]
            similarWords[i] = [val for val in awardKeyset if val in awardWordsSet]
            similarity = len(similarWords[i])
            similarityScores[i] = similarity#*1.0/len(awardKeyset)
        maxScore = max(similarityScores)
        awardIndex = similarityScores.index(max(similarityScores))
        awardWordsFound = similarWords[awardIndex]
        return (awardIndex, awardWordsFound)
    else:
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
    congratsPhrases = ["congratulations to", "congrats to"]
    for congratsPhrase in congratsPhrases:
        index = tweet.lower().find(congratsPhrase)
        remainingIndex = index + len(congratsPhrase)
        if index != -1 and remainingIndex < len(tweet):
            remainingTweet = tweet[remainingIndex:]
            recipient = getFollowingRecipientHandleOrName(remainingTweet)
            if recipient[1] != '':
                return recipient
    entities = get_continuous_chunks(tweet)
    for entity in entities:
        personResults = ia.search_person(entity)
        if len(personResults) >= 1:
            result = personResults[0]
            if result.has_key('name'):
                if result['name'] == entity:
                    return (0,entity)
    for entity in entities:
        movieResults = ia.search_movie(entity)
        if len(movieResults) >= 1:
            result = movieResults[0]
            if result.has_key('title') and result.has_key('year'):
                if result['title'] == entity and (result['year'] == awardYears[0] or result['year'] == awardYears[1]):
                    return (0,entity)
    return None


def analyze_tweets():
    ##main function
    i = 0
    for tweet in tweetsClean:
        # print tweet
        i += 1
        if (i % 500) == 0:
            print i
        awardCheckResult = awardCheck(tweet)
        awardIndex = awardCheckResult[0]
        if awardIndex != -1:
            findRecipientResult = findRecipient(tweet)
            if findRecipientResult != None:
                award = FullAwardsList[awardIndex]
                AwardsDatabase.add_score(award, findRecipientResult[1], 1)
                # print FullAwardsList[awardCheckResult[0]] + "-------" + findRecipientResult[1]
                # else:
                # print "no recipient found"
                # else:
                # print "no info in tweet"
                # print "------------------------------------------------------------------------------------"
    AwardsDatabase.find_winners()
