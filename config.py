#Variables that are used in all files are saved in here

import configparser
import utility

worlds = ["world"]
screen = "minecraft_server_xmc"
start_server_command = "java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui"
use_broadcast = False
multiworld_support = False
messages = ["message1", "message2"]
server_tool = "craftbukkit"
server_jar_name = "minecraft_server.jar"


def load_config(filename='xmc_server_script/xmc_config.cfg'):
    try:
        f = open(filename, "r")

        config = configparser.RawConfigParser()
        config.read_file(f)

        global worlds, screen, start_server_command, use_broadcast, multiworld_support, messages, server_tool, server_jar_name
        worlds = config.get('data', 'worlds').split("\n")
        screen = config.get('data', 'screen')
        start_server_command = config.get('data', 'start_server_command')
        use_broadcast = config.getboolean('data', 'use_broadcast')
        multiworld_support = config.getboolean('data', 'multiworld_support')
        messages = config.get('data', 'announce_messages').split("\n")
        server_tool = config.get('data', 'server_tool')
        server_jar_name = config.get('data', 'server_jar_name')

        f.close()

        if server_tool not in ("craftbukkit", "spigot"):
            utility.xmc_print("XMC ERR: Invalid server tool")
            fix_config(filename, 'server_tool')
    except FileNotFoundError:
        utility.xmc_print("XMC ERR: No config file found")
        generate_config(filename)
    except ValueError:
        utility.xmc_print("XMC ERR: Invalid value for 'use_broadcast' in xmc_config.cfg")
        fix_config(filename, 'use_broadcast')
    except (configparser.NoOptionError, configparser.NoSectionError, configparser.MissingSectionHeaderError, configparser.ParsingError):
        utility.xmc_print("XMC ERR: Config file is broken")
        fix_config()


def generate_config(filename='xmc_server_script/xmc_config.cfg'):
    utility.xmc_print("XMC: Generating a new config file")

    try:
        f = open(filename, 'w')

        f.seek(0)
        f.truncate(0)

        f.writelines(
            [ "[data]\n",
                "worlds = " + worlds + "\n",
                "screen = " + screen + "\n",
                "start_server_command = " + start_server_command + "\n",
                "use_broadcast = " + str(use_broadcast) + "\n",
                "multiworld_support = " + str(multiworld_support) + "\n",
                "announce_messages = " + messages[0] + "\n",
                "                    " + messages[1] + "\n",
                "server_tool = " + server_tool + "\n",
                "server_jar_name = " + server_jar_name + "\n",
                "#Available options for 'server_tool' are 'craftbukkit' and 'spigot'\n",
                "#Please use consistent names for your server jar file, otherwise the update script might not work properly\n"]
        )
        f.close()
        utility.xmc_print("XMC: New config file has been generated")
        return True
    except:
        return False


def fix_config(filename='xmc_server_script/xmc_config.cfg', error='broken'):
    utility.xmc_print("XMC: Attempting to fix the config file")

    if error == 'use_broadcast':
        try:
            f = open(filename, 'r+')

            config_file = f.readlines()
            for x in range(len(config_file)):
                if config_file[x].split("=")[0] in ("use_broadcast", "use_broadcast "):
                    config_file[x] = "use_broadcast = False\n"
                    f.seek(0)
                    f.truncate(0)
                    f.writelines(config_file)

            f.close()
            utility.xmc_print("XMC: Fixed the use_broadcast value in config file")
            load_config()
            return True
        except:
            utility.xmc_print("XMC ERR: Unable to fix config file")
            return False
    elif error == "server_tool":
        try:
            f = open(filename, 'r+')

            config_file = f.readlines()
            for x in range(len(config_file)):
                if config_file[x].split("=")[0] in ("server_tool", "server_tool "):
                    config_file[x] = "server_tool = craftbukkit\n"
                    f.seek(0)
                    f.truncate(0)
                    f.writelines(config_file)

            f.close()
            utility.xmc_print("XMC: Fixed the server_tool value in config file")
            load_config()
            return True
        except:
            utility.xmc_print("XMC ERR: Unable to fix config file")
            return False
    else:
        try:
            generate_config(filename)
            load_config()
        except:
            utility.xmc_print("XMC ERR: Unable to fix config file")
            return False

