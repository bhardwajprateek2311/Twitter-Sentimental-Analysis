
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import matplotlib.pyplot as plt
from zipfile import ZipFile 
import os 
import xlsxwriter

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'L4ROQj8rhzrJ269XOfdUlSh43'
        consumer_secret = 'WWReiZIgd8QwgPdiHZHMb84r4rulcVOw4uhUAOyotTC36DlAXu'
        access_token = '1163443965988724737-ivY7BvxXUiGf9ShpRCuIEvh3JIJsWD'
        access_token_secret = '46KVcnVm8zZ4XCASebwYNbVkDsrYVI1RRu9jm4Pg0I6dm'
  
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
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
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
        labels = ['Positive','Negative','Neutral']
        colors = ['yellowgreen','lightcoral','gold']
        for one_fig in all_figs:
            all_total = 0
            sentiments = {}
            sentiments["Positive"] = one_fig[0]
            sentiments["Negative"] = one_fig[1]
            sentiments["Neutral"]  = one_fig[2]
            all_total = one_fig[0] + one_fig[1] + one_fig[2]
            sizes = []

            sizes = [sentiments['Positive']/float(all_total), sentiments['Negative']/float(all_total),
                     sentiments['Neutral']/float(all_total)]


            plt.pie(sizes,labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
            plt.axis('equal')

            plt.title('Sentiment for the word - ' + str(one_fig[3])+"\n\n")
            fig_name = "pie_" + str(one_fig[3]) + ".png"
            # Save the figures
            plt.savefig(fig_name)
            #plt.close()
            plt.show()

def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths
            
def zippy(word):
    # path to folder which needs to be zipped 
    directory = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter'
  
    # calling function to get all file paths in the directory 
    file_paths = get_all_file_paths(directory) 
  
    # printing the list of all files to be zipped 
    #print('Following files will be zipped:') 
    #for file_name in file_paths: 
        #print(file_name) 
  
    # writing files to a zipfile 
    with ZipFile(word+'.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            if '.zip' not in file and '.ipynb' not in file and '.py' not in file and 'templates' not in file and 'static' not in file:
                _,tail=os.path.split(file)
                zip.write(tail) 
  
    #print('All files zipped successfully!')
    delete()
    
def xlchart(i,a,b,c,d):
    # Workbook() takes one, non-optional, argument   
    # which is the filename that we want to create. 
    workbook = xlsxwriter.Workbook('pie_'+i+'.xlsx') 
      
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
        ['Postive% :-', 'Negative% :-', 'Neutral% :-'], 
        [a, b, c], 
    ] 
      
    # Write a row of data starting from 'A1' 
    # with bold format . 
    worksheet.write_row('A1', headings, bold) 
      
    # Write a column of data starting from 
    # A2, B2, C2 respectively. 
    worksheet.write_column('A2', data[0],bold) 
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
        'name': 'Sentimental Ananlysis for '+i, 
        'categories': ['Sheet1', 1, 0, 3, 0], 
        'values':     ['Sheet1', 1, 1, 3, 1], 
        'points': [ 
            {'fill': {'color': '#5ABA10'}}, 
            {'fill': {'color': '#FE110E'}}, 
            {'fill': {'color': '#FFFF00'}}, 
        ], 
    }) 
      
    # Add a chart title. 
    chart2.set_title({'name': 'Sentimental Ananlysis for-'+i+' in last '+str(d)+' tweets'}) 
      
    # Insert the chart into the worksheet (with an offset) 
    # the top-left corner of a chart is anchored to cell C2.   
    worksheet.insert_chart('C2', chart2, {'x_offset': 50, 'y_offset': 15}) 
      
    workbook.close() 
    
def delete():
    directory = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter'
    file_paths = get_all_file_paths(directory) 
    for file in file_paths: 
        if '.zip' not in file and '.ipynb' not in file and '.py' not in file and 'templates' not in file  and 'static' not in file:
            _,tail=os.path.split(file)
            os.remove(tail) 
            
def textw(word):
    global ptweets,ntweets,tweets
    new_path = 'C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\'+word+'.txt'
    tw = open(new_path,'w', encoding="utf-8")
    
    tw.write("\n\nPositive tweets percentage: "+str(100*len(ptweets)/len(tweets)))
    tw.write("\nNegative tweets percentage: "+str(100*len(ntweets)/len(tweets)))
    tw.write("\nNeutral tweets percentage: "+str(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
    
    tw.write("\n\nPositive tweets:\n\n")
    for tweet in ptweets[:10]: 
        tw.write("->"+str(tweet['text'])+"\n\n")
        
    tw.write("\n\nNegative tweets:\n\n") 
    for tweet in ntweets[:10]: 
        tw.write("->"+str(tweet['text'])+"\n\n")
        
    tw.write("\n\nNeutral tweets:\n\n") 
    tweetr=[tweet for tweet in tweets if tweet['sentiment'] != 'positive' and tweet['sentiment'] != 'negative']
    for tweet in tweetr[:10]: 
        tw.write("->"+str(tweet['text'])+"\n\n")
        
    tw.close()
  
def main_fun(astr,icnt): 
    global all_figs,ptweets,ntweets,tweets
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets
    #wb = openpyxl.load_workbook("C:\\Users\\P.Harish Kumar\\Desktop\\Project twitter\\twt_ana.xlsx")
    #s1 = wb.get_sheet_by_name('Sheet1')
    search_words = astr
    Total_tweet_count = icnt
    #print search_words
    search_words_list = search_words.split(",")
    for i in search_words_list:
        print("\nFor Tweet of \"",i,"\" :- \n")
        tweets = api.get_tweets(query = i, count = Total_tweet_count) 
      
        # picking positive tweets from tweets 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        # percentage of positive tweets 
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
        # picking negative tweets from tweets 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        # percentage of negative tweets 
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
        # percentage of neutral tweets 
        print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
      
        # printing first 5 positive tweets 
        print("\n\nPositive tweets:") 
        for tweet in ptweets[:10]: 
            print(tweet['text']) 
      
        # printing first 5 negative tweets 
        print("\n\nNegative tweets:") 
        for tweet in ntweets[:10]: 
            print(tweet['text']) 
        xlchart(i,(100*len(ptweets)/len(tweets)),(100*len(ntweets)/len(tweets)),
                (100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)),Total_tweet_count)
        draw_helper = []
        draw_helper.append(len(ptweets))
        draw_helper.append(len(ntweets))
        draw_helper.append(len(tweets) - len(ntweets) - len(ptweets))
        draw_helper.append(i)
        all_figs=[draw_helper]
        drawing()
        #for writing into a text file
        textw(i)
        zippy(i)
  
