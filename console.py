import utility, config


class Console:
    def __init__(self, screen, use_broadcast):
        self.__screen = screen
        self.__use_broadcast = use_broadcast

    def send_command(self, comm):
        """
        Executes a command in the console.
        """
        utility.run_command("screen -x {0} -X stuff \"{1} $(printf '\r')\"".format(self.__screen, comm))

    def say(self, message):
        self.send_command("say {0}".format(message))

    def broadcast(self, message):
        self.send_command("broadcast {0}".format(message))

    def announce(self, message):
        if self.__use_broadcast:
            self.broadcast(message)
        else:
            self.say(message)

    def save_all(self):
        self.send_command("save-all")

    def stop(self):
        self.send_command("stop")
