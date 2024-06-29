import modules.configuration as configuration
import modules.instagram as instagram
import modules.webhook as webhook
import os, time, sys

if os.name != "nt":
     os.environ.get("TERM")

if not os.path.isfile("config.cfg"):
     print("Running for first time! Creating new config")
     configuration.create()

if len(sys.argv) > 1:
     print("Argument detected!")
     arg = sys.argv[1].lower()
     if arg == "modify":
          configuration.modify()
     else:
          print(f"Unknown argument! Got {arg}. Continuing as usual.")

print("Loading configuration!")
config = configuration.load()     

print("Startup successful!")

latest_post_id = None
latest_story_id = None

while True:
    post_id, post_url, post_caption = instagram.fetch_latest_post()
    if post_id != latest_post_id:
        latest_post_id = post_id
        print("Got new post!")
        webhook.send_webhook(id=0,name="Rock for People 2025 - Post", caption=post_caption, url=post_url)

    story_id, story_url, story_caption = instagram.fetch_latest_story()
    if story_id != latest_story_id:
        latest_story_id = story_id
        print("Got new story!")
        webhook.send_webhook(id=0,name="Rock for People 2025 - Story", caption=story_caption, url=story_url)

    # Check for new posts and stories every 10 minutes
    time.sleep(600)