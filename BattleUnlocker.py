import praw
import OAuth2Util
import time
import requests

plag_names = []
INTERVAL = 5 #minutes
running = True
unlock = 'Unlocking' # Text for unlocking
vote = 'Voting' # Text for voting
subname =  'photoshopbattles'
username ='PhotoShopBattles'
user_agent = "Battle Unlocker by /u/Captain_McFiesty ver 0.2"

r = praw.Reddit(user_agent)
o = OAuth2Util.OAuth2Util(r)

def approve_comments(all_comments):
    for comment in all_comments:
        if(comment.banned_by.name == 'AutoModerator'):
            comment.approve()
    return

def check_flair(submission):
    if ('| ' + unlock) in submission.link_flair_text:
        print('Submission: %r' % submission.id)
        print('Approving Comments')
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        approve_comments(flat_comments)
        ftext = submission.link_flair_text
        submission.set_flair(flair_text =
                             (ftext[:(len(ftext)-len(unlock))] + vote),
                             flair_css_class = 'green')
        print('Changed flair')
    return
        


def do_code():
    user = r.get_redditor(username)
    for submission in user.get_submitted(limit=5):
        if submission.subreddit.display_name == subname:
            check_flair(submission)    
    return

#do_code()

while running:
    try:
        o.refresh()
        do_code()
        running = False
    except KeyboardInterrupt:
        running = False
    except (praw.errors.APIException):
        print("[ERROR]: APIException")
    except (praw.errors.HTTPException):
        print("[ERROR]: HTTPException")
        time.sleep(INTERVAL/2*60)
        continue
    except (praw.errors.PRAWException):
        print("[ERROR]: PRAWException")
        time.sleep(INTERVAL/2*60)
        continue
    except (requests.exceptions.ConnectionError):
        print("Internet down")
        time.sleep(INTERVAL/2*60)
        continue
    except (Exception):
        print("[ERROR]: Other error")
        break
