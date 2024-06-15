import re
import platform
import subprocess
import sys


def is_valid_hostname(hostname: str):
    if len(hostname) > 255:
        return False
    if hostname.endswith("."):
        hostname = hostname[:-1]
    disallowed = re.compile("[^A-Z\d-]", re.IGNORECASE)
    return all(
        (label and len(label) <= 63
         and not label.startswith("-") and not label.endswith("-")
         and not disallowed.search(label))
        for label in hostname.split("."))


def main():
    if len(sys.argv) < 2:
        print("Hostname required")
        exit(1)
    hostname = sys.argv[1]
    if len(sys.argv) > 2:
        size = sys.argv[2]
    else:
        size = 1450
    if not is_valid_hostname(hostname):
        print("Invalid hostname")
        exit(1)

    command = ["ping", hostname, "-D", "-c", "1", "-s", str(size)]
    if platform.system().lower() == "windows":
        command[2] = "-f"
        command[3] = "-n"
        command[5] = "-l"
    elif platform.system().lower() == "linux":
        command[2] = "-M"
        command.insert(3, "do")

    try:
        resp = subprocess.check_call(command[:-1] + ["1"])
    except subprocess.CalledProcessError:
        print("Hostname unreachable or it is incorrect")
        exit(1)

    while True:
        try:
            resp = subprocess.call(command)
            if resp != 0:
                break
            command[-1] = str(int(command[-1]) + 1)

        except subprocess.CalledProcessError:
            print("An error has occurred")
            exit(1)

    while True:
        try:
            resp = subprocess.call(command)
            if resp == 0:
                break
            command[-1] = str(int(command[-1]) - 1)

        except subprocess.CalledProcessError:
            print("An error has occurred")
            exit(1)

    print(int(command[-1]) + 28)


if __name__ == "__main__":
    main()
