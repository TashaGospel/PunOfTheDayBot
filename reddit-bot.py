import praw
import time
import json
import requests
import re

filename = "comments_replied"


def authenticate():
    reddit = praw.Reddit("PunOfTheDayBot", user_agent="PunOfTheDayBot v1.0")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def handle_ratelimit(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
                break
            except praw.exceptions.APIException as error:
                # print("Hit rate limit - Sleeping for 10 minutes.")
                print(error)
                time.sleep(60 * 10)

    return wrapper


def get_pun():
    raw = requests.get("http://www.punoftheday.com/cgi-bin/arandompun.pl").text
    pun = re.search(r"&quot;(.+)&quot;", raw).group(1)
    return pun


@handle_ratelimit
def reply(comment):
    comment.reply(">" + get_pun() + "\n\n© 1996-2017 [Pun of the Day.com](http://www.punoftheday.com)")


def run_bot(reddit, comments_replied):
    for comment in reddit.subreddit("puns").comments(limit=5):
        if "!pun" in comment.body and comment.id not in comments_replied:  # and comment.author != reddit.user.me():
            reply(comment)
            comments_replied.append(comment.id)
            save_comments_replied(filename, comments_replied)


def load_comments_replied(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except BaseException:
        return []


def save_comments_replied(filename, comments_replied):
    with open(filename, "w") as f:
        json.dump(comments_replied, f)


def main():
    reddit = authenticate()
    comments_replied = load_comments_replied(filename)
    while True:
        run_bot(reddit, comments_replied)
        time.sleep(20)


if __name__ == '__main__':
    main()
