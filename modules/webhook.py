from discord_webhook import DiscordWebhook, DiscordEmbed
import modules.configuration as configuration

def send_webhook(name, type, ig_id, caption, url, embed_color):
    role = configuration.get_value("General", "role_id")
    webhook_url = configuration.get_value("General", "webhook")
    #Create new instance
    webhook = DiscordWebhook(url=webhook_url, content=f'<@&{role}>')

    #Configure message
    if type == "Post":
        embed = DiscordEmbed(title=f'Nový Instagram Post', description=f'Caption: {caption}', color=embed_color, rate_limit_retry=True)
    if type == "Story":
        embed = DiscordEmbed(title=f'Nová Instagram Story', description=f'Caption: {caption}', color=embed_color, rate_limit_retry=True)
    #embed.set_author(name=name) 
    embed.set_image(url=url)
    embed.set_footer(f"Doufám, že tohle nebyl zbytečnej ping.\nInstagram ID: {ig_id}")

    #Add it to message
    webhook.add_embed(embed)

    #Send webhook
    response = webhook.execute()
    print(f"Webhook sent! Response: {response}")