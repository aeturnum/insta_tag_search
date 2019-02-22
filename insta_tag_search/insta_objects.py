from dataclasses import dataclass
import json

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
        image_url = None
        caption = post.get("caption", {}).get("text")
        image_url = post.get("image_versions2", {}).get("candidates", [{}])[0].get("url")


        try:
            # todo: add flag for comments being disabled
            # todo: get better location data
            return Post(
                id = post["id"],
                timestamp = post["taken_at"],
                location = {'lat': post.get('lat'), 'lng': post.get('lng')},
                comment_count = post.get("comment_count", 0),
                image_url = image_url,
                user = User.create(post),
                likes = post["like_count"],
                caption = caption
            )
        except Exception as e:
            print(json.dumps(post))
            raise e

    id: str
    timestamp: int
    location: dict
    comment_count: int
    image_url: str
    user: User
    likes: int
    caption: str

    def add_to_worksheet(self, worksheet):
        # _post_labels = [
        #     'Global ID', 'Username', 'Timestamp', 'Location', 'Comments', 'Image URL', 'Likes',
        #     'Caption'
        # ]
        worksheet.append(
            [
                self.id,
                self.user.username,
                self.timestamp,
                json.dumps(self.location),
                self.comment_count,
                self.image_url,
                self.likes,
                self.caption
            ]
        )

    def __str__(self):
        return f"Post({self.user.username})|{self.likes} {self.image_url}"

