"""
writer.py

Module for writer objects
"""

import datetime


class Writer:

    pub_key_link = 'https://redd.it/arzneu'
    bot_home_sub = 'r/DisappeerGPGBotHome'

    def __init__(self):
        pass

    @property
    def writer_type(self):
        raise NotImplementedError

    @classmethod
    def append_signature(cls):
        signature = f'\n----------\n^(This message was posted by a bot prototype. Reply using the [DisappeerGPGBot PubKey]({cls.pub_key_link}))'
        return signature

    @property
    def message_post_script(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    @staticmethod
    def format_string_as_code_block(message_string):
        final = ''.join(['    ' + item + '\n' for item in message_string.split('\n')])
        return final


class SubmissionResponseWriter(Writer):

    def __init__(self, submission_validator, random_post=None):
        super().__init__()
        self.submission = submission_validator.submission
        self.validator = submission_validator.validator
        self.random_post = random_post

    @property
    def writer_type(self):
        return 'comment'

    @property
    def message_post_script(self):
        message_list = [
            "\nThis message was posted by the Disappeer GPGPractice Bot. This bot is a prototype.\n",
            f"You can find the bot's GPG Public Key at: {self.pub_key_link}\n",
            f"You can find the bot's home sub at: {self.bot_home_sub}\n",
            "\n\nIf you encrypt your reply to this comment, the next time the bot runs, it will respond with an encrypted message quoting your reply.\n",
            "\n\nI hope you found this helpful! Keep up the r/GPGPractice!\n",
            "- u/disappeerbots\n"
        ]
        return ''.join(message_list)

    def write(self):
        submission = self.submission
        author_name = submission.author.name
        author_created = str(datetime.datetime.fromtimestamp(submission.author.created))

        validator_key_dict = self.validator.key_dict
        key_id = validator_key_dict['keyid']
        key_created = str(datetime.datetime.fromtimestamp(int(validator_key_dict['date'])))
        key_expires = str(datetime.datetime.fromtimestamp(int(validator_key_dict['expires'])))
        key_user = str(validator_key_dict['uids'])
        random_post = self.random_post

        message_list = [
            f"Hello {author_name}!\n",
            f"If you can read this, you have successfully decrypted this message!\n",
            f"Here are some fun facts gleaned from your reddit handle and your GPG key . . .\n",
            f"    You have been a redditor since: {author_created}\n",
            f"    Your GPG key id is: {key_id}\n",
            f"    Your GPG key UID is: {key_user}\n",
            f"    Your GPG key was created on: {key_created}\n",
            f"    Your GPG key will expire on: {key_expires}\n",
        ]

        if self.random_post is not None:
            msg = f"    Here is a random reddit post: {random_post}\n"
            message_list.append(msg)

        message_list.extend(self.message_post_script)
        return ''.join(message_list)


class CommentResponseWriter(SubmissionResponseWriter):

    def __init__(self, submission_validator, random_post=None, quote=None):
        super().__init__(submission_validator, random_post=random_post)
        self.quote = quote

    def write(self):
        base_string = super().write()
        message_list = base_string.split('\n')

        if self.quote is not None:
            response_msg = f'\nThis is a response to your encrypted comment:\n"\n{self.quote}\n"\n'
            message_list.insert(2, response_msg)

        return '\n'.join(message_list)
