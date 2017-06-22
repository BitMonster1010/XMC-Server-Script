#Variables that are used in all files are saved in here

import configparser
import json
import utility
import sys


class ConfigException(Exception):
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message


class ConfigDefaults:
    worlds = ["world"]
    screen = "minecraft_server_xmc"
    start_server_command = "java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui"
    use_broadcast = False
    multiworld_support = False
    messages = ["message1", "message2"]
    server_tool = "craftbukkit"
    server_jar_name = "minecraft_server.jar"

    config_file = "xmc_server_script/xmc_config.cfg"


class Config:
    def __init__(self, config_file=ConfigDefaults.config_file):
        try:
            f = open(config_file, "r")

            c = configparser.RawConfigParser()
            c.read_file(f)

            self.worlds = c.get('data', 'worlds', fallback=ConfigDefaults.worlds)
            if str(type(self.worlds)) == "<class 'str'>":
                # Convert the string to a list
                self.worlds = json.loads(self.worlds)
            self.screen = c.get('data', 'screen', fallback=ConfigDefaults.screen)
            self.start_server_command = c.get('data', 'start_server_command', fallback=ConfigDefaults.start_server_command)
            self.use_broadcast = c.getboolean('data', 'use_broadcast', fallback=ConfigDefaults.use_broadcast)
            self.multiworld_support = c.getboolean('data', 'multiworld_support', fallback=ConfigDefaults.multiworld_support)
            self.messages = c.get('data', 'announce_messages', fallback=ConfigDefaults.messages)
            if str(type(self.messages)) == "<class 'str'>":
                self.messages = json.loads(self.messages)
            self.server_tool = c.get('data', 'server_tool', fallback=ConfigDefaults.server_tool)
            self.server_jar_name = c.get('data', 'server_jar_name', fallback=ConfigDefaults.server_jar_name)

            f.close()
        except FileNotFoundError:
            utility.xmc_print("No config file found", True)
            self.generate_config(config_file)
        except ResourceWarning:
            f.close()
        except:
            raise ConfigException("An error has occured while loading the config file")

    def generate_config(self, config_file):
        utility.xmc_print("Generating a new config file")

        try:
            f = open(config_file, 'w')

            f.seek(0)
            f.truncate(0)

            f.writelines(
                ["[data]\n",
                 "worlds = " + utility.replace_char(str(ConfigDefaults.worlds), "'", "\"") + "\n",
                 "screen = " + ConfigDefaults.screen + "\n",
                 "start_server_command = " + ConfigDefaults.start_server_command + "\n",
                 "use_broadcast = " + str(ConfigDefaults.use_broadcast) + "\n",
                 "multiworld_support = " + str(ConfigDefaults.multiworld_support) + "\n",
                 "announce_messages = " + utility.replace_char(str(ConfigDefaults.messages), "'", "\"") + "\n",
                 "server_tool = " + ConfigDefaults.server_tool + "\n",
                 "server_jar_name = " + ConfigDefaults.server_jar_name + "\n\n",
                 "#Available options for 'server_tool' are 'craftbukkit' and 'spigot'\n",
                 "#Please use consistent names for your server jar file, otherwise the update script might not work properly\n"]
            )
            f.close()
            utility.xmc_print("New config file has been generated")
            self.__init__()
        except:
            raise ConfigException("Failed to generate new config file")
