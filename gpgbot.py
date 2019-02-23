"""
gpgbot.py

Main run file for GPGBot
"""

import argparse
from bot import redditclient
from bot import basegpgbot
from bot import submissionreplybot
from bot import commentreplybot
from helpers import applogger
from helpers import config

log = applogger.AppLogger(config.title).create()


def parse_args():
    parser = argparse.ArgumentParser(description="The Disappeer r/GPGPractice Bot",
                                     epilog="r/GPGPractice makes perfect!")
    parser.add_argument('-s', '--submission', action='store_true', help='Initialize SubmissionReplyBot')
    parser.add_argument('-c', '--comment', action='store_true', help='Initialize CommentReplyBot')
    parser.add_argument('-b', '--base', action='store_true', help='Initialize BaseGPGBot, for testing and debugging')
    parser.add_argument('-u', '--user', action='store_true', help='Initialize BaseGPGBot with USER creds, default is bot')
    parser.add_argument('-r', '--reddit', action='store_true', help='Initialize Reddit Client for testing and debugging')
    subparser = parser.add_subparsers(dest='subparser', help='Subcommand help')

    runparser = subparser.add_parser('run', help='Run the specified bot')
    runparser.add_argument('-s', '--submission', action='store_true', help='Run SubmissionReplyBot')
    runparser.add_argument('-c', '--comment', action='store_true', help='Run CommentReplyBot')
    runparser.add_argument('-a', '--all', action='store_true', help='Run SubmissionReplyBot and CommentReplyBot')
    runparser.add_argument('-t', '--target', help='Specify target subreddit')

    args = parser.parse_args()
    return args


def get_base_bot(botuser=True):
    bot = basegpgbot.BaseGPGBot(botuser=botuser)
    return bot


def get_submission_reply_bot():
    bot = submissionreplybot.SubmissionReplyBot()
    return bot


def get_comment_reply_bot():
    bot = commentreplybot.CommentReplyBot()
    return bot


def get_reddit_client():
    # TODO: add ability to specify reddit user to authenticate
    client = redditclient.RedditClient()
    return client


def get_target_sub_list(args):
    if args.target == 'private':
        final = config.private_subs
    elif args.target == 'public':
        final = config.public_subs
    else:
        raise NotImplementedError("No such target sub: " + args.target)
    return final


if __name__ == '__main__':
    args = parse_args()
    log.info("gpgbot.py args: " + str(args))

    if args.subparser is None:
        if args.base and args.user:
            basebot = get_base_bot(botuser=False)

        if args.base and not args.user:
            basebot = get_base_bot()

        if args.submission:
            subbot = get_submission_reply_bot()

        if args.comment:
            combot = get_comment_reply_bot()

        if args.reddit:
            reddit = get_reddit_client()

    if args.subparser == 'run':
        if args.submission:
            subbot = get_submission_reply_bot()
            target_list = get_target_sub_list(args)
            subbot.run(target_list)

        if args.comment:
            combot = get_comment_reply_bot()
            combot.run()
