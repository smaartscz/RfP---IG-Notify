from configparser import ConfigParser
from modules.f_time import get_time
config = ConfigParser()


#Create config
def create():
    config.read("config.cfg")

    webhook_url = input("Webhook URL: ")

    #Add basic information
    config.add_section("General")
    config.set("General", "created", get_time())
    config.set("General", "modified", get_time())
    
    config.set("General", "name", "General")

    config.set("General", "webhook", webhook_url)
    config.set("General", "role_id", "1121821428111646864")

    config.add_section("Instagram")
    config.set("Instagram", "account", "smaartscz")

    #Save config
    with open("config.cfg", "w") as f:
        config.write(f)
    
    print("Config successfully generated!")


def load():
    config.read("config.cfg")
    content = {}
    for section in config.sections():
        content[section] = dict(config.items(section))
    print("Config loaded successfully!")
    return content

def save(section, key, value):
    print("Saving config!")
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
    print("Config saved!") 

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