"""
redditclient.py

Module for reddit client class an abstraction over the reddit api wrapper
"""

import praw
import authconfig


class RedditClient:

    def __init__(self, botuser=True):
        self.client = self.get_reddit_client(botuser=botuser)

    def get_reddit_client(self, botuser=True):
        if botuser:
            client_id = authconfig.bot_app_id
            client_secret = authconfig.bot_app_secret
            user_agent = authconfig.bot_user_agent
            username = authconfig.bot_user_name
            password = authconfig.bot_user_password
        else:
            client_id = authconfig.app_id
            client_secret = authconfig.app_secret
            user_agent = authconfig.user_agent
            username = authconfig.user_name
            password = authconfig.user_password

        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent,
                             username=username,
                             password=password)
        return reddit

    def get_subreddit(self, name):
        sub = self.client.subreddit(name)
        return sub

    def get_new_posts(self, subreddit):
        if isinstance(subreddit, type('')):
            s = self.get_subreddit(subreddit)
        else:
            s = subreddit
        n = s.new()
        return n

    def post_to_subreddit(self, subreddit_name, title, self_text):
        subreddit = self.get_subreddit(subreddit_name)
        result = subreddit.submit(title, selftext=self_text)
        return result

    def get_random_post(self):
        sub = self.client.random_subreddit(nsfw=False)
        post = sub.random()
        return post.shortlink

    def get_inbox(self):
        return self.client.inbox

    def get_unread_comment_replies_from_inbox(self):
        i = self.get_inbox()
        unread = i.unread()
        return [u for u in unread if u.was_comment and u.subject == 'comment reply']

    def get_current_user(self):
        user = self.client.user.me()
        return user
