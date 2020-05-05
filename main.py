from flask import Flask, render_template, request,redirect
import re
import tweepy
from tweepy import OAuthHandler                     
from textblob import TextBlob
import matplotlib.pyplot as plt
import os,shutil
import xlsxwriter
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import forms


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self,lgn):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = lgn.consumer_key  #'L4ROQj8rhzrJ269XOfdUlSh43'
        consumer_secret = lgn.consumer_secret  #'WWReiZIgd8QwgPdiHZHMb84r4rulcVOw4uhUAOyotTC36DlAXu'
        access_token = lgn.access_token  #'1163443965988724737-ivY7BvxXUiGf9ShpRCuIEvh3JIJsWD'
        access_token_secret = lgn.access_token_secret  #'46KVcnVm8zZ4XCASebwYNbVkDsrYVI1RRu9jm4Pg0I6dm'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0.2:
            return 'more positive'
        elif analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity < -0.2:
            return 'more negative'
        elif analysis.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'

    def get_tweets(self, query, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def drawing():
    global all_figs
    print("\n")
    labels = ['More Positive', 'Positive', 'Negative', 'More Negative', 'Neutral']
    colors = ['yellowgreen', 'lightcoral', 'gold', 'blue', 'cyan']
    for one_fig in all_figs:
        all_total = 0
        sentiments = {}
        sentiments["More Positive"] = one_fig[0]
        sentiments["Positive"] = one_fig[1]
        sentiments["Negative"] = one_fig[2]
        sentiments["More Negative"] = one_fig[3]
        sentiments["Neutral"] = one_fig[4]
        all_total = one_fig[0] + one_fig[1] + one_fig[2] + one_fig[3] + one_fig[4]
        sizes = []

        sizes = [sentiments['More Positive'] / float(all_total), sentiments['Positive'] / float(all_total), sentiments['Negative'] / float(all_total),
                  sentiments['More Negative'] / float(all_total), sentiments['Neutral'] / float(all_total)]

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
        plt.axis('equal')

        plt.title('Sentiment for the word - ' + str(one_fig[5]) + "\n\n")
        fig_name = "pie_" + str(one_fig[5]) + ".png"
        # Save the figures
        plt.savefig('C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\'+fig_name)
        plt.savefig('C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\static\\pie_images\\'+fig_name)
        plt.close()
        
def drawing1():
    global all_figs
    print("\n")
    objects = ('More Positive', 'Positive', 'Negative', 'More Negative', 'Neutral')
    for one_fig in all_figs:
        all_total = one_fig[0] + one_fig[1] + one_fig[2] + one_fig[3] + one_fig[4]
        sentiments = []
        sentiments.append(100*one_fig[0]//all_total)
        sentiments.append(100*one_fig[1]//all_total)
        sentiments.append(100*one_fig[2]//all_total)
        sentiments.append(100*one_fig[3]//all_total)
        sentiments.append(100*one_fig[4]//all_total)
        y_pos = np.arange(len(objects))

        plt.bar(y_pos, sentiments, align='center', alpha=0.5) 
        plt.xticks(y_pos, objects)
        plt.ylabel('Percentage %')
        

        plt.title('Sentiment for the word - ' + str(one_fig[5]) + "\n\n")
        fig_name = "bar_" + str(one_fig[5]) + ".png"
        # Save the figures
        plt.savefig('C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\'+fig_name)
        plt.close()


def zippy():
    dest='C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\t_ana'
    dest1='C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\static\\t_ana'
    shutil.make_archive(dest1, 'zip', dest)


def movef(word):
    source='C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\'
    directory = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\t_ana\\'+word
    os.mkdir(directory)
    files = os.listdir(source)
    for f in files:
        if word+'.png' in f or word+'.txt' in f or word+'.xlsx' in f:
            shutil.move(source+f, directory)
        




def xlchart(i, a, b, c, d, e, f):
    # Workbook() takes one, non-optional, argument
    # which is the filename that we want to create.
    workbook = xlsxwriter.Workbook('C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\pie_' + i + '.xlsx')

    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()

    # Create a new Format object to formats cells
    # in worksheets using add_format() method .

    # here we create bold format object .
    bold = workbook.add_format({'bold': 1})

    # create a data list .
    headings = ['Tweet :-', i]

    data = [
        ['More Postive% :-', 'Postive% :-', 'Negative% :-', 'More Negative% :-', 'Neutral% :-'],
        [a, b, c, d, e],
    ]

    # Write a row of data starting from 'A1'
    # with bold format .
    worksheet.write_row('A1', headings, bold)

    # Write a column of data starting from
    # A2, B2, C2 respectively.
    worksheet.write_column('A2', data[0], bold)
    worksheet.write_column('B2', data[1])

    # Create a chart object that can be added
    # to a worksheet using add_chart() method.

    # here we create a pie chart object
    chart2 = workbook.add_chart({'type': 'pie'})

    # Add a data series to a chart
    # using add_series method.

    # Configure the first series.
    # = Sheet1 !$A$1 is equivalent to ['Sheet1', 0, 0].
    chart2.add_series({
        'name': 'Sentimental Ananlysis for ' + i,
        'categories': ['Sheet1', 1, 0, 5, 0],
        'values': ['Sheet1', 1, 1, 5, 1],
        'points': [
            {'fill': {'color': '#5ABA10'}},
            {'fill': {'color': '#FE110E'}},
            {'fill': {'color': '#FFFF00'}},
            {'fill': {'color': '#0D3AE4'}},
            {'fill': {'color': '#FF830E'}},
        ],
    })

    # Add a chart title.
    chart2.set_title({'name': 'Sentimental Ananlysis for-' + i + ' in last ' + str(f) + ' tweets'})

    # Insert the chart into the worksheet (with an offset)
    # the top-left corner of a chart is anchored to cell C2.
    worksheet.insert_chart('C2', chart2, {'x_offset': 100, 'y_offset': 60})

    workbook.close()


def delete():
    directory = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\t_ana\\'
    file_paths = os.listdir(directory)
    for file in file_paths: 
        shutil.rmtree(directory+file)
        
def delete1():
    directory = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\static\\pie_images\\'
    file_paths = os.listdir(directory)
    for file in file_paths: 
        os.remove(directory+file)


def textw(word):
    global ptweets, ntweets, mptweets, mntweets, tweets
    new_path = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\' + word + '.txt'
    tw = open(new_path, 'w', encoding="utf-8")

    tw.write("\n\nMore Positive tweets percentage: " + str(100 * len(mptweets) / len(tweets)))
    tw.write("\n\nPositive tweets percentage: " + str(100 * len(ptweets) / len(tweets)))
    tw.write("\nNegative tweets percentage: " + str(100 * len(ntweets) / len(tweets)))
    tw.write("\nMore Negative tweets percentage: " + str(100 * len(mntweets) / len(tweets)))
    tw.write("\nNeutral tweets percentage: " + str(100 * (len(tweets) - len(ntweets) - len(ptweets) - len(mntweets) - len(mptweets)) / len(tweets)))

    tw.write("\n\nMore Positive tweets:\n\n")
    for tweet in mptweets[:10]:
        tw.write("->" + str(tweet['text']) + "\n\n")
        
    tw.write("\n\nPositive tweets:\n\n")
    for tweet in ptweets[:10]:
        tw.write("->" + str(tweet['text']) + "\n\n")

    tw.write("\n\nNegative tweets:\n\n")
    for tweet in ntweets[:10]:
        tw.write("->" + str(tweet['text']) + "\n\n")
        
    tw.write("\n\nMore Negative tweets:\n\n")
    for tweet in mntweets[:10]:
        tw.write("->" + str(tweet['text']) + "\n\n")

    tw.write("\n\nNeutral tweets:\n\n")
    tweetr = [tweet for tweet in tweets if tweet['sentiment'] != 'positive' and tweet['sentiment'] != 'negative' and tweet['sentiment'] != 'more positive' and tweet['sentiment'] != 'more negative']
    for tweet in tweetr[:10]:
        tw.write("->" + str(tweet['text']) + "\n\n")

    tw.close()


def main_fun(astr, icnt):
    global all_figs, ptweets, mptweets, ntweets, mntweets, tweets, lgn
    details=[]
    # creating object of TwitterClient Class
    api = TwitterClient(lgn)
    search_words = astr
    k=0
    Total_tweet_count = icnt
    total=[]
    # print search_words
    search_words_list = search_words.split(",")
    for i in search_words_list:
        print("\nFor Tweet of \"", i, "\" :- \n")
        tweets = api.get_tweets(query=i, count=Total_tweet_count)

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        mptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'more positive']
        # percentage of positive tweets
        print("More Positive tweets percentage: {} %".format(100 * len(mptweets) / len(tweets)))
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        mntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'more negative']
        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
        print("More Negative tweets percentage: {} %".format(100 * len(mntweets) / len(tweets)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets) - len(mntweets) - len(mptweets)) / len(tweets)))

        
        
        xlchart(i, (100 * len(mptweets) / len(tweets)), (100 * len(ptweets) / len(tweets)), (100 * len(ntweets) / len(tweets)), (100 * len(mntweets) / len(tweets))
                ,(100 * (len(tweets) - len(ntweets) - len(ptweets) - len(mntweets) - len(mptweets)) / len(tweets)), Total_tweet_count)
        draw_helper = []
        draw_helper.append(len(mptweets))
        draw_helper.append(len(ptweets))
        draw_helper.append(len(ntweets))
        draw_helper.append(len(mntweets))
        draw_helper.append(len(tweets) - len(ntweets) - len(ptweets)  - len(mntweets) - len(mptweets))
        draw_helper.append(i)
        details.append([i,k,(len(mptweets)),(len(ptweets)),(len(ntweets)),(len(mntweets)),((len(tweets) - len(ntweets) - len(ptweets) - len(mntweets) - len(mptweets)))])
        all_figs = [draw_helper]
        total.append(len(tweets))
        drawing()
        drawing1()
        # for writing into a text file
        textw(i)
        movef(i)
        k=k+1
    zippy()
    delete()
    return(details,len(details),total)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Twitter_data(db.Model):

    __tablename__ = 'Twitter_data'

    user = db.Column(db.String(30), primary_key=True)
    password= db.Column(db.String(30))
    email = db.Column(db.String(64))
    consumer_key = db.Column(db.String(64))
    consumer_secret = db.Column(db.String(64))
    access_token = db.Column(db.String(64))
    access_token_secret = db.Column(db.String(64))
    face_key = db.Column(db.String(30))
    

    def __init__(self, email, user, password):
        self.email = email
        self.user = user
        self.password = password

    def __repr__(self):
        return f"Username {self.user} , password {self.password}"

db.create_all()

@app.route('/',methods=['GET','POST'])
def login():
    global lgn
    delete1()

    form1=forms.login1()
    form2=forms.register1()

    if form1.submit.data==True:
        user=Twitter_data.query.get(form1.user1.data)
        if user!=None and user.password==form1.pass1.data:
            lgn=user
            return render_template('button.html',lgn=lgn)
        else:
            return render_template('login.html',check=3)
    
    if form2.submit1.data==True:
        user=Twitter_data.query.get(form2.user.data)
        if user==None and form2.pass2.data==form2.pass3.data:
            new_user=Twitter_data(form2.email.data,form2.user.data,form2.pass2.data)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html',check=1)
        else:
            return render_template('login.html',check=2)
        

    return render_template('login.html',check=0)

@app.route('/tweet_form',methods=['GET','POST'])
def tweet_form():
    global lgn
    form1=forms.tweet_f()
    if form1.submit2.data==True:
        lgn.consumer_key=form1.ck.data
        lgn.consumer_secret=form1.cs.data
        lgn.access_token=form1.at.data
        lgn.access_token_secret=form1.ats.data
        db.session.add(lgn)
        db.session.commit()
        print(lgn.consumer_key)
        print(lgn.consumer_secret)
        return render_template('button.html',lgn=lgn)

    return render_template('tweet_form.html',lgn=lgn)


@app.route('/button')
def button():
    global lgn
    delete1()
    return render_template('button.html',lgn=lgn)



@app.route('/index')
def index():
    delete1()
    return render_template('index.html')


@app.route('/main_p')
def main_p():
    tweet = request.args.get('tweet_w')
    details,length,total=main_fun(tweet, 100)
    return render_template('main_p.html', details=details,length=length,total=total)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('sorry.html',che
                           ck=0), 404


if __name__ == '__main__':
    app.run(debug=True)