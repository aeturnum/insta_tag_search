from InstagramAPI import InstagramAPI
from .insta_objects import Post
from .worksheet import WorkbookManager
import argparse
import json

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
        api.getHashtagFeed(args.tag)
        # print(api.LastJson)  # print last response JSON
        for post in api.LastJson["items"]:
            # print(json.dumps(post))
            post_obj = Post.create(post)
            post_obj.add_to_worksheet(wbm.post_worksheet)
            post_obj.user.add_to_worksheet(wbm.user_worksheet)
        print(f"Saved {len(api.LastJson['items'])} items!")
    else:
        print("Can't login!")

    wbm.save()

