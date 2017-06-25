#!/usr/bin/env python3

import getopt
import sys, os
import utility, config

os.chdir(sys.path[0])
os.chdir("../")

from server_control import ServerController
from subprocess import getoutput

VERSION = "v1.5"
RELEASE_DATE = "22-06-2017"
AUTHOR = "XxMoNsTeR"


def needs_config(opt):
    return opt in ("-a", "--announce", "-b", "--backup", "-R", "--restore", "-r",
                   "--restart", "-S", "--start", "-s", "--stop", "-U", "--update",
                   "-c", "--check_config", "-e", "--check_server")

def usage():
    print("--------------------------------------------------------------")
    print("Usage:                                                        ")
    print("       -a, --announce [message]                               ")
    print("           Announce a message or type nothing to make         ")
    print("           it announce a random message from config           ")
    print("       -b, --backup [backup_name]                             ")
    print("           Backup the world file                              ")
    print("       -c, --check_config                                     ")
    print("           Checks if data is correct in the config file       ")
    print("       -e --check_server                                      ")
    print("           Shows the last 20 lines of the console output if   ")
    print("           the server is running                              ")
    print("       -g, --generate_config                                  ")
    print("           Generate a new config file (overwrites old one)    ")
    print("       -h, --help                                             ")
    print("           Shows this usage message                           ")
    print("       -R, --restore {backup_path}                            ")
    print("           Restores a specific backup                         ")
    print("       -r, --restart [restart_time]                           ")
    print("           Restart the server                                 ")
    print("       -S, --start                                            ")
    print("           Start the server                                   ")
    print("       -s, --stop [stop_time]                                 ")
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
        opts, args = getopt.getopt(argv, "hSUegcvbR:rsa", ["help", "start", "update", "check_server", "generate_config", "check_config", "version", "backup", "restore=", "restart", "stop", "announce"])
    except getopt.GetoptError:
        utility.xmc_print("Invalid argument", True)
        utility.xmc_print("Please use -h or --help for usage")
        sys.exit()
    for opt, arg in opts:
        try:
            screen_running = server_controller.screen_running
            args = ' '.join(args)
            if opt in ("-b", "--backup"):
                if screen_running:
                    if args == '':
                        server_controller.backup()
                    else:
                        server_controller.backup(args)
                else:
                    utility.xmc_print("Server is not started", True)
            elif opt in ("-S", "--start"):
                if not screen_running:
                    server_controller.start()
                else:
                    utility.xmc_print("Server is already started", True)
            elif opt in ("-r", "--restart"):
                if screen_running:
                    server_controller.restart(0 if args == '' else int(args))
                else:
                    server_controller.start(0 if args == '' else int(args))
            elif opt in ("-s", "--stop"):
                if screen_running:
                    server_controller.stop(0 )
                else:
                    utility.xmc_print("Server is already stopped", True)
            elif opt in ("-a", "--announce"):
                if screen_running:
                    server_controller.announce(args)
                else:
                    utility.xmc_print("Server is not started", True)
            elif opt in ("-c", "--check_config"):
                print("Worlds: ")
                for world in server_controller.config.worlds:
                    print("   " + world)
                print("Screen: " + server_controller.config.screen)
                print("Start Server Command: " + server_controller.config.start_server_command)
                print("Use Broadcast: " + str(server_controller.config.use_broadcast))
                print("Multiworld Support: " + str(server_controller.config.multiworld_support))
                print("Messages: ")
                for message in server_controller.config.messages:
                    print("   " + message)
                print("Server Tool: " + server_controller.config.server_tool)
                print("Server Jar Name: " + server_controller.config.server_jar_name)
            elif opt in ("-R", "--restore"):
                server_controller.restore(arg)
            elif opt in ("-U", "--update"):
                server_controller.update()
            elif opt in ("-e", "--check_server"):
                if screen_running:
                    utility.xmc_print("Server is running")
                    utility.xmc_print("Here are the last 20 lines of the Console Output:")
                    utility.xmc_print(getoutput("tail -20 screenlog.0"))
                else:
                    utility.xmc_print("Server is not running")
        except config.ConfigException as e:
            utility.xmc_print(e)

        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-v", "--version"):
            print("XMC Server Script " + VERSION)
            print("Release Date: " + RELEASE_DATE)
            print("Author: " + AUTHOR)
        elif opt in ("-g", "--generate_config"):
            server_controller.config.generate_config(config.ConfigDefaults.config_file)


if __name__ == "__main__":
   main(sys.argv[1:])


