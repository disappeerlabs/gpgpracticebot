"""
submissionreplybot.py

"""

import sys
import praw.exceptions as prawexceptions
from bot import basegpgbot
from helpers import config
from db import dbfacade
import logging

log = logging.getLogger(config.title)


class SubmissionReplyBot(basegpgbot.BaseGPGBot):

    def __init__(self):
        super().__init__()
        self.db = dbfacade.DBFacade()

    ############################
    # SUBMISSION RESPONSE FLOW #
    ############################

    def run(self, target_sub_list):
        for target in target_sub_list:
            log.debug(f"Running {self.__class__.__name__} on: r/{target}")
            self.respond_to_submissions(target)

    def respond_to_submissions(self, subreddit_name):
        potentials = self.check_new_subreddit_posts_for_gpg_key(subreddit_name)
        log.debug(f"Found potentials: " + str(len(potentials)))
        validated = self.find_validated_submissions(potentials)
        for item in validated:
            result = self.reply_to_validated_submission(item)
            log.info("Reply to validated submission result: " + str(result))

    def check_new_subreddit_posts_for_gpg_key(self, subreddit):
        posts = self.reddit.get_new_posts(subreddit)
        found = []
        for submission in posts:
            if self._string_contains_gpg_key(submission.selftext):
                found.append(submission)
        return found

    def find_validated_submissions(self, target_submissions):
        valid_posts = []
        for submission in target_submissions:

            # Check if we've already responded to this submission
            if self.is_already_saved_to_db(submission):
                log.debug("Submission already saved to DB, skipping: " + submission.title)
                continue

            # Make sure we're not the submitter
            if submission.author == self.get_current_reddit_user():
                continue

            # If not already responded, validate submission
            current = self.validate_submission(submission)
            if current is not None:
                log.debug("Found valid target subission: " + submission.title)
                valid_posts.append(current)

        return valid_posts

    def reply_to_validated_submission(self, validated_namespace):
        submission = validated_namespace.submission
        try:
            message = self._write_encrypted_message_for_validated(validated_namespace)
        except ValueError as err:
            log.error("Error writing encrypted message: " + str(err))
            return err

        # API rate limit is 8 minutes, will get praw.exceptions.APIException
        try:
            log.debug("Replying to submission: " + submission.title)
            result = submission.reply(message)
        except prawexceptions.APIException as err:
            log.error("Received praw exception: " + str(err))
            log.info("Exiting...")
            sys.exit()

        self.save_submission_to_db(submission)

        return result

    def is_already_saved_to_db(self, submission):
        submission_id = submission.id
        result = self.db.fetch_submission(submission_id)
        return result

    def save_submission_to_db(self, submission):
        submission_id = submission.id
        self.db.insert_submission(submission_id)
