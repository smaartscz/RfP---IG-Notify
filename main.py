import modules.configuration as configuration
import modules.instagram as instagram
import modules.webhook as webhook
import modules.colors as colors
import os, time, sys
import modules.docker_handler as docker


if os.name != "nt":
     os.environ.get("TERM")

if not os.path.isfile("config.cfg"):
     print(colors.red + "Running for first time! Creating new config" + colors.reset)
     configuration.create()

if len(sys.argv) > 1:
     print("Argument detected!")
     arg = sys.argv[1].lower()
     if arg == "modify":
          configuration.modify()
     else:
          print(f"Unknown argument! Got {arg}. Continuing as usual.")

print(colors.yellow + "Loading configuration!" + colors.reset)
config = configuration.load()     

print(colors.green + "Startup successful!" + colors.reset)

latest_post_id = configuration.get_value("Instagram", "latest_post_id")
latest_story_id = configuration.get_value("Instagram", "latest_story_id")


while True:
     try:
          post_id, post_url, post_caption = instagram.fetch_latest_post()
          if post_id != latest_post_id:
               latest_post_id = post_id
               configuration.save("Instagram", "latest_post_id", str(latest_post_id))
               print(colors.yellow + "Got new post!" + colors.reset)
          webhook.send_webhook(name="Rock for People 2025 - Post", type="Post", ig_id=post_id, caption=post_caption, url=post_url,embed_color="ffA500")

          story_id, story_url, story_caption = instagram.fetch_latest_story()
          if story_id != latest_story_id and story_id != None:
               latest_story_id = story_id
               configuration.save("Instagram", "latest_story_id", str(latest_story_id))
               print(colors.yellow + "Got new story!" + colors.reset)
               webhook.send_webhook(name="Rock for People 2025 - Story", type="Story",ig_id=story_id, caption=story_caption, url=story_url,embed_color="ffA500")

          # Check for new posts and stories every 10 minutes
          time.sleep(600)

     except Exception as e:
          print(colors.red + f"An unexpected error occurred: {e}" + colors.reset)
          docker.shutdown_container()
        