from dataclasses import dataclass
import json
import time

@dataclass
class User:
    @staticmethod
    def create(user):
        if "user" in user:
            user = user["user"]

        return User(
            username = user["username"],
            full_name = user["full_name"],
            profile_picture_url = user["profile_pic_url"]
        )

    username: str
    full_name: str
    profile_picture_url: str

    def add_to_worksheet(self, worksheet):
        worksheet.append(
            [self.username, self.full_name, self.profile_picture_url],
            key = self.username
        )

@dataclass
class Post:
    @staticmethod
    def create(post):
        try:
            caption = post.get("caption")
            if caption is not None:
                caption = caption.get("text")
            else:
                caption = ""

            image_url = post.get("image_versions2", {}).get("candidates", [{}])[0].get("url")
            location = None
            if post.get('lat') != None and post.get('lng') != None:
                location = {'lat': post.get('lat'), 'lng': post.get('lng')}



            # todo: add flag for comments being disabled
            # todo: get better location data
            return Post(
                id = post["id"],
                timestamp = post["taken_at"],
                location = location,
                comment_count = post.get("comment_count", 0),
                image_url = image_url,
                user = User.create(post),
                likes = post["like_count"],
                caption = caption,
                code = post["code"]
            )
        except Exception as e:
            print(f'Exception encountered in creating post:\n\t{str(e)}\n\tPost:{str(post)}')
            raise e

    id: str
    timestamp: int
    location: dict
    comment_count: int
    code: str
    image_url: str
    user: User
    likes: int
    caption: str

    def make_instagram_url(self):
        # https: // www.instagram.com / p / post["code"] /
        # post["code"]
        return f'https://www.instagram.com/p/{self.code}/'

    def make_location_url(self):
        # https://www.google.com/maps/search/?api=1&query=<lat>,<lng>
        if self.location is None:
            return ''
        else:
            return f'https://www.google.com/maps/search/?api=1&query={self.location["lat"]},{self.location["lng"]}'

    def get_text_timestamp(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.timestamp))

    def add_to_worksheet(self, worksheet):
        # _post_labels = [
        #     'Global ID', 'URL', 'Location', 'Username', 'Timestamp', 'Comment Count', 'Image URL', 'Likes',
        #     'Caption'
        # ]
        worksheet.append(
            [
                self.id,
                self.make_instagram_url(),
                self.make_location_url(),
                self.user.username,
                self.get_text_timestamp(),
                self.comment_count,
                self.image_url,
                self.likes,
                self.caption
            ]
        )

    def __str__(self):
        return f"Post[+{self.likes}]({self.comment_count} comments) {self.make_instagram_url()} by {self.user.username}"


@dataclass
class Comment:
    id: str
    user: User
    post: Post
    content: str

    @staticmethod
    def create(Post, comment):

        return Comment(
            post = Post,
            user = User.create(comment),
            id = str(comment.get("pk")),
            content = comment.get("text")
        )

    def add_to_worksheet(self, worksheet):
        # _comment_labels = [
        #     'Post ID', 'Username', 'Comment ID', 'Content'
        # ]
        return worksheet.append(
            [
                self.post.id,
                self.user.username,
                self.id,
                self.content
            ],
            # avoid duplicate comments
            key = self.id
        )