"""
reddit_to_json.py
Authors: Abdullatif Hassan, David Budaghyan, Dibbyajit Dam
Date Created: November 22, 2020
Description: Collects 334 reddit posts from an input subreddit name and outputs them to a json file
"""

import sys
import pandas
import requests
import os.path as osp
import argparse
import json 
import re
script_dir = osp.dirname(__file__)


# def filter_posts(posts):
#     new_posts = []
#     presidents = ["Trump", "trump", "Biden", "biden"]
#     for post in posts:
#         words = post['data']['title'].split()
#         for president in presidents:
#             if president in words:
#                 new_posts.append(post)
#                 break
#     return new_posts



#FIXED REGEX FOR TRUMP OR BIDEN
def filter_posts(posts):
    new_posts = []
    for post in posts:
        words = post['data']['title']
        #if words.str.contains("(^|[^A-Za-z0-9])Trump([^A-Za-z0-9]|$)", regex=True, case=False) or words.str.contains("(^|[^A-Za-z0-9])Biden([^A-Za-z0-9]|$)", regex=True, case=False):
        if not ((re.search("(^|[^A-Za-z0-9])Trump([^A-Za-z0-9]|$)",words)==None) and (re.search("(^|[^A-Za-z0-9])Biden([^A-Za-z0-9]|$)", words)==None)):
            new_posts.append(post)
    return new_posts


def get_posts(subreddit, num_posts): #input is name of subreddit and number of posts (n) we want to collect, output is a list of n jsons
    posts=[]
    responses = []
    posts_left = num_posts
    first_time = True
    post_limit = 50
    while(posts_left > 0):
        if first_time:
            first_time = False
            data=requests.get(f'http://api.reddit.com/r/{subreddit}/new?limit={post_limit}',
                headers={'User-Agent': 'windows: requests (by/users/aboud)'})
        else:
            data=requests.get(f'http://api.reddit.com/r/{subreddit}/new?limit={post_limit}&after={after}', headers={'User-Agent': 'windows: requests (by/users/aboud)'})

        incoming_posts = data.json()['data']['children'] # store in a list containing answer for each requests (packets of 50 posts usually)
        new_posts = []
        for post in incoming_posts:
            new_posts.append(post)
        new_posts = filter_posts(new_posts)
        responses.append(new_posts)
        posts_left = posts_left - len(new_posts)
        after = data.json()['data']['after']
    for response in responses:
        for post in response:
            posts.append(post)
    return posts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help = 'output json file')
    parser.add_argument('subreddit')
    parser.add_argument('num_posts')
    args = parser.parse_args()
    posts = get_posts(args.subreddit, int(args.num_posts)+40)
    mock_open = open(args.o, 'w')
    write_output = open(args.o, 'a')
    i=0
    for post in posts:
        i = i+1
        write_output.write(json.dumps(post))
        write_output.write("\n")
        if(i==int(args.num_posts)):
            break
    write_output.close()

if __name__ == "__main__":
    main()
