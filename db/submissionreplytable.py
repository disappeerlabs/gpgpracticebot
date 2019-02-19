"""
submissionreplytable.py

Model for sqlite submission reply db table
"""

from db import abstractdbtable


class SubmissionReplyTable(abstractdbtable.AbstractDBTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'SubmissionReply'

    @property
    def data_row_name(self):
        return 'SubmissionReplyTableRow'

    @property
    def column_names_tuple(self):
        cols = ('submission_id', )
        return cols

