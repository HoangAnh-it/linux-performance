from dotenv import dotenv_values
import psutil
import time
from datetime import timedelta, datetime
from email.message import EmailMessage
import logging
import smtplib
import argparse

env = dotenv_values(".env")

ONE_GIGABYTE = 1073741824


def extractTime(timeString):
    match timeString[-1]:
        case "d":
            time = int(timeString[:-1])
            return timedelta(days=time)

        case "h":
            time = int(timeString[:-1])
            return timedelta(hours=time)

        case "m":
            time = int(timeString[:-1])
            return timedelta(minutes=time)

        case "s":
            time = int(timeString[:-1])
            return timedelta(seconds=time)


def byte_to_gigabyte(byte):
    gb = byte / ONE_GIGABYTE
    return "{:.2f}".format(gb)


class Logger:
    def __init__(self, logPath):
        logging.basicConfig(
            filename=logPath,
            filemode="a",
            level=logging.DEBUG,
            format="%(message)s",
        )
        self.logger = logging

    def write(self, message):
        self.logger.info(message)


class Mail:
    def __init__(self, me, my_password):
        self.__me = me
        self.__my_password = my_password
        self.__server = None

    def login(self):
        try:
            self.__server = smtplib.SMTP_SSL("smtp.gmail.com", smtplib.SMTP_SSL_PORT)
            self.__server.login(self.__me, self.__my_password)

        except Exception as e:
            print("Fail to login mail:::", e)

    def sendToMe(self, message):
        try:
            if not self.__server:
                raise Exception("You must login to mail first")

            msg = EmailMessage()
            msg["Subject"] = "Performance of linux"
            msg["From"] = self.__me
            msg["To"] = self.__me
            msg.set_content(message)
            self.__server.sendmail(self.__me, self.__me, msg.as_string())
        except Exception as e:
            print("Fail to send mail", e)

    def logout(self):
        if self.__server:
            self.__server.quit()


class LinuxHealth:
    formatLog = "{time}: CPU:{cpu}%, RAM:{{{ram}}}%"

    def __init__(self):
        pass

    def checkCPU(self):
        return psutil.cpu_percent()

    def checkRAM(self):
        percent = psutil.virtual_memory().percent
        used = psutil.virtual_memory().used
        total = psutil.virtual_memory().total
        return [used, percent, total]

    def checkDisk():
        pass

    def checkHealth(self):
        cpu = self.checkCPU()
        ram = self.checkRAM()
        log = self.formatLog.format(
            time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            cpu=cpu,
            ram="{} GB ({}%) of {} GB".format(
                byte_to_gigabyte(ram[0]), ram[1], byte_to_gigabyte(ram[2])
            ),
        )

        return {"log": log, "cpu": cpu, "ram": ram}


class LinuxHealthCommand:
    def __init__(self):
        pass

    def setUpArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-lg", "--log", dest="logPath", help="Path of log file")
        parser.add_argument(
            "-i",
            "--interval",
            dest="intervalChecking",
            help="A period of time to check using minutes unit",
            type=int,
            default=60,
        )
        parser.add_argument(
            "-m",
            "--email",
            dest="email",
            help="Email is used to send notification",
        )
        parser.add_argument(
            "-mp",
            "--email-pass",
            dest="emailPass",
            help="Password of email",
        )
        parser.add_argument(
            "-lu",
            "--limit-usage",
            dest="limitUsage",
            help="Max percent of usage",
            type=int,
            default=90,
        )

        options = parser.parse_args()
        if not options.logPath:
            parser.error(
                "[-] Please specify path of log. User --help for more information"
            )
        elif not options.email:
            parser.error(
                "[-] Please specify email used to send notification. User --help for more information"
            )

        elif not options.emailPass:
            parser.error(
                "[-] Please specify password of email used to send notification. User --help for more information"
            )

        return options


INTERVAL_CHECKING = extractTime(env["INTERVAL_CHECKING"]).total_seconds()


def main(log_path, email, emailPass, limitUsage):
    logPath = log_path if log_path else env["LOG_PATH"]
    _email = email if email else env["MAIL"]
    _emailPass = emailPass if emailPass else env["MAIL_PASSWORD"]
    LIMIT = int(limitUsage) if int(limitUsage) > 0 else 90

    logger = Logger(logPath)
    linuxHealth = LinuxHealth()
    mail = Mail(_email, _emailPass)
    mail.login()

    health = linuxHealth.checkHealth()
    log = health["log"]
    cpuUsed = health["cpu"]
    ramUsed = health["ram"][1]

    print("LOG_PATH: ", logPath)
    print("INTERVAL CHECKING: ", INTERVAL_CHECKING)
    while True:
        if cpuUsed > LIMIT or ramUsed > LIMIT:
            mail.sendToMe(
                "Warning! Your linux OS is overloading. CPU:{}%, RAM:{}%".format(
                    cpuUsed, ramUsed
                )
            )

        logger.write(log)
        print(log)
        time.sleep(INTERVAL_CHECKING)


def start():
    cmd = LinuxHealthCommand()
    options = cmd.setUpArguments()
    main(options.logPath, options.email, options.emailPass, options.limitUsage)


if __name__ == "__main__":
    start()
