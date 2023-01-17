import snscrape.modules.twitter as snt
import pickle

import matplotlib.pyplot as plt
import base64
from io import BytesIO

import mysql.connector


def get_data(topic, limit_tweet, dateStart, dateEnd):
    # query = "resesi since:2022-10-01 until:2022-10-16 lang:id"
    query = topic + " since:"+dateStart+" until:"+dateEnd+" lang:id"
    tweets = []
    limit = limit_tweet

    for tweet in snt.TwitterSearchScraper(query, top=True).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append({'date': tweet.date, 'tweet': (
                tweet.content).replace("\n", " ")})

    return tweets


def modelNB(data_tweets):
    tweets = []
    date = []
    with open('./MachineLearning/modelNB.pickle', 'rb') as file:
        unpickled_model = pickle.load(file)

    with open('./MachineLearning/tfidf_vector.pickle', 'rb') as file:
        unpickled_vector = pickle.load(file)
    for tw in data_tweets:
        tweets.append(tw['tweet'])
        # print(tw['tweet'])
        date.append(tw['date'])
    date = [date.strftime('%Y-%m-%d') for date in date]
    print(date)
    test_vectors = unpickled_vector.transform(tweets)
    result = unpickled_model.predict(test_vectors)
    # result[0]
    return {
        'tweets': tweets,
        'date': date,
        'score': result
    }

# Visualisasi


def pie_chart(negative, positive, netral):
    fig, ax = plt.subplots(figsize=(6, 6))
    sizes = [negative, positive, netral]
    labels = ['negatif', 'positif', 'netral']

    if negative > positive and negative > netral:
        explode = (0.1, 0, 0)
    elif positive > negative and positive > netral:
        explode = (0, 0.1, 0)
    elif netral > negative and netral > positive:
        explode = (0, 0, 0.1)
    else:
        explode = (0, 0, 0)

    ax.pie(x=sizes, labels=labels, autopct='%1.1f%%',
           explode=explode, textprops={'fontsize': 14})
    ax.set_title('Sentiment Polarity on Tweets Data', fontsize=16, pad=20)
    # plt.show()
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def insertTweets(topic, data_tweets, date_start, date_end, total, positive, negative, netral):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='p2')
    cursor = cnx.cursor()

    query = "INSERT INTO topics (`topik`, `date_start`, `date_end`) VALUES (%s, %s, %s)"
    values = (topic, date_start, date_end)
    cursor.execute(query, values)
    new_id = cursor.lastrowid
    cnx.commit()

    query = "INSERT INTO hasil (`topic_id`, `total`, `positive`, `negative`, `netral`) VALUES (%s, %s, %s, %s, %s)"
    values = (int(new_id), total, positive, negative, netral)
    cursor.execute(query, values)
    cnx.commit()

    for t in data_tweets:
        query = "INSERT INTO tweets (topic_id,tweet,sentiment,tanggal) VALUES (%s, %s, %s, %s)"
        values = (int(new_id), t['tweet'], t['sentimen'], t['date'])
        cursor.execute(query, values)
        cnx.commit()

    cursor.close()
    cnx.close()


def getTopics():
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='p2')
    cursor = cnx.cursor()

    query = "SELECT id,topik ,DATE_FORMAT(date_start, '%Y-%m-%d') as date_start,DATE_FORMAT(date_end, '%Y-%m-%d') as date_end FROM topics"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def getTopic(id):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='p2')
    cursor = cnx.cursor()

    query = "SELECT id,topik ,DATE_FORMAT(date_start, '%Y-%m-%d') as date_start,DATE_FORMAT(date_end, '%Y-%m-%d') as date_end FROM topics WHERE id=" + str(id)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def getHasil(id):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='p2')
    cursor = cnx.cursor()
    query = "SELECT * from hasil WHERE topic_id=" + str(id)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def getTweets(id):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='p2')
    cursor = cnx.cursor()
    query = "SELECT *, DATE_FORMAT(tanggal, '%Y-%m-%d') as tanggal from tweets WHERE topic_id=" + str(id)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def removeTopic(id):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='p2')
    cursor = cnx.cursor()
    query = "DELETE FROM topics WHERE id=%s"
    values = (str(id),)
    cursor.execute(query, values)
    cnx.commit()
    
    query = "DELETE FROM tweets WHERE topic_id=%s"
    values = (str(id),)
    cursor.execute(query, values)
    cnx.commit()
     
    query = "DELETE FROM hasil WHERE topic_id =%s"
    values = (str(id),)
    cursor.execute(query, values)
    cnx.commit()
    return "ok"

