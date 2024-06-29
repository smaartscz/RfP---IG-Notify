from discord_webhook import DiscordWebhook, DiscordEmbed
import modules.configuration as configuration
from modules.f_time import remaining_time

def send_webhook(id, name, ig_id, caption, url, embed_color):
    config = configuration.load()
    #Create new instance
    webhook = DiscordWebhook(url=f'{config["General"]["webhook"]}', content=f'<@&{config[id]["role_id"]}>')

    #Configure message
    embed = DiscordEmbed(title=f'Novej Instagram Post/Story', description=f'Caption: {caption}\n URL: {url}', color=embed_color)
    embed.set_author(name=name) 
    embed.set_footer(f"Doufám, že tohle nebyl zbytečnej ping, Instagram ID: {ig_id}")
    #Add it to message
    webhook.add_embed(embed)

    #Send webhook
    response = webhook.execute()
    print(f"Webhook sent! Response: {response}")