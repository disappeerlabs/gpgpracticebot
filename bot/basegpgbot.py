"""
basegpgbot.py

Base class for gpgbot
"""

from types import SimpleNamespace
from bot import reader
from bot import redditclient
from helpers import config
from gpg import gpgclient
from gpg import gpgpubkeyvalidator
from bot.writer import SubmissionResponseWriter
from bot.writer import CommentResponseWriter
import logging

log = logging.getLogger(config.title)


class BaseGPGBot:
    sub_botuserpage = 'u_disappeerbots'
    sub_private = 'cf760aaa9b034dc4f24de'
    sub_bothome = 'DisappeerGPGBotHome'
    sub_gpgpractice = 'gpgpractice'

    def __init__(self, botuser=True):
        self.reddit = redditclient.RedditClient(botuser=botuser)
        self.reader = reader.Reader()

    def validate_submission(self, submission):
        key_string = self._try_extract_key_string_from_submission(submission)
        g = gpgpubkeyvalidator.GPGPubKeyValidator(key_string)
        if g.valid:
            pair = SimpleNamespace()
            pair.submission = submission
            pair.validator = g
            return pair

    def _write_encrypted_message_for_validated(self, validated_namespace, quote=None):
        writer = self.get_writer(validated_namespace, quote=quote)
        plaintext = writer.write()

        validator = validated_namespace.validator
        client = gpgclient.GPGClient(validator.temp_dir_name)
        ciphertext = client.encrypt(plaintext, validator.key_dict['fingerprint'])

        if not ciphertext.ok:
            raise ValueError(ciphertext.stderr)

        final = writer.format_string_as_code_block(str(ciphertext))
        return final + writer.append_signature()

    def _try_extract_key_string_from_submission(self, submission):
        selftext = submission.selftext
        key_string = self.reader.extract_gpg_content_from_string('key', selftext)
        if key_string != '':
            return key_string

        # TODO: add try/except blocks to catch potential err
        html_string = submission.selftext_html
        key_string = self.reader.extract_gpg_key_from_bad_format_html_string(html_string)
        return key_string

    def _string_contains_gpg_key(self, target_string):
        return self.reader.string_contains_gpg('key', target_string)

    def get_writer(self, submission_validator, quote=None):
        if quote is None:
            return SubmissionResponseWriter(submission_validator, random_post=self.reddit.get_random_post())
        else:
            return CommentResponseWriter(submission_validator, random_post=self.reddit.get_random_post(), quote=quote)

    @staticmethod
    def get_gpg_client():
        return gpgclient.GPGClient(config.bot_key_dir)

    #######################
    # CONVENIENCE HELPERS #
    #######################

    def post_pubkey_to_subreddit(self, subreddit_name, title='DisappeerGPGBot PubKey'):
        valid_target_subs = [self.sub_botuserpage, self.sub_private, self.sub_bothome]
        if subreddit_name not in valid_target_subs:
            log.error(f"You cannot post to {subreddit_name}, valid subs are: " + str(valid_target_subs))
            return None

        self_text = SubmissionResponseWriter.format_string_as_code_block(self._get_bot_pub_key())
        self_text += SubmissionResponseWriter.append_signature()
        result = self.reddit.post_to_subreddit(subreddit_name, title, self_text)
        return result

    def _get_bot_pub_key(self):
        client = self.get_gpg_client()
        pubkey = client.export_key(config.bot_key_id)
        return pubkey

    def get_current_reddit_user(self):
        return self.reddit.get_current_user()
