import socket
import datetime
import time

# Lokitiedoston sijainti
FILE = "/path/to/your/logfile"


def ping():
    """Tarkistaa verkkoyhteyden tilan."""
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("8.8.8.8", 53))
        s.close()
        return True
    except OSError:
        return False


def calculate_time(start, stop):
    """Laskee katkoksen keston sekunneissa."""
    difference = stop - start
    seconds = float(difference.total_seconds())
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def log_message(message):
    """Kirjoittaa viestin lokitiedostoon."""
    try:
        with open(FILE, "a") as file:
            file.write(message + "\n")
    except IOError as e:
        print(f"Virhe lokitiedoston kirjoituksessa: {e}")


def first_check():
    """Tarkistaa verkkoyhteyden käynnistettäessä."""
    if ping():
        connection_time = datetime.datetime.now()
        log_message("\nYHTEYS HAVAITTU\n")
        log_message(f"Yhdistetty verkkoon: {connection_time}")
        return True
    else:
        log_message("\nEI YHTEYTTÄ\n")
        return False


def main():
    """Ohjelman päälogiikka."""
    monitor_start_time = datetime.datetime.now()
    log_message(f"Valvonta aloitettu: {monitor_start_time}")

    if not first_check():
        # Odottaa yhteyden palautumista
        while not ping():
            time.sleep(1)
        first_check()

    # Aloittaa yhteyden jatkuvan valvonnan
    while True:
        if not ping():
            down_time = datetime.datetime.now()
            log_message(f"Verkko katkennut: {down_time}")
            print(f"Verkko katkennut: {down_time}")

            while not ping():
                time.sleep(1)

            up_time = datetime.datetime.now()
            downtime_duration = calculate_time(down_time, up_time)
            log_message(f"Yhdistetty uudelleen: {up_time}")
            log_message(f"Katkoksen kesto: {downtime_duration}")
            print(f"Yhdistetty uudelleen: {up_time}")
            print(f"Katkoksen kesto: {downtime_duration}")
        else:
            time.sleep(5)


if __name__ == "__main__":
    main()
