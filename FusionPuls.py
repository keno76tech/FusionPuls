# -- Importowanie bibliotek -- #
import socket # Biblioteka odpowiadająca za obsługę operacji sieciowych
import select # Biblioteka odpowiada za monitorowanie wielu gniazd
from colorama import init, Fore, Back, Style # Funkcja colored służy do dodawania koloru do tekstu wyświetlanego w konsoli
import sys # Biblioteka dostarcza funkcje i zmienne umożliwiające interakcję z interpreterem Pythona

# -- Inicjalizacja koloramy -- #
init()

# -- Ustawianie Gniazda Sieciowego -- #
server_ip = socket.gethostbyname(socket.gethostname()) # Pozyskiwanie ip komputera i ustawianie go jako ip serwera
server_port = 17630 # Ustawianie portu serwera

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tworzenie nowego gniazda serwera IPv4 tcp
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Konfiguracja gniazda serwera
server_socket.bind((server_ip, server_port)) # Powiązanie gniazda serwera z konkretnym adresem IP i numerem portu

server_socket.listen() # Nasłuchiwanie serwera

# -- Ustawianie List i zmiennych systemowych -- #
sockets_list = [server_socket] # Lista gniazd sieciowych
clients = {} # Lista użytkowników
header_length = 10 # Ustawianie długości nagłówka

# -- Ustawianie zmiennych służących do dodawania koloru do tekstu wyświetlanego w konsoli -- #
information_symbol = Fore.CYAN + '@' + Style.RESET_ALL # Ustawienie symbolu informacyjnego
correct_symbol = Fore.GREEN + '+' + Style.RESET_ALL # Ustawienie symbolu pomyślnie wykonanej operacji
error_symbol = Fore.RED + '!' + Style.RESET_ALL # Ustawienie symbolu błędu
message_symbol = Fore.LIGHTYELLOW_EX + '>' + Style.RESET_ALL # Ustawianie symbolu wiadomości

# -- Uruchamianie serwera -- #
print(f'[{information_symbol}] Serwer został uruchomiony na {server_ip}:{server_port}') # Informacja o starcie serwera
print(f'[{information_symbol}] Oczekiwanie na połączenie użytkowników:\n') # Informacja o oczekiwaniu na dołączenie

# -- Funckja odbierania wiadomości -- #
def receive_message(client_socket):

    try: # Próbowanie operacji odczytania wiadomości

        message_header = client_socket.recv(header_length) # Odbierania danych ze zdalnego gniazda sieciowego

        if not len(message_header): # Jeżeli wiadomość nie posiada danych
            return False # Zwracanie funkcji
        
        message_length = int(message_header.decode('utf-8').strip()) # Odczytania długości wiadomości z otrzymanego nagłówka

        return {'header': message_header, 'data': client_socket.recv(message_length)} # Zwracanie słownika

    except: # Podczas wystompienia błędu zwracanie odpowiedzi False

        return False
    
# -- Głowna pentla serwera -- #
while True: # pętla

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list) # Monitorowanie listy gniazd sieciowych

    for notified_socket in read_sockets: # Wykonywanie operacji przez listę gniazd

        if notified_socket == server_socket: # Rozróżnianie, czy dane zdarzenie dotyczy gniazda serwera

            client_socket, client_address = server_socket.accept() # Akceptowanie połączenia od clienta

            user = receive_message(client_socket) # Pobieranie nazwy użytkownika

            if user is False: # Sprawdzanie danych nazwy użytkownika
                continue

            sockets_list.append(client_socket) # Dodawanie użytkownika do listy połączeń

            clients[client_socket] = user # Dodawanie nowego klienta

            # -- Wyświetlanie dołączenia użytkonwika -- #
            username = user['data'].decode('utf-8') # Pobieranie nazwy użytkownika
            print(f'[{correct_symbol}] Zaakceptowano połączenie od {client_address[0]}:{client_address[1]}, Nazwa użytkownika: {username}') # Wyświetlanie informacji
            
            print(f'[{information_symbol}] Obecna ilość użytkowników na serwerze to: {len(clients)}') # Informacja o ilości połączeń

        else: # Wprzeciwnym razie rozróżniania czy dane znarzenie dotyczy gniazda serwera

            message = receive_message(notified_socket) # Odbieranie wiadomości od użytkownika

            if message is False: # Jeżeli wiadomoś nieprawidłowa

                # -- Wyświetlanie odłączenia użytkownika -- #
                username = clients[notified_socket]['data'].decode('utf-8') # Pobieranie nazwy użytkownika
                print(f'[{error_symbol}] Rozłączono użytkownika: {username}') # Wyświetlanie informacji

                sockets_list.remove(notified_socket) # Usuwanie z listy połączenia gniazda sieciowego
                del clients[notified_socket] # Usuwanie klienta

                print(f'[{information_symbol}] Obecna ilość użytkowników na serwerze to: {len(clients)}') # Informacja o ilości połączeń

                continue
            
            # -- Wyświetlanie wiadomości od użytkownika -- #
            user = clients[notified_socket] # Pobieranie informacji o użytkowniku
            username = user["data"].decode("utf-8") # Pobieranie nazwy użytkownika

            print(f'[{message_symbol}] Wysłano wiadomość od: {username} / "{message["data"].decode("utf-8")}"') # Wyświetlanie wiadomości od użytkownika

            for client_socket in clients: # Petla użytkowników

                if client_socket != notified_socket: # Sprawdzanie użytkownika

                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data']) # Wysyłanie wiadomości do innych użytkowników

    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket) # Usuwanie aktualnego gniazda sieciowego 

        del clients[notified_socket] # Usuwanie informacji o kliencie