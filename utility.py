import os
import time
from subprocess import check_output
from subprocess import getoutput

prefix = "XMC: "
error_prefix = "XMC ERR: "
initial_time_stamp = time.strftime("%d-%m-%Y_%H:%M:%S")


def run_command(command):
    output = getoutput(command)
    if output != "":
        print(output)
    add_to_log(output)


def xmc_print(message):
    print(message)
    add_to_log(message)


def add_to_log(message):
    time_stamp = time.strftime("%d-%m-%Y_%H:%M:%S")
    if not os.path.exists("xmc_server_script/logs"):
        os.system("mkdir xmc_server_script/logs")
    if message != "":
        f = open("xmc_server_script/logs/xmclog-" + initial_time_stamp + ".log", 'a+')
        if f.tell() == 0:
            f.write("====================================XMC LOG START===========================\n")
        f.write("[" + time_stamp + "]: " + message + "\n")
        f.close()


def get_directory_size(path):
    total_size = 0
    seen = set()

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)

            try:
                stat = os.stat(fp)
            except OSError:
                continue

            if stat.st_ino in seen:
                continue

            seen.add(stat.st_ino)

            total_size += stat.st_size

    return total_size


def get_number_of_free_bytes():
    statvfs = os.statvfs("/")
    return statvfs.f_frsize * statvfs.f_bavail


def is_screen_running(name):
    var = check_output(["screen -ls; true"], shell=True)
    return bytes("." + name + "\t(", 'UTF-8') in var