"""
commentreplybot.py
"""

import authconfig
from bot import basegpgbot
from helpers import config
from db import dbfacade
import praw.exceptions as prawexceptions
import sys
import logging


log = logging.getLogger(config.title)


class CommentReplyBot(basegpgbot.BaseGPGBot):

    def __init__(self):
        super().__init__()
        self.db = dbfacade.DBFacade()

    #########################
    # COMMENT RESPONSE FLOW #
    #########################

    def run(self):
        log.debug(f"Running {self.__class__.__name__}")
        self.check_inbox_for_comment_replies()

    def check_inbox_for_comment_replies(self):
        new_comment_replies = self.reddit.get_unread_comment_replies_from_inbox()
        log.info("Num new comments: " + str(len(new_comment_replies)))
        for item in new_comment_replies:
            result = self.process_unread_comment(item)
            log.info("Process unread comment result: " + str(result))

    def process_unread_comment(self, comment):
        comment.upvote()
        comment.mark_read()

        comment_author = comment.author

        parent_submission = comment.submission
        submission_author = parent_submission.author

        if comment_author != submission_author:
            # comment is not from submission OP, do nothing
            return

        if comment_author == self.get_current_reddit_user():
            # we are the author, do not reply
            return

        # Check if we've already responded to this comment
        if self.is_already_saved_to_db(comment):
            log.debug("Comment already saved to DB, skipping: " + comment.id)
            return

        validated_submission = self.validate_submission(parent_submission)
        if validated_submission is None:
            # Comment is not on a validated post, do nothing
            return

        encrypted_message = self._extract_gpg_message_from_comment(comment)
        if encrypted_message == '':
            # message is not encrypted, do nothing
            return

        # We have an encrypted message
        # Decrypt it
        client = self.get_gpg_client()
        output = client.decrypt(encrypted_message, authconfig.key_passphrase)

        if not output.ok:
            log.error("Decryption Error: " + str(output.stderr))
            return output

        result = self.reply_to_validated_comment(comment, validated_submission, str(output))
        return result

    def reply_to_validated_comment(self, validated_comment, validated_submission, response_text):
        try:
            message = self._write_encrypted_message_for_validated(validated_submission, quote=response_text)
        except ValueError as err:
            log.error("Error encrypting message: " + str(err))
            return err

        # API rate limit is 8 minutes, will get praw.exceptions.APIException
        try:
            log.debug("Replying to comment: " + validated_comment.id)
            result = validated_comment.reply(message)
        except prawexceptions.APIException as err:
            validated_comment.mark_unread()
            log.error("Received praw exception: " + str(err))
            log.info("Exiting...")
            sys.exit()

        self.save_comment_to_db(validated_comment)

        return result

    def _extract_gpg_message_from_comment(self, comment):
        raw = comment.body
        found_string = self.reader.extract_gpg_content_from_string('msg', raw)
        if found_string != '':
            return found_string
        second_try = self.reader.extract_gpg_content_from_string_bad_formatting(raw)
        return second_try

    def is_already_saved_to_db(self, comment):
        comment_id = comment.id
        result = self.db.fetch_comment(comment_id)
        log.debug("DB Fetch:" + str(result))
        return result

    def save_comment_to_db(self, comment):
        comment_id = comment.id
        self.db.insert_comment(comment_id)
