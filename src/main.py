from dotenv import dotenv_values
import utils
from linux import LinuxHealth
import time

env = dotenv_values(".env")

INTERVAL_CHECKING = utils.extractTime(env["INTERVAL_CHECKING"]).total_seconds()
LOG_PATH = env["LOG_PATH"]
MAX_USED = 90


def main():
    logger = utils.Logger(LOG_PATH)
    linuxHealth = LinuxHealth()
    mail = utils.Mail(env["MAIL"], env["MAIL_PASSWORD"])
    mail.login()

    while True:
        health = linuxHealth.checkHealth()
        log = health["log"]
        cpuUsed = health["cpu"]
        ramUsed = health["ram"][1]

        if cpuUsed > MAX_USED or ramUsed > MAX_USED:
            mail.sendToMe(
                "Warning! Your linux OS is overloading. CPU:{}%, RAM:{}%".format(
                    cpuUsed, ramUsed
                )
            )

        logger.write(log)
        print("LOG:::", log)
        time.sleep(INTERVAL_CHECKING)


main()
