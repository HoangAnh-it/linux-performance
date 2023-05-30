from datetime import timedelta
import logging
import smtplib
from email.message import EmailMessage

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
        self.__server.quit()
