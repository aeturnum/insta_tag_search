from InstagramAPI import InstagramAPI
from .insta_objects import Post, Comment
from .worksheet import WorkbookManager
import argparse
import json
import time
import copy

CONST_TARGET = 400

def wait():
    how_long = 1
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

    parser.add_argument(
        '-c', '--count',
        type=int,
        required=False,
        default=CONST_TARGET,
        help='Number of posts to get (default: 400)'
    )

    args = parser.parse_args()

    api = InstagramAPI(args.username, args.password)
    wbm = WorkbookManager(args.tag, args.username)

    if (api.login()):
        item_count = 0
        max_id = ''
        while True:
            wait()
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
                    added = comment_object.add_to_worksheet(wbm.comment_worksheet)
                    if added:
                        commend_count += 1

                comment_id = ''
                if commend_count < post_obj.comment_count:
                    print(f"Need to fetch more comments for post {str(post_obj)}")
                    while True:
                        wait()
                        api.getMediaComments(post_obj.id, max_id=comment_id)

                        # thanks to https://github.com/LevPasha/Instagram-API-python/blob/master/examples/get_all_comments.py

                        comments = copy.deepcopy(api.LastJson)
                        has_more_comments = comments.get('has_more_comments', False)


                        for comment in comments['comments']:
                            comment_object = Comment.create(post_obj, comment)
                            added = comment_object.add_to_worksheet(wbm.comment_worksheet)
                            if added:
                                commend_count += 1

                        if has_more_comments:
                            comment_id = comments.get('next_max_id', '')
                        else:
                            break

                    # print(f"Final comment count for {str(post_obj)} is {commend_count}")


                item_count += 1

            if item_count >= args.count:
                break
            max_id = posts["next_max_id"]

        print(f"Saved {item_count} items!")
    else:
        print("Can't login!")

    wbm.save()

