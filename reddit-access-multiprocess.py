#! /usr/bin/python3

import praw
import pandas as pd
import datetime as dt
import yake
from time import process_time
import csv
import sys
from collections import Counter
from multiprocessing import Process, Queue, freeze_support

numOfKeywordsComments=80
numOfKeywordsSubmissions=20

kw_extractor_comments = yake.KeywordExtractor(top=numOfKeywordsComments)
kw_extractor_posts = yake.KeywordExtractor(top= numOfKeywordsSubmissions)

def get_comments_and_subreddits_users_have_commented_in(user):
    most_common_num = 10
    comment_objects = list(user.comments.top(limit=200))
    comments = ','.join([comment_objects[num].body for num in range(len(comment_objects))])
    most_common = Counter([comment_objects[num].subreddit.display_name for num in range(len(comment_objects))]).most_common(most_common_num)
    if len(most_common) == most_common_num:
        string_subreddits = ','.join([most_common[num][0] for num in range(len(most_common))])
    else:
        string_subreddits = ''
    return comments, string_subreddits

def get_submissions(user):
    #print("Getting users submissions")
    submission_objects = list(user.submissions.top(limit=200))
    submissions = " ".join(submission_objects[num].title for num in range(len(submission_objects)))
    return submissions

def extract_comment_keywords(keyphrase):
    keywords_list = kw_extractor_comments.extract_keywords(keyphrase)
    keywords = ",".join(keywords_list[num][1] for num in range(len(keywords_list)))
    return keywords

def extract_submission_keywords(keyphrase):
    keywords_list = kw_extractor_posts.extract_keywords(keyphrase)
    keywords = ",".join(keywords_list[num][1] for num in range(len(keywords_list)))
    return keywords

personal_use_script = "uw1FJXIt1GijgQ"
secret_key = "ReBJAgWJDRXMFC0fCtQ-6G4bJvw"


def get_data(reddit, csv_reader, data_queue):    
    for i, row in csv_reader.iterrows(): 
        #print("Currently processing user {}".format(row[0]))
        try:  
            user = reddit.redditor(row[0])

            comments, commented_subreddits = get_comments_and_subreddits_users_have_commented_in(user)
            if commented_subreddits == '':
                continue
            submissions = get_submissions(user)
        
            #print("Getting keywords from user comments")
            comments_keywords = extract_comment_keywords(comments)
            #print("Getting keywords from user submissions")
            submission_keywords = extract_submission_keywords(submissions)
            
            row = [row[0], "%s,%s" % (comments_keywords, submission_keywords), commented_subreddits]
            data_queue.put(row)
        except:
            continue
    data_queue.put(['DONE'])

if __name__ == '__main__':
    
    
    with open(sys.argv[1], mode='r') as inp, open(sys.argv[2], 'w') as out:
        csv_writer = csv.writer(out)
        csv_reader = pd.read_csv(inp)
    
        reddit = praw.Reddit(client_id= personal_use_script, \
                             client_secret= secret_key, \
                             user_agent='subsuggester.com', \
                             username='paddyxvy', \
                             password='')
        count = 0
    
    #df_new1, df_new2, df_new3, df_new4 = csv_reader[:1250, :], csv_reader[1250:2500, :], csv_reader[2500:3750, :], csv_reader[3750:len(csv_reader), :]
        df_new1 = csv_reader.iloc[:625]
        df_new2 = csv_reader.iloc[625:1250]
        df_new3 = csv_reader.iloc[1250:1875]
        df_new4 = csv_reader.iloc[1875:2500]
        df_new5 = csv_reader.iloc[2500:3125]
        df_new6 = csv_reader.iloc[3125:3750]
        df_new7 = csv_reader.iloc[3750:4375]
        df_new8 = csv_reader.iloc[4375:len(csv_reader)]
        print(df_new1)
        data_queue = Queue()
        p1 = Process(target=get_data, args=(reddit, df_new1, data_queue))
        p1.start()
        p2 = Process(target=get_data, args=(reddit, df_new2, data_queue))
        p2.start()
        p3 = Process(target=get_data, args=(reddit, df_new3, data_queue))
        p3.start()
        p4 = Process(target=get_data, args=(reddit, df_new4, data_queue))
        p4.start()
        p5 = Process(target=get_data, args=(reddit, df_new5, data_queue))
        p5.start()
        p6 = Process(target=get_data, args=(reddit, df_new6, data_queue))
        p6.start()
        p7 = Process(target=get_data, args=(reddit, df_new7, data_queue))
        p7.start()
        p8 = Process(target=get_data, args=(reddit, df_new8, data_queue))
        p8.start()
        finished = 0
        while finished != 8:
            row = data_queue.get()
            if len(row) == 1:
                finished += 1
            elif len(row) > 1:
                count += 1
                print(count)
                csv_writer.writerow(row)            
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()
        p8.join()
        print('finished')

