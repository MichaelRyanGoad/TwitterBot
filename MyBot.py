import tweepy
import time
import re

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_index.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

#1222667249187573761 for development (first mention id)
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

#1222667249187573761 for development (first mention id)
def reply_to_tweets():
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        t = mention.full_text
        t = t.lower()
        store_last_seen_id(mention.id, FILE_NAME)
        if '#helloworld' in t:
            print('hello world found... responding ', t)
            api.update_status('#HelloWorld back to you!', mention.id)
        elif '#countwords' in t:
            print('count words found. counting and responding...')
            ans = countWords(mention.user.screen_name)
            api.update_status('The most commonly used word was: '+ str(ans[0]) + '. It was used ' + str(ans[1]) + ' times.', mention.id)

#Count words in the last 20 tweets. Tweet back the most commonly used word.
def countWords(id):
    mentions = api.user_timeline(id, tweet_mode='extended')
    vocab = dict({})

    for mention in reversed(mentions):
        text = mention.full_text
        words = cleanString(text)
        for word in words:
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1
    maxKey = max(vocab, key=vocab.get)
    print('the most used word is: ', maxKey)
    print('Times used: ', vocab[maxKey])
    print(vocab)
    return (maxKey, vocab[maxKey])

def cleanString(myString):
    p = re.compile(r'[^a-zA-Z ]+')
    retString = re.sub(p, '', myString).lower()
    words = retString.split()
    return words

while True:
    print('A')
    reply_to_tweets()
    time.sleep(15)
