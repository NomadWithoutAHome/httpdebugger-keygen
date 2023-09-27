import re
import random
import hashlib
import platform
import winreg


class Keygen:
    parsed_version = None
    serial_number = None
    generated_key = None

    @staticmethod
    def find_match(regex, text):
        return re.search(regex, text).group(0) if re.search(regex, text) else None

    @classmethod
    def retrieve_app_version(cls):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\MadeForNet\\HTTPDebuggerPro") as key:
                version = winreg.QueryValueEx(key, "AppVer")[0]
                cls.parsed_version = cls.find_match(r"(\d+.*)", version).replace(".", "") if version else None
        except FileNotFoundError:
            cls.parsed_version = None

    @classmethod
    def generate_serial_number(cls):
        volume_info = hashlib.md5(platform.system().encode()).hexdigest()
        cls.serial_number = str(int(cls.parsed_version or 0) ^ ((int(volume_info, 16) >> 1) + 0x2E0) ^ 0x590D4)

    @staticmethod
    def produce_key():
        random.seed()
        Keygen.generated_key = "".join([f"{random.randint(0, 255):02X}" for _ in range(7)])

    @classmethod
    def write_license_key(cls):
        cls.retrieve_app_version()
        cls.generate_serial_number()
        cls.produce_key()

        print("[ < ] App Version:", cls.parsed_version)
        print("[ < ] Serial Number: SN" + cls.serial_number)
        print("[ < ] Generated Key:", cls.generated_key)

        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\MadeForNet\\HTTPDebuggerPro") as key:
                winreg.SetValueEx(key, "SN" + cls.serial_number, 0, winreg.REG_SZ, cls.generated_key)
                print("\t[ + ] License key written successfully.")
        except PermissionError:
            print("Unable to write to the registry.")


if __name__ == "__main__":
    Keygen.write_license_key()
