"""
reader.py

Module for base reader
"""


class Reader:

    target_begin_key = '    -----BEGIN PGP PUBLIC KEY BLOCK-----'
    target_end_key = '-----END PGP PUBLIC KEY BLOCK-----'
    target_begin_message = '    -----BEGIN PGP MESSAGE-----'
    target_end_message = '-----END PGP MESSAGE-----'
    target_begin_key_bad_format = '-----BEGIN PGP PUBLIC KEY BLOCK-----'

    def __init__(self):
        pass

    def string_contains_gpg(self, gpg_type, text_string):
        if gpg_type == 'key':
            begin = self.target_begin_key_bad_format
            end = self.target_end_key
        elif gpg_type == 'msg':
            begin = self.target_begin_message
            end = self.target_end_message
        else:
            raise NotImplementedError("Unknown gpg string type:", gpg_type)

        targets = [begin in text_string, end in text_string]
        return all(targets)

    def extract_gpg_content_from_string(self, content_type, target_string):
        if content_type == 'key':
            begin = self.target_begin_key
            end = self.target_end_key
        elif content_type == 'msg':
            begin = self.target_begin_message
            end = self.target_end_message
        else:
            raise NotImplementedError("Extraction not implemented for content type:", content_type)

        found = target_string.partition(begin)[2].partition(end)[0]
        if found == '':
            return found

        interim = begin + found + end
        final = ''.join(interim.split('    '))
        return final

    def extract_gpg_key_from_bad_format_html_string(self, html_string):
        html = html_string
        initial = html.partition(self.target_begin_key_bad_format)[2].partition(self.target_end_key)[0]

        split = initial.split('\n\n')

        remove_ptags = [i[3:-4] for i in split]

        remove_empty_string = [i for i in remove_ptags if i != '']

        interim = [i + '\n' for i in remove_empty_string]

        for idx, val in enumerate(interim):
            if val == '&#x200B;\n':
                interim[idx] = '\n'

        interim.insert(0, self.target_begin_key_bad_format + '\n')
        interim += self.target_end_key + '\n'
        final = ''.join(interim)
        return final


class SubmissionReader(Reader):

    def __init__(self, submission):
        super().__init__()
        self.submission = submission



class CommentReader(Reader):

    def __init__(self):
        super().__init__()