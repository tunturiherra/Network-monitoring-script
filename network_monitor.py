import os
import time
from datetime import datetime

# Lokitiedoston sijainti
LOGFILE = "/home/sammeli/network_log.txt"
# Kohde, jota pingataan (Googlen DNS)
PING_TARGET = "8.8.8.8"

def log_message(message):
    """Kirjoittaa viestin lokitiedostoon aikaleiman kanssa."""
    with open(LOGFILE, "a") as log:
        log.write(f"{datetime.now()}: {message}\n")

def check_connection():
    """Tarkistaa verkkoyhteyden ping-komennolla."""
    response = os.system(f"ping -c 1 -W 2 {PING_TARGET} > /dev/null 2>&1")
    return response == 0  # Palauttaa Truen, jos yhteys toimii

def main():
    log_message("Verkon valvonta aloitettu.")  # Alkuviesti lokitiedostoon
    was_connected = True  # Alustetaan sillä olettamuksella, että yhteys toimii

    while True:
        # Testataan verkkoyhteys
        is_connected = check_connection()

        # Vain tilan muutokset tallentuvat lokiin
        if is_connected and not was_connected:
            log_message("Yhteys palautui.")  # Yhteys palautui
        elif not is_connected and was_connected:
            log_message("Yhteys katkennut!")  # Yhteys katkesi

        # Päivitetään tila seuraavaa kierrosta varten
        was_connected = is_connected

        # Odota ennen seuraavaa tarkistusta
        time.sleep(10)  # Tarkistusväli 10 sekuntia

if __name__ == "__main__":
    main()
