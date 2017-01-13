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
    def type_integer(question, default_val, min_val, max_val):
        res = "a"
        while True:
            res = input("%s: [%s] " % (question, default_val))
            if res == "":
                return default_val
            if not res.isdigit():
                continue
            res = int(res)
            if res < min_val:
                print("Minimum value is %s" % min_val)
                continue
            if res > max_val:
                print("Maximum value is %s" % max_val)
                continue
            break
        return res

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
