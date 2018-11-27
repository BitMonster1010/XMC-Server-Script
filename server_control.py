import os
import random
import sys
import time
import utility

from config import Config, ConfigDefaults
from console import Console
from subprocess import getoutput


class ServerController:
    def __init__(self):
        self.config = Config()
        self.__console = Console(self.config.screen, self.config.use_broadcast)
        self.screen_running = utility.is_screen_running(self.config.screen)

    def backup(self, special_name="normal", include_announce=True):
        try:
            utility.xmc_print("Backing up worlds")
            if include_announce:
                if special_name == "normal":
                    self.__console.announce("&6Backing up worlds")
                else:
                    self.__console.announce("&6Backing up worlds as a '{0}' backup".format(special_name))
                self.__console.announce("&6Saving the world...")
            self.__console.save_all()
            if not os.path.exists("backups"):
                utility.run_command("mkdir backups")
            if not os.path.exists("backups/{0}".format(special_name)):
                utility.run_command("mkdir backups/{0}".format(special_name))

            folder_str = "backups/{0}/".format(special_name)
            time_str = time.strftime(self.config.datetime_format)
            backup_name = "backup-{0}.tar".format(time_str)

            if self.config.multiworld_support:

                utility.run_command("tar -cvf {0}{1} {2}".format(folder_str, backup_name, self.config.worlds[0]))
                if len(self.config.worlds) > 1:
                    for x in range(1, len(self.config.worlds)):
                        utility.run_command("tar -uvf {0}{1} {2}".format(folder_str, backup_name, self.config.worlds[x]))
                time.sleep(0.75)
                utility.run_command("gzip {0}{1}".format(folder_str, backup_name))
            else:
                utility.run_command("tar -zcvf {0}{1] {2}".format(folder_str, backup_name, self.config.worlds[0]))

            if include_announce:
                self.__console.announce("&6Finished the backup!")
            utility.xmc_print("Successfully backed up worlds!")
            utility.xmc_print("The backup restore path is: '{0}{1}.gz'".format(folder_str, backup_name))
        except IOError as e:
            utility.xmc_print("An unexpected I/O error has occured!", True)
            utility.xmc_print(e, True)
            utility.xmc_print("Aborting backup!")
            sys.exit()

    def stop(self, time_to_stop):
        time_left = time_to_stop
        self.__console.announce("&7Stopping server in {0} seconds...".format(str(time_to_stop)))
        for x in range(time_to_stop):
            time.sleep(1)
            time_left -= 1

            show_timer = False

            if time_left == 0:
                break

            if time_left <= 5:
                show_timer = True
            elif time_left == time_to_stop / 2 or time_left == time_to_stop / 4:
                show_timer = True

            if show_timer:
                if time_left != 1:
                    self.__console.announce("&7Stopping server in {0} seconds...".format(str(time_left)))
                else:
                    self.__console.announce("&7Stopping server in 1 second...")

        self.__console.save_all()
        self.__console.stop()

        utility.xmc_print("Server was stopped")

    def restart(self, time_to_restart):
        self.__console.announce("&7Server is restarting")
        self.stop(time_to_restart)
        self.start()

    def start(self):
        utility.run_command("screen -L xmc-screen.log -dmS {0} {1}".format(self.config.screen, self.config.start_server_command))
        self.screen_running = utility.is_screen_running(self.config.screen)
        if self.screen_running:
            utility.xmc_print("Server was started")
        else:
            utility.xmc_print("Failed to start server", True)

    def announce(self, message):
        msg = ""
        if message == "":
            msg = self.config.messages[random.randint(0, len(self.config.messages) - 1)]
            self.__console.announce("&d{0}".format(msg))
        else:
            msg = message
            self.__console.announce("&d{0}".format(msg))
        utility.xmc_print("Announced message: '{0}'".format(msg))

    def restore(self, path):
        if path[-7:] != ".tar.gz":
            path += ".tar.gz"

        if path[:8] != "backups/":
            path = "backups/" + path

        if os.path.exists(path):
            utility.xmc_print("A backup is being restored")
            self.backup("pre-restore", False)

            if self.screen_running:
                self.__console.announce("&6Restoring backup")
                time.sleep(2)
                self.__console.stop()

            archived_files = getoutput("tar -tf {0} --exclude '*/*'".format(path)).split("\n")

            for file in archived_files:
                if os.path.exists(file):
                    utility.run_command("rm -vr {0}".format(file[:-2]))

            if self.config.multiworld_support:
                utility.run_command("tar -zxvf {0}".format(path))
            else:
                archived_name_different = False
                if archived_files[0] != self.config.worlds[0]:
                    archived_name_different = True

                utility.run_command("tar -zxvf {0}".format(path))

                if archived_name_different:
                    utility.run_command("mv -vT \"{0}\" \"{1}\"".format(archived_files[0], self.config.worlds[0]))

            time.sleep(1)
            self.start()
        else:
            utility.xmc_print("Backup file doesn't exist", True)

    def update(self):
        utility.xmc_print("Please note that the updates use BuildTools.jar and only contains CraftBukkit and Spigot")
        utility.xmc_print("Make sure you have set the right server tool in xmc_config.cfg")
        utility.xmc_print("Server tool found in the config file: {0}".format(self.config.server_tool))
        utility.xmc_print("Are you sure you want to continue? (y/n)")
        response = input()
        utility.xmc_print("Response: " + response)
        if response == "y":
            utility.xmc_print("Special arguments?")
            special_args = input()
            utility.xmc_print("Response: {0}".format(special_args))
            utility.xmc_print("Starting update process...")
            self.__console.announce("&6Downloading server updates")
            if not os.path.exists("BuildTools/BuildTools.jar"):
                download_link = "\"https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar\""
                utility.run_command("wget {0} -O BuildTools.jar".format(download_link))
                utility.run_command("mkdir BuildTools")
                utility.run_command("mv BuildTools.jar BuildTools/BuildTools.jar")
            if special_args == "--dev":
                self.__console.announce("&6Downloading development version")
            elif special_args[:5] == "--rev":
                more_args = special_args.split()
                self.__console.announce("&6Downloading version with revision '{0}'".format(more_args[1]))
            if special_args == "":
                utility.run_command("java -jar BuildTools/BuildTools.jar")
            else:
                utility.run_command("java -jar BuildTools/BuildTools.jar {0}".format(special_args))

            self.backup("pre-update", False)
            self.__console.announce("&6Updating server")
            time.sleep(2)
            self.__console.save_all()
            self.__console.stop()
            time.sleep(1.5)
            utility.run_command("rm {0}".format(self.config.server_jar_name))

            jar = getoutput("ls *.jar").split("\n")

            if self.config.server_tool == "craftbukkit":
                for j in jar:
                    if j[:11] == "craftbukkit":
                        filepath = j
                        break
            elif self.config.server_tool == "spigot":
                for j in jar:
                    if j[:6] == "spigot":
                        filepath = j
                        break

            utility.run_command("mv -f {0} {1}".format(filepath, self.config.server_jar_name))

            self.start()
        else:
            sys.exit()
