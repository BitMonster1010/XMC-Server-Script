import os
import random
import sys
import time
import utility, config

from console import Console


class ServerController:
    def __init__(self):
        self.__console = Console()
        self.worlds = config.worlds
        self.screen_running = utility.is_screen_running(config.screen)
        os.chdir("../")

    def backup(self, special_name):
        free_bytes = utility.get_number_of_free_bytes()
        dir_size = 0
        for x in range(len(self.worlds)):
            dir_size += utility.get_directory_size(os.getcwd() + "/" + self.worlds[x])
        if free_bytes >= dir_size + 2147483648:
            if special_name == "normal":
                self.__console.announce("&6Backing up worlds")
            else:
                self.__console.announce("&6Backing up worlds as a '" + special_name + "' backup")
            self.__console.announce("&6Saving the world...")
            self.__console.save_all()
            if not os.path.exists("backups"):
                utility.run_command("mkdir backups")
            if not os.path.exists("backups/" + special_name):
                utility.run_command("mkdir backups/" + special_name)

            folder_str = "backups/" + special_name + "/"
            time_str = time.strftime("%d-%m-%Y_%H-%M")
            backup_name = "backup-" + time_str + ".tar"

            if config.multiworld_support:

                utility.run_command("tar -cvf " + folder_str + backup_name + " " + self.worlds[0])
                if len(self.worlds) > 1:
                    for x in range(1, len(self.worlds)):
                        utility.run_command("tar -uvf " + folder_str + backup_name + " " + self.worlds[x])
                time.sleep(0.75)
                utility.run_command("gzip " + folder_str + backup_name)
            else:
                utility.run_command("tar -zcvf " + folder_str + backup_name + " " + self.worlds[0])

            self.__console.announce("&6Finished the backup!")
        else:
            utility.xmc_print("XMC ERR: Not enough space left on the device")
            utility.xmc_print("XMC: Aborting backup")
            sys.exit()

    def stop(self, time_to_stop):
        time_left = time_to_stop
        self.__console.announce("&7Stopping server in " + str(time_to_stop) + " seconds...")
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
                if time_left > 1:
                    self.__console.announce("&7Stopping server in " + str(time_left) + " seconds...")
                else:
                    self.__console.announce("&7Stopping server in " + str(time_left) + " second...")

        self.__console.save_all()
        self.__console.stop()

        utility.xmc_print("XMC: Server was stopped")

    def restart(self, time_to_restart):
        self.__console.announce("&7Server is restarting")
        self.stop(time_to_restart)
        self.start()

    def start(self):
        utility.run_command("screen -dmS " + config.screen + " " + config.start_server_command)
        self.screen_running = utility.is_screen_running(config.screen)
        if self.screen_running:
            utility.xmc_print("XMC: Server was started")
        else:
            utility.xmc_print("XMC ERR: Failed to start server")

    def announce(self, message):
        if message == "random_message":
            self.__console.announce("&d" + config.messages[random.randint(0, len(
                config.messages) - 1)])
        else:
            self.__console.announce("&d" + message)

    def restore(self, path):
        if path[-7:] != ".tar.gz":
            path += ".tar.gz"

        if path[:8] != "backups/":
            path = "backups/" + path

        if os.path.exists(path):
            if self.screen_running:
                self.__console.announce("&6Restoring backup")
                time.sleep(2)
                self.__console.stop()

            utility.run_command("tar -tf " + path + " --exclude '*/*' > archive-check.tmp")

            f = open("archive-check.tmp", "r")
            archived_files = f.readlines()
            f.close()

            utility.run_command("rm archive-check.tmp")

            for x in range(len(archived_files)):
                if os.path.exists(archived_files[x][:-2]):
                    utility.run_command("rm -vr " + archived_files[x][:-2])

            if config.multiworld_support:
                utility.run_command("tar -zxvf " + path)
            else:
                archived_files[0] = archived_files[0][:-2]

                archived_name_different = False
                if archived_files[0] != self.worlds[0]:
                    archived_name_different = True

                utility.run_command("tar -zxvf " + path)

                if archived_name_different:
                    utility.run_command("mv -vT \"" + archived_files[0] + "\" \"" + self.worlds[0] + "\"")

            time.sleep(1)
            self.start()
        else:
            utility.xmc_print("XMC ERR: Backup file doesn't exist")

    def update(self):
        utility.xmc_print("Please note that the updates use BuildTools.jar and only contains CraftBukkit and Spigot")
        utility.xmc_print("Make sure you have set the right server tool in xmc_config.cfg")
        utility.xmc_print("Server tool found in the config file: " + config.server_tool)
        utility.xmc_print("Are you sure you want to continue? (y/dev/n)")
        response = input()
        utility.xmc_print("Response: " + response)
        if response == "y" or response == "dev":
            devBuild = False;
            if response == "dev":
                devBuild = True;
            utility.xmc_print("Starting update process...")
            self.__console.announce("&6Downloading server updates")
            if not os.path.exists("BuildTools/BuildTools.jar"):
                download_link = "\"https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar\""
                utility.run_command("wget " + download_link + " -O BuildTools.jar")
                utility.run_command("mkdir BuildTools")
                utility.run_command("mv BuildTools.jar BuildTools/BuildTools.jar")
            if devBuild:
                self.__console.announce("&6Downloading development build")
                utility.run_command("java -jar BuildTools/BuildTools.jar --dev")
            else:
                utility.run_command("java -jar BuildTools/BuildTools.jar")

            self.__console.announce("&6Updating server")
            time.sleep(2)
            self.__console.save_all()
            self.__console.stop()
            time.sleep(1.5)
            utility.run_command("rm " + config.server_jar_name)

            utility.run_command("ls *.jar > jar-check.tmp")

            f = open("jar-check.tmp", "r")
            jar = f.readlines()
            f.close()

            utility.run_command("rm jar-check.tmp")

            if config.server_tool == "craftbukkit":
                for x in range(len(jar)):
                    if jar[x][:11] == "craftbukkit":
                        filepath = jar[x][:-1]
                        break
            elif config.server_tool == "spigot":
                for x in range(len(jar)):
                    if jar[x][:6] == "spigot":
                        filepath = jar[x][:-1]
                        break

            utility.run_command("mv -f " + filepath + " " + config.server_jar_name)

            self.start()
        else:
            sys.exit()
