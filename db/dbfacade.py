"""
dbfacade.py

Facade object for inserting, accessing records from db tables
"""

from helpers import config
from db import submissionreplytable
from db import commentreplytable


class DBFacade:

    def __init__(self):
        self.database_file = config.database_file
        self.submissions = submissionreplytable.SubmissionReplyTable(self.database_file)
        self.comments = commentreplytable.CommentReplyTable(self.database_file)

    def fetch_submission(self, submission_id):
        result = self.submissions.fetch_record_where_x_equals_y('submission_id', submission_id)
        return result

    def fetch_comment(self, comment_id):
        result = self.comments.fetch_record_where_x_equals_y('comment_id', comment_id)
        return result

    def insert_submission(self, submission_id):
        result = self.submissions.insert_data_row([submission_id])
        return result

    def insert_comment(self, comment_id):
        result = self.comments.insert_data_row([comment_id])
        return result
