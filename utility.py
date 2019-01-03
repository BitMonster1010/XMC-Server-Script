import os
import time
from subprocess import check_output
from subprocess import getoutput

prefix = "XMC:"
error_prefix = "XMC ERR:"
initial_time_stamp = time.strftime("%Y-%m-%d_%H:%M:%S")


def run_command(command):
    output = getoutput(command)
    if output != "":
        print(output)
    add_to_log(output)


def xmc_print(message, is_error=False):
    message = "{0} {1}".format(error_prefix if is_error else prefix, message)
    print(message)
    add_to_log(message)
    return message


def add_to_log(message):
    time_stamp = time.strftime("%Y-%m-%d_%H:%M:%S")
    if not os.path.exists("xmc/logs"):
        os.system("mkdir xmc/logs")
    if message != "":
        f = open("xmc/logs/xmc-{0}.log".format(initial_time_stamp), 'a+')
        if f.tell() == 0:
            f.write("====================================XMC LOG START===========================\n")
        f.write("[{0}]: {1}\n".format(time_stamp, message))
        f.close()


def is_screen_running(name):
    var = check_output(["screen -ls; true"], shell=True)
    return bytes(".{0}\t(".format(name), 'UTF-8') in var


def replace_char(str_, replaced_char, replace_with):
    for letter in str_:
        if letter == replaced_char:
            str_ = str_.replace(replaced_char, replace_with)
    return str_
