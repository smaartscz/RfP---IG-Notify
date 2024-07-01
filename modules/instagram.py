import instaloader, time
import modules.configuration as configuration
import modules.colors as colors
import modules.docker_handler as docker

configuration.load()

instagram_account = configuration.get_value("Instagram", "account")
instagram_username = configuration.get_value("Instagram", "username")
instagram_password = configuration.get_value("Instagram", "password")
fails = configuration.get_value("General", "max_fails")

L = instaloader.Instaloader(iphone_support=False, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
try:
    L.login(instagram_username, instagram_password)
except instaloader.BadCredentialsException:
    print(colors.red + f"Login failed. Looks like Instagram flagged this account :(. Let's sleep for 30min." + colors.reset) 
        
    #Check if we failed 3 times, when True shutdown this container.
    if fails == 3:
        docker.shutdown_container()
    fails = fails + 1
    time.sleep(1800) #Wait for a 30min.
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