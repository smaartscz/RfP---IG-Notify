import instaloader, time
import modules.configuration as configuration
import modules.colors as colors
import modules.docker_handler as docker

configuration.load()

instagram_account = configuration.get_value("Instagram", "account")
instagram_username = configuration.get_value("Instagram", "username")
instagram_password = configuration.get_value("Instagram", "password")

max_fails = int(configuration.get_value("General", "max_fails"))
fails = 0

L = instaloader.Instaloader(iphone_support=False,save_metadata=False,fatal_status_codes=False, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
profile = None

try:
    L.login(instagram_username, instagram_password)
except instaloader.BadCredentialsException:
    print(colors.red + f"Login failed. Looks like Instagram flagged this account :(. Let's sleep for 30min." + colors.reset) 
    #Check if we failed 3 times, when True shutdown this container.
    if fails == max_fails:
        docker.shutdown_container(error="Login failed. Looks like Instagram flagged this account :(")
    else:
        fails = fails + 1
        time.sleep(1800) #Wait for a 30min.
        L.login(instagram_username, instagram_password)

def fetch_latest_post():
    global profile
    posts = list(profile.get_posts())
    if posts:
        latest_post = posts[0]
        return latest_post.shortcode, latest_post.url, latest_post.caption
    return None, None, None

# Function to fetch the latest story
def fetch_latest_story():
    global profile
    stories = L.get_stories(userids=[profile.userid])
    for story in stories:
        for item in story.get_items():
            return item.shortcode, item.url, item.caption
    return None, None, None

def update_profile():
    global profile
    print(colors.yellow + "Updating profile" + colors.reset)
    profile = instaloader.Profile.from_username(L.context, instagram_account)
    print(colors.green + "Profile updated!" + colors.reset)