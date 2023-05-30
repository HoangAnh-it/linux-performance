from crontab import CronTab
from dotenv import dotenv_values
import os
import subprocess

env = dotenv_values(".env")


class AppSchedule:
    def __init__(self, username):
        self.user = username
        self.manager = CronTab(username)
        pass

    def newSchedule(self, command="", comment="", minute=59):
        if not command or not comment:
            print("exit with no command or comment")
            return
        if self.isExisting(comment):
            print("Already exist cron with comment:", comment)
            self.removeByComment(comment)
            print("Remove existed cron")
        job = self.manager.new(command=command, comment=comment)
        job.minute.every(minute)
        self.manager.write()
        print(f"Done: create cron. Interval: %d minute(s)" % minute)
        return job

    def isExisting(self, comment):
        for job in self.manager:
            if job.comment == comment:
                return True
        return False

    def removeByComment(self, comment):
        self.manager.remove_all(comment=comment)


def main():
    # create command
    result = subprocess.run(["which", "python3"], capture_output=True, text=True)
    if result.returncode == 0:
        python_path = result.stdout.strip()
    else:
        print("Cannot find python3")
        os._exit(1)

    sourcePath = "{path_folder}/{entryFile}".format(
        path_folder=os.getcwd(), entryFile="dist/main"
    )

    # command = python_path + " " + sourcePath
    command = sourcePath

    USER_CRON = env["USER_CRON"]
    schedule = AppSchedule(USER_CRON)
    schedule.newSchedule(
        command=command,
        comment="linux-health",
        minute=1,
    )


main()
