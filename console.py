import utility, config


class Console:
    def __init__(self, screen, use_broadcast):
        self.__screen = screen
        self.__use_broadcast = use_broadcast

    def send_command(self, comm):
        """
        Executes a command in the console.
        """
        utility.run_command("screen -x " + self.__screen + " -X stuff \"" + comm + " $(printf '\r')\"")

    def say(self, message):
        self.send_command("say " + message)

    def broadcast(self, message):
        self.send_command("broadcast " + message)

    def announce(self, message):
        if self.__use_broadcast:
            self.broadcast(message)
        else:
            self.say(message[2:])

    def save_all(self):
        self.send_command("save-all")

    def stop(self):
        self.send_command("stop")
