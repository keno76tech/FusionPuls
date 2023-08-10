# -- Importowanie bibliotek -- #
import socket  # Biblioteka odpowiadająca za obsługę operacji sieciowych
import select  # Biblioteka odpowiada za monitorowanie wielu gniazd
import sys  # Biblioteka dostarcza funkcje i zmienne umożliwiające interakcję z interpreterem Pythona
from colorama import init, Fore, Style  # Funkcja colored służy do dodawania koloru do tekstu wyświetlanego w konsoli

# -- Inicjalizacja kolorów -- #
init()

# -- Ustawianie zmiennych służących do dodawania koloru do tekstu wyświetlanego w konsoli -- #
information_symbol = Fore.CYAN + '@' + Style.RESET_ALL
correct_symbol = Fore.GREEN + '+' + Style.RESET_ALL
error_symbol = Fore.RED + '!' + Style.RESET_ALL
message_symbol = Fore.LIGHTYELLOW_EX + '>' + Style.RESET_ALL

# -- Ustawienia użytkownika -- #
client_username = str(input(f"[{information_symbol}] Nazwa użytkownika: "))

if client_username == '': # Sprawdzanie czy nazwa użytkownika zawiera dane
    client_username = str(socket.gethostname())

# -- Ustawianie Gniazda Sieciowego -- #
server_ip = input(f'[{information_symbol}] IP serwera: ')
server_port = input(f'[{information_symbol}] PORT serwera: ')
header_length = 10

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((str(server_ip), int(server_port)))
client_socket.setblocking(False)

# -- Wysyłanie nazwy użytkownika -- #
username = client_username.encode('utf-8')
username_header = f"{len(username):<{header_length}}".encode('utf-8')
client_socket.send(username_header + username)

# -- Informacja o podłączeniu do serwera -- #
print(f'[{correct_symbol}] Podłączono do serwera {server_ip}:{server_port}:\n')

# -- Pętla główna programu -- #
while True:
    try:
        message = str(input(f'[{message_symbol}] {client_username}: '))

        if message:
            # -- Wysyłanie wiadomości do serwera -- #
            message = message.encode('utf-8')
            message_header = f"{len(message):<{header_length}}".encode('utf-8')
            client_socket.send(message_header + message)

        try:
            while True:
                try:
                    username_header = client_socket.recv(header_length)

                    if not len(username_header):
                        print(f'[{error_symbol}] Połączenie zostało zamknięte przez serwer')
                        sys.exit()

                    username_length = int(username_header.decode('utf-8').strip())
                    username = client_socket.recv(username_length).decode('utf-8')

                    message_header = client_socket.recv(header_length)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = client_socket.recv(message_length).decode('utf-8')

                    print(f'[{message_symbol}] {username}: {message}')

                except socket.error as e:
                    if e.errno == 10035:
                        break  # Brak dostępnych danych, pętla kontynuowana

                    print(f'[{error_symbol}] Błąd odczytu: {e}')
                    sys.exit()

        except Exception as e:
            print(f'[{error_symbol}] Błąd systemu')
            print(e)
            sys.exit()

    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print("\n[!] Wyjście z programu na żądanie użytkownika.")
        else:
            print(f'[{error_symbol}] Błąd: {e}')
        sys.exit()
