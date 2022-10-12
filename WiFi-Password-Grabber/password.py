import subprocess
import sys

command = subprocess.check_output(["netsh", "wlan", "show", "profiles"])
data = command.decode("utf-8", errors="backslahsreplace")
ndata = data.split("\n")
profiles = []

for i in ndata:
    # find "All User Profile"
    if "All User Profile" in i:
        i = i.split(":")
        i = i[1]
        i = i[1:-1]
        profiles.append(i)

sys.stdout = open("all_pass.txt", "w")

# with open("all_password.txt", "w", encoding="utf-8") as f:
print("=============================================")
print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
print("=============================================")

for i in profiles:
    try:
        results = subprocess.check_output(["netsh", "wlan", "show", "profiles", i, "key=clear"])
        results = results.decode("utf-8", errors="backslashreplace")
        results = results.split("\n")
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

        try:
            print("{:<30}| {:<}".format(i, results[0]))
        except IndexError:
            print("{:<30}| {:<}".format(i, ""))
    except subprocess.CalledProcessError:
        print("Error founded, exiting")

hostnames = subprocess.check_output("hostname")
nhostname = hostnames.decode("utf-8", errors="backslashreplace")

print(f"\nAll password collected from: {nhostname}")

sys.stdout.close()