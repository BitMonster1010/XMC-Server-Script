import utility, config


class Console:
    def send_command(self, comm):
        """
        Executes a command in the console.
        """
        utility.run_command("screen -x " + config.screen + " -X stuff \"" + comm + " $(printf '\r')\"")

    def say(self, message):
        self.send_command("say " + message)

    def broadcast(self, message):
        self.send_command("broadcast " + message)

    def announce(self, message):
        if config.use_broadcast:
            self.broadcast(message)
        else:
            self.say(message[2:])

    def save_all(self):
        self.send_command("save-all")

    def stop(self):
        self.send_command("stop")
