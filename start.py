#!/usr/bin/env python3

import getopt
import sys
import utility, config

sys.path.append("../")

from server_control import ServerController

version = "v1.4"
release_date = "29-04-2017"

prefix = "XMC: "
error_prefix = "XMC ERR: "


def needs_config(opt):
    return opt in ("-a", "--announce", "-b", "--backup", "-R", "--restore", "-r", "--restart", "-S", "--start", "-s", "--stop", "-U", "--update", "-c", "--check_config")

def usage():
    print("--------------------------------------------------------------")
    print("Usage:                                                        ")
    print("       -a, --announce {random_message or `proper message`}    ")
    print("           Announce a message                                 ")
    print("       -b, --backup {backup_name}                             ")
    print("           Backup the world file                              ")
    print("       -c, --check_config                                     ")
    print("           Checks if data is correct in the config file       ")
    print("       -g, --generate_config                                  ")
    print("           Generate a new config file (overwrites old one)    ")
    print("       -h, --help                                             ")
    print("           Shows this usage message                           ")
    print("       -R, --restore {full_backup_path}                       ")
    print("           Restores a specific backup                         ")
    print("       -r, --restart {restart_time}                           ")
    print("           Restart the server                                 ")
    print("       -S, --start                                            ")
    print("           Start the server                                   ")
    print("       -s, --stop {stop_time}                                 ")
    print("           Stop the server                                    ")
    print("       -U, --update                                           ")
    print("           Updates the server                                 ")
    print("       -v, --version                                          ")
    print("           Shows the version of the script                    ")
    print("--------------------------------------------------------------")
    sys.exit()


def main(argv):
    server_controller = ServerController()

    try:
        opts, args = getopt.getopt(argv, "hSUgcvb:R:r:s:a:", ["help", "start", "generate_config", "check_config", "version", "update", "backup=", "restore=", "restart=", "stop=", "announce="])
    except getopt.GetoptError:
        utility.xmc_print(error_prefix + "Invalid argument")
        utility.xmc_print(prefix + "Please use -h or --help for usage")
        sys.exit()
    for opt, arg in opts:
        if needs_config(opt):
            config.load_config()
            server_controller.worlds = config.worlds
            screen_running = utility.is_screen_running(config.screen)
            server_controller.screen_running = screen_running

            if opt in ("-b", "--backup"):
                if screen_running:
                    server_controller.backup(arg)
                else:
                    utility.xmc_print(error_prefix + "Server is not started")
            elif opt in ("-S", "--start"):
                if not screen_running:
                    server_controller.start()
                else:
                    utility.xmc_print(error_prefix + "Server is already started")
            elif opt in ("-r", "--restart"):
                if screen_running:
                    server_controller.restart(int(arg))
                else:
                    server_controller.start()
            elif opt in ("-s", "--stop"):
                if screen_running:
                    server_controller.stop(int(arg))
                else:
                    utility.xmc_print(error_prefix + "Server is already stopped")
            elif opt in ("-a", "--announce"):
                if screen_running:
                    server_controller.announce(arg)
                else:
                    utility.xmc_print(error_prefix + "Server is not started")
            elif opt in ("-c", "--check_config"):
                print("Worlds: ")
                for x in range(len(config.worlds)):
                    print("   " + config.worlds[x])
                print("Screen: " + config.screen)
                print("Start Server Command: " + config.start_server_command)
                print("Use Broadcast: " + str(config.use_broadcast))
                print("Multiworld Support: " + str(config.multiworld_support))
                print("Messages: ")
                for x in range(len(config.messages)):
                    print("   " + config.messages[x])
                print("Server Tool: " + config.server_tool)
                print("Server Jar Name: " + config.server_jar_name)
            elif opt in ("-R", "--restore"):
                server_controller.restore(arg)
            elif opt in ("-U", "--update"):
                server_controller.update()
        else:
            if opt in ("-h", "--help"):
                usage()
            elif opt in ("-v", "--version"):
                print("XMC Server Script " + version)
                print("Release Date: " + release_date)
                print("Author: XxMoNsTeR")
            elif opt in ("-g", "--generate_config"):
                config.generate_config()


if __name__ == "__main__":
   main(sys.argv[1:])


