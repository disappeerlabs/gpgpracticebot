# Disappeer GPGPractice Bot

Attempt at a Reddit r/GPGPractice bot leveraging the GPG library 
from the [Disappeer GPG Messaging App](https://github.com/disappeerlabs/disappeer). 

## Setup

To run the bots in this project, you must:
- provide values for all necessary variables in your authconfig.py file
- update all values as necessary in helpers/config.py
- create a directory named `keys` in the project root that contains a GPG keyring
with a single private key, and then the passphrase for this key must be added to
your local authconfig.py file

### Help Text

Initialize Clients for Testing and Debugging:
```
$ python gpgbot.py -h
usage: gpgbot.py [-h] [-s] [-c] [-b] [-r] {run} ...

The Disappeer r/GPGPractice Bot

positional arguments:
  {run}             Subcommand help
    run             Run the specified bot

optional arguments:
  -h, --help        show this help message and exit
  -s, --submission  Initialize SubmissionReplyBot
  -c, --comment     Initialize CommentReplyBot
  -b, --base        Initialize BaseGPGBot, for testing and debugging
  -r, --reddit      Initialize Reddit Client for testing and debugging

r/GPGPractice makes perfect!

```

Run clients:
```
$ python gpgbot.py run -h
usage: gpgbot.py run [-h] [-s] [-c] [-a] [-t TARGET]

optional arguments:
  -h, --help            show this help message and exit
  -s, --submission      Run SubmissionReplyBot
  -c, --comment         Run CommentReplyBot
  -a, --all             Run SubmissionReplyBot and CommentReplyBot
  -t TARGET, --target TARGET
                        Specify target subreddit

```

### BaseBot
- Base class for submission and comment reply bots
- Convenience methods for testing and debugging

### SubmissionReplyBot
- Get recent posts from target subreddit, ex. r/GPGPractice
- Detect GPG public key in selftext
- Check db to see if we've responded already, if not . . .
- Encrypt a basic message and respond with a comment
- Save submission id to db

### CommentReplyBot
- Check inbox
- Get unread comment replies
- For each comment reply:
    - upvote
    - mark read
    - if comment author is submission author
        - continue
    - if we haven't replied to comment already:
        - continue
    - if encrypted message in comment 
        - decrypt the message
        - create response quoting decrypted message 
        - reply to comment with response
        - save comment id to db

      