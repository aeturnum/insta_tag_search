from InstagramAPI import InstagramAPI
from .insta_objects import Post, Comment
from .worksheet import WorkbookManager
import argparse
import json
import time
import copy

CONST_TARGET = 200

def wait():
    how_long = 2
    print(f"Pausing for {how_long} seconds for Instagram rate limiting")
    time.sleep(how_long)

def get_tags():
    parser = argparse.ArgumentParser(description='Search a number of Instagram posts based on a hashtag .')
    parser.add_argument(
        '-u', '--username',
        type=str,
        required=True,
        help='The Instagram username to be used'
                        )
    parser.add_argument(
        '-p', '--password',
        type=str,
        required=True,
        help='The Instagram username password to be used'
    )

    parser.add_argument(
        '-t', '--tag',
        type=str,
        required=True,
        help='The Instagram Tag to search'
    )

    args = parser.parse_args()

    api = InstagramAPI(args.username, args.password)
    wbm = WorkbookManager(args.tag, args.username)

    if (api.login()):
        wait()
        time.sleep(2)

        item_count = 0
        max_id = ''
        while True:
            api.getHashtagFeed(args.tag, maxid=max_id)
            posts = copy.deepcopy(api.LastJson)
            # print(api.LastJson)  # print last response JSON
            for post in posts["items"]:
                # print(json.dumps(post))
                post_obj = Post.create(post)
                post_obj.add_to_worksheet(wbm.post_worksheet)
                post_obj.user.add_to_worksheet(wbm.user_worksheet)

                commend_count = 0
                for comment in post["preview_comments"]:
                    comment_object = Comment.create(post_obj, comment)
                    comment_object.add_to_worksheet(wbm.comment_worksheet)
                    commend_count += 1

                if commend_count < post_obj.comment_count:
                    print(f"Post {str(post_obj)} has more comments to get.")

                item_count += 1

            if item_count >= CONST_TARGET:
                break
            max_id = posts["next_max_id"]
            wait()

        print(f"Saved {item_count} items!")
    else:
        print("Can't login!")

    wbm.save()

