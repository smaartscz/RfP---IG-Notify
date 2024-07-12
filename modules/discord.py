from discord_webhook import DiscordWebhook, DiscordEmbed
import modules.configuration as configuration
import modules.colors as colors

def send_webhook(name="None", type="None", ig_id="None", caption="None", url="None", embed_color="None"):
    role = configuration.get_value("General", "role_id")
    webhook_url = configuration.get_value("General", "webhook")
    type = type.lower()

    #Create new instance
    webhook = DiscordWebhook(url=webhook_url, content=f'<@&{role}>')

    #Configure message
    if type == "post":
        embed = DiscordEmbed(title=f'Nový Instagram Post', description=f'{caption}', color=embed_color, rate_limit_retry=True)
    elif type == "story":
        embed = DiscordEmbed(title=f'Nová Instagram Story', color=embed_color, rate_limit_retry=True)
    elif type == "error":
        embed = DiscordEmbed(title=f'Někde nastala chyba', description=f'{caption}', color=embed_color, rate_limit_retry=True)
    else:
        print(colors.red + "Error sending webhook!" + colors.reset)
    if url !="None":
        embed.set_image(url=url)
    embed.set_footer(f"Doufám, že tohle nebyl zbytečnej ping.\nInstagram ID: {ig_id}")

    #Add it to message
    webhook.add_embed(embed)

    #Send webhook
    response = webhook.execute()
    print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)