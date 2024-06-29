import instaloader
import modules.configuration as configuration

configuration.load()

instagram_account = configuration.get_value("Instagram", "account")
instagram_username = configuration.get_value("Instagram", "username")
instagram_password = configuration.get_value("Instagram", "password")

L = instaloader.Instaloader()
L.login(instagram_username, instagram_password)

def fetch_latest_post():
    profile = instaloader.Profile.from_username(L.context, instagram_account)
    posts = list(profile.get_posts())
    if posts:
        latest_post = posts[0]
        return latest_post.shortcode, latest_post.url, latest_post.caption
    return None, None, None

# Function to fetch the latest story
def fetch_latest_story():
    profile = instaloader.Profile.from_username(L.context, instagram_account)
    stories = L.get_stories(userids=[profile.userid])
    for story in stories:
        for item in story.get_items():
            return item.shortcode, item.url, item.caption
    return None, None, None