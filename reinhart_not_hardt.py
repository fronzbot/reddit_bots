#!/usr/bin/python3

'''
reinhart_not_hardt.py
Author: Kevin Fronczak
Date  : Dec 18, 2016
Desc  : How hard is it to spell 'Reinhart'?  Apparently really fucking difficult,
        otherwise I wouldn't be making this bot.
'''

import praw
import sys
import os
import time
from app import logger

LOGGER  = logger.Logger("reinhart_not_hardt.log")

def main():
  reddit     = praw.Reddit('reinhart_not_hardt')
  subreddit  = reddit.subreddit("sabres+hockey")

  if not os.path.isfile("already_replied.txt"): 
    already_done = []
  else:
    with open("already_replied.txt", "r") as f:
      already_done = f.read()
      already_done = already_done.split("\n")
      already_done = list(filter(None, already_done))
  
  # Read through all submissions
  for submission in subreddit.hot(limit=30):
    fix_post_errors(submission, already_done)
    
  # Run every 10 minutes
  save_post_data(already_done)    

'''
Goes through posts in subreddit(s) and replys if:
  - Title misspells 'Reinhart'
  - Text post misspells 'Reinhart'
  - Comment misspells 'Reinhart'
'''
def fix_post_errors(submission, already_done):
  lc_title = submission.title.lower()
  lc_text  = submission.selftext.lower()
  
  submission.comments.replace_more(limit=0)
  comment_queue = submission.comments[:]
  
  while comment_queue:
    comment = comment_queue.pop(0)
    
    # Check if I've responded at all    
    if comment.author == 'reinhart_not_hardt' and submission.id not in already_done:
      LOGGER.write('Already commented on: '+submission.title)
      already_done.append(submission.id)
    for reply in comment.replies:
      if reply.author == 'reinhart_not_hardt' and comment.link_id not in already_done:
        LOGGER.write('Already Replied to: '+comment.body)
        already_done.append(comment.link_id)
      
    lc_comment = comment.body.lower()
    if 'reinhardt' in lc_comment and comment.link_id not in already_done:
      comment.reply("#")
      LOGGER.write("Replying to Comment: "+lc_comment)
      already_done.append(comment.link_id)
      
  # Check title
  if submission.id not in already_done:
    if 'reinhardt' in lc_title or 'reinhardt' in lc_text:
      submission.reply('#')
      LOGGER.write('Replying to: '+submission.title)
      LOGGER.write(submission.id)
      already_done.append(submission.id)
    
def save_post_data(data):
  f = open("already_replied.txt", "w")
  for id in data:
    f.write(id+'\n')
  f.close()
    
if __name__ == '__main__':
  main()
