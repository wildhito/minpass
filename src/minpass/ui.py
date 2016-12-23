import getpass


class UI(object):
    @staticmethod
    def create_secret(input_type):
        sec1 = getpass.getpass("Enter %s: " % input_type)
        sec2 = getpass.getpass("Re-enter %s: " % input_type)
        if sec1 != sec2:
            print("Error: non matching %ss" % input_type)
            return ""
        return sec1

    @staticmethod
    def type_secret(input_type):
        return getpass.getpass("Enter %s: " % input_type)

    @staticmethod
    def confirm(question, default_yes=False):
        res = "-"
        choices = "[y/N]"
        if default_yes:
            choices = "[Y/n]"

        while (not res in ["", 'y', 'n']):
            res = input("%s %s " % (question, choices)).lower()
            if res == "y":
                return True
            if res == "n":
                return False
            if res == "":
                return default_yes
