# FusionPuls.py i FusionClient.py

## Opis
Projekt "FusionPuls" to prosty serwer i klient czatu, które pozwalają użytkownikom na komunikację tekstową w czasie rzeczywistym.
Serwer umożliwia podłączanie wielu klientów jednocześnie i przesyłanie wiadomości między nimi. 
Klient pozwala użytkownikom na dołączanie do serwera, wysyłanie i odbieranie wiadomości.

## Wymagania
- Python 3.x
- Biblioteka `socket`
- Biblioteka `select`
- Biblioteka `colorama`

- pip install -r requirements.txt

## Uruchamianie

### Serwer (FusionPuls.py)
1. Uruchom terminal.
2. Przejdź do katalogu zawierającego plik `FusionPuls.py`.
3. Wpisz `python FusionPuls.py` i naciśnij Enter.
4. Serwer zostanie uruchomiony i zacznie nasłuchiwać na wskazanym adresie IP i porcie.

### Klient (FusionClient.py)
1. Uruchom terminal.
2. Przejdź do katalogu zawierającego plik `FusionClient.py`.
3. Wpisz `python FusionClient.py` i naciśnij Enter.
4. Podaj nazwę użytkownika oraz adres IP i port serwera, do którego chcesz się podłączyć.
5. Po poprawnym podłączeniu będziesz mógł wprowadzać i odbierać wiadomości na czacie.

## Funkcje

### FusionPuls.py (Serwer)
- Nasłuchiwanie na określonym adresie IP i porcie.
- Obsługa wielu klientów jednocześnie.
- Wysyłanie i odbieranie wiadomości od klientów.
- Wyświetlanie informacji o dołączających i rozłączających się klientach.

### FusionClient.py (Klient)
- Podłączanie do serwera poprzez wprowadzenie adresu IP i portu.
- Wysyłanie i odbieranie wiadomości na czacie.
- Obsługa nazwy użytkownika.
- Wyświetlanie kolorowych symboli informujących o różnych wydarzeniach.

## Wskazówki
- Upewnij się, że używane adresy IP i numery portów są dostępne i poprawne.
- W pliku `FusionClient.py` wprowadź nazwę użytkownika i dane serwera przed uruchomieniem klienta.
- Pamiętaj, że to tylko prosty przykład, który może być rozwinięty o dodatkowe funkcje i zabezpieczenia.

### Autor
- Ten projekt został stworzony przez użytkownika "keno76tech". 
- https://github.com/keno76tech
