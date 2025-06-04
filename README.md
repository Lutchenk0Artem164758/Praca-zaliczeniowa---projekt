# Projekt: Aplikacja Klient-Serwer – Animal Network

## Autor
- Lutchenko Artem
- Bohdan Protasov
- Andrii Tarnovskyi

## Opis

Aplikacja sieciowa działająca w architekturze klient-serwer. Serwer zarządza kolekcją obiektów trzech klas (`Cat`, `Dog`, `Bird`) i umożliwia klientom pobieranie ich na żądanie. Jednocześnie może być obsługiwanych maksymalnie `MAX_CLIENTS = 3` klientów — nadmiarowi otrzymują komunikat `REFUSED`.

## Struktura projektu

- `server.py` – implementacja serwera
- `client.py` – implementacja klienta
- `animal.py` – definicje klas danych: `Animal`, `Cat`, `Dog`, `Bird`

## Wymagania

- Python 3.12+
- Brak zewnętrznych bibliotek – użyto tylko standardowych modułów (`socket`, `threading`, `pickle`, `time`, `random`)

## Uruchamianie

### Serwer

```bash
python server.py
```

Serwer nasłuchuje na `localhost:23456` i tworzy po 4 obiekty każdej klasy (`Cat`, `Dog`, `Bird`), zapisując je w mapie z kluczami w formacie `cat_1`, `dog_3`, `bird_4`, itd.

### Klient

```bash
python client.py
```

Skrypt uruchamia jednego klienta z losowym ID. Klient wysyła swoje ID, a następnie trzykrotnie prosi o dane jednej z klas (`cat`, `dog`, `unicorn`).

## Klient może:

- otrzymać odpowiedź `OK` i przetworzyć dane,
- otrzymać odpowiedź `REFUSED`, jeśli serwer osiągnął limit aktywnych klientów.

## Przykład działania

```
Client 1234: connected.
Client 1234 received: Cat(Cat1, age=3)
Client 1234 received: Dog(Dog2, age=3)
Client 1234 received: Dog(Reserve, age=0)
```

```
Client 5678: connection refused.
```

## Obsługa błędów

- Klienci wykrywają problemy z serializacją i typem danych (`TypeError`).
- Serwer przesyła rezerwowy obiekt `Dog("Reserve", 0)`, jeśli żądana klasa nie istnieje.

## Uwagi

- Obsługa klientów odbywa się w osobnych wątkach z losowym opóźnieniem (`sleep`), co pozwala zaobserwować współbieżność.
- Limit `MAX_CLIENTS` egzekwowany jest natychmiast po odebraniu ID klienta – nadmiarowi są odrzucani.
