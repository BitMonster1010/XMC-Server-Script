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


def xmc_print(message, is_error=False):
    message = ("{0}" + message).format(error_prefix if is_error else prefix)
    print(message)
    add_to_log(message)
    return message


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


def is_screen_running(name):
    var = check_output(["screen -ls; true"], shell=True)
    return bytes("." + name + "\t(", 'UTF-8') in var

def replace_char(str_, replaced_char, replace_with):
    for letter in str_:
        if letter == replaced_char:
            str_ = str_.replace(replaced_char, replace_with)
    return str_