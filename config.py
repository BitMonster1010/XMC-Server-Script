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
    backup_folder = "backups"
    sort_backups = True

    l_datetime_format = "%Y-%m-%d_%H-%M"
    l_backup = "&6Backing up worlds"
    l_backup_as = "&6Backing up worlds as a '{0}' backup"
    l_saving_world = "&6Saving the world"
    l_backup_finished = "&6Finished the backup!"
    l_restart = "&7Sever is restarting"
    l_stopping = "&7Stopping server in {0} second{1}"
    l_restoring_backup = "&6Restoring backup"
    l_downloading_updates = "&6Downloading server updates"
    l_downloading_development_version = "&6Downloading development version"
    l_downloading_version_with_revision = "&6Downloading version with revision '{0}'"
    l_updating = "&6Updating server"

    config_file = "xmc/xmc_config.cfg"


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
            self.backup_folder = c.get('data', 'backup_folder', fallback=ConfigDefaults.backup_folder)
            self.sort_backups = c.get('data', 'sort_backups', fallback=ConfigDefaults.sort_backups)

            self.l_datetime_format = c.get('localization', 'datetime_format', fallback=ConfigDefaults.l_datetime_format)
            self.l_backup = c.get('localization', 'backup', fallback=ConfigDefaults.l_backup)
            self.l_backup_as = c.get('localization', 'backup_as', fallback=ConfigDefaults.l_backup_as)
            self.l_saving_world = c.get('localization', 'saving_world', fallback=ConfigDefaults.l_saving_world)
            self.l_backup_finished = c.get('localization', 'backup_finished', fallback=ConfigDefaults.l_backup_finished)
            self.l_restart = c.get('localization', 'restart', fallback=ConfigDefaults.l_restart)
            self.l_stopping = c.get('localization', 'stopping', fallback=ConfigDefaults.l_stopping)
            self.l_restoring_backup = c.get('localization', 'restoring_backup', fallback=ConfigDefaults.l_restoring_backup)
            self.l_downloading_updates = c.get('localization', 'downloading_updates', fallback=ConfigDefaults.l_downloading_updates)
            self.l_downloading_development_version = c.get('localization', 'downloading_development_version',
                                                           fallback=ConfigDefaults.l_downloading_development_version)
            self.l_downloading_version_with_revision = c.get('localization', 'downloading_version_with_revision',
                                                             fallback=ConfigDefaults.l_downloading_version_with_revision)
            self.l_updating = c.get('localization', 'updating', fallback=ConfigDefaults.l_updating)

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
                 "worlds = {0}\n".format(utility.replace_char(str(ConfigDefaults.worlds), "'", "\"")),
                 "screen = {0}\n".format(ConfigDefaults.screen),
                 "start_server_command = {0}\n".format(ConfigDefaults.start_server_command),
                 "use_broadcast = {0}\n".format(str(ConfigDefaults.use_broadcast)),
                 "multiworld_support = {0}\n".format(str(ConfigDefaults.multiworld_support)),
                 "announce_messages = {0}\n".format(utility.replace_char(str(ConfigDefaults.messages), "'", "\"")),
                 "server_tool = {0}\n".format(ConfigDefaults.server_tool),
                 "server_jar_name = {0}\n".format(ConfigDefaults.server_jar_name),
                 "backup_folders = {0}\n".format(ConfigDefaults.backup_folder),
                 "sort_backups = {0}\n\n".format(ConfigDefaults.sort_backups),
                 "#Available options for 'server_tool' are 'craftbukkit' and 'spigot'\n",
                 "#Please use consistent names for your server jar file, otherwise the update script might not work properly\n\n",
                 "[localization]\n",
                 "datetime_format = {0}\n".format(ConfigDefaults.l_datetime_format),
                 "backup = {0}\n".format(ConfigDefaults.l_backup),
                 "backup_as = {0}\n".format(ConfigDefaults.l_backup_as),
                 "#{0} - Backup name\n",
                 "saving_world = {0}\n".format(ConfigDefaults.l_saving_world),
                 "backup_finished = {0}\n".format(ConfigDefaults.l_backup_finished),
                 "restart = {0}\n".format(ConfigDefaults.l_restart),
                 "stopping = {0}\n".format(ConfigDefaults.l_stopping),
                 "{0} - Number of seconds left until stopping the server\n",
                 "{1} - Plural for seconds, if there is more than 1 second it will be 's'\n",
                 "restoring_backup = {0}\n".format(ConfigDefaults.l_restoring_backup),
                 "downloading_updates = {0}\n".format(ConfigDefaults.l_downloading_updates),
                 "downloading_development_version = {0}\n".format(ConfigDefaults.l_downloading_development_version),
                 "downloading_version_with_revision = {0}\n".format(ConfigDefaults.l_downloading_version_with_revision),
                 "{0} - The specified revision to download given by the user through special arguments\n",
                 "updating = {0}\n".format(ConfigDefaults.l_updating)]
            )
            f.close()
            utility.xmc_print("New config file has been generated")
            self.__init__()
        except:
            raise ConfigException("Failed to generate new config file")
