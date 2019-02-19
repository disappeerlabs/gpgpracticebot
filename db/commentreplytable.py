"""
commentreplytable.py

Model for sqlite comment reply db table
"""

from db import abstractdbtable


class CommentReplyTable(abstractdbtable.AbstractDBTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'CommentReply'

    @property
    def data_row_name(self):
        return 'CommentReplyTableRow'

    @property
    def column_names_tuple(self):
        cols = ('comment_id', )
        return cols

