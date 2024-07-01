from configparser import ConfigParser
from modules.f_time import get_time
import modules.colors as colors
config = ConfigParser()


#Create config
def create():
    config.read("config.cfg")

    print(colors.green + "Sup, now we will setup your Discord integration." + colors.reset)
    webhook_url = input(colors. yellow + "Webhook URL: " + colors.reset)
    ping_role = input(colors.yellow + "Ping role: " + colors.reset)

    print(colors.green + "Now let's get to Instagram" + colors.reset)
    ig_account = input(colors.yellow + "Monitor this Instagram account: " + colors.reset)

    print(colors.yellow + f"Now I will ask about your login credintials. These credentials will be saved {colors.red}UNENCRYPTED{colors.reset} and only on {colors.red}YOUR{colors.reset} machine." + colors.reset)
    ig_username = input(colors.yellow + "Instagram account username: " + colors.reset)
    ig_password = input(colors.yellow + "Instagram account password: " + colors.reset)
    max_fails = input(colors.yellow + "How many fails we can accept before terminating this script(3): " + colors.reset) or 3

    print(colors.green + "Cool, now I will save it to config.cfg" + colors.reset)

    #Add basic information
    config.add_section("General")
    config.set("General", "created", get_time())
    config.set("General", "modified", get_time())
    
    config.set("General", "name", "General")

    config.set("General", "webhook", webhook_url)
    config.set("General", "role_id", ping_role)

    config.set("General", "max_fails", max_fails)

    config.add_section("Instagram")
    config.set("Instagram", "account", ig_account)
    config.set("Instagram", "username", ig_username)
    config.set("Instagram", "password", ig_password)

    #Save config
    with open("config.cfg", "w") as f:
        config.write(f)
    
    print(colors.green + "Config successfully generated!" + colors.reset)


def load():
    config.read("config.cfg")
    content = {}
    for section in config.sections():
        content[section] = dict(config.items(section))
    print(colors.green + "Config loaded successfully!" + colors.reset)
    return content

def save(section, key, value):
    print(colors.yellow + "Saving config!" + colors.reset)
    config.read("config.cfg")
    section_name = section.replace(" ","_")
    try:
        config.set(section_name, "modified", get_time())
        config.set(section_name, key, value)
        with open("config.cfg", "w") as f:
          config.write(f)
    except:
        config.add_section(section_name)
        config.set(section_name, "created", get_time())
        config.set(section_name, "modified", get_time())
        config.set(section_name, "has_finished", "False")
        config.set(section_name, "name", section)
        config.set(section_name, key, value)
        with open("config.cfg", "w") as f:
            config.write(f)   
    print(colors.green + "Config saved!" + colors.reset) 

def modify(action, section, key="", value=""):
    config.read("config.cfg")
    action = action.lower()
    
    #Delete section
    if action == "2":
        print(f"Removing section: {section}")
        config.remove_section(section)
    else:
        print(f"Modifing section: {section}, key: {key}, value: {value}")
        save(section, key, value)

    #Save file
    with open("config.cfg", "w") as f:
        config.write(f)
    print("Section removed!")

def get_section():
    sections = "\n"
    for section in config:
        if section != "DEFAULT":
            sections += section + "\n"
    return sections

def get_key(section):
    keys = "\n"
    for key in config[section]:
        keys += key + "\n"
    return keys

def get_value(section, key):
    value = config[section][key]
    return value