# Reguły epizodyczne

Wykonali:
* Michał Berliński, 290432
* Łukasz Pietraszek, 323581

## 0. Uruchomienie programu

### Instalacja wymaganych pakietów
```
pip install -r requirements.txt
pip install -e .
```

### Przykładowe uruchomienie programu
Należy uruchomić plik Jupytera ```win_miner.ipynb```.

1. Ustalenie zbioru danych
```
sequence_alarm_1 = sorted([
(1, 'E'), (2, 'D'), (5, 'A'), (7, 'B'), (8, 'E'), (9, 'C'), (10, 'D'),
(11, 'A'), (12, 'E'), (13, 'A'), (14, 'D'), (16, 'F'), (17, 'C'), (18, 'A'),
(19, 'F'), (20, 'E'), (21, 'A'), (22, 'B'), (23, 'B'), (25, 'E'), (26, 'E'),
(27, 'F'), (28, 'E'), (29, 'D'), (31, 'E'), (32, 'D'), (33, 'A'), (35, 'A'),
(37, 'F'), (38, 'D'), (39, 'A'), (40, 'D'), (42, 'E'), (44, 'F'),
], key=lambda x:x[0])
```
2. Inicjalizacja algorytmu
```
alg = WinMiner(sequence_alarm_1, episode_type='serial')
freqEpisodes = alg.win_miner(max_width=20, step=7, minFrequent=0.1)
```
3. Wygenerowanie reguł
```
win_miner_rules = WinMinerRules(freqEpisodes, max_width=20, step=7, minConfidence=0.75)
ruleList = win_miner_rules.generateRules()
win_miner_rules.printRules(ruleList)
```
```
WinMinerRule: ['A'] [7] ==> ['A', 'E'] [20] [5, 0.875]
WinMinerRule: ['A'] [14] ==> ['A', 'E'] [20] [5, 0.875]
WinMinerRule: ['A'] [20] ==> ['A', 'E'] [20] [5, 0.875]
WinMinerRule: ['B'] [7] ==> ['B', 'A'] [20] [2, 1.0]
WinMinerRule: ['B'] [14] ==> ['B', 'A'] [20] [2, 1.0]
WinMinerRule: ['B'] [20] ==> ['B', 'A'] [20] [2, 1.0]
WinMinerRule: ['B'] [7] ==> ['B', 'D'] [20] [3, 1.0]
WinMinerRule: ['B'] [14] ==> ['B', 'D'] [20] [3, 1.0]
WinMinerRule: ['B'] [20] ==> ['B', 'D'] [20] [3, 1.0]
WinMinerRule: ['B'] [7] ==> ['B', 'E'] [20] [2, 1.0]
WinMinerRule: ['B'] [14] ==> ['B', 'E'] [20] [2, 1.0]
WinMinerRule: ['B'] [20] ==> ['B', 'E'] [20] [2, 1.0]
WinMinerRule: ['C'] [7] ==> ['C', 'E'] [20] [2, 1.0]
WinMinerRule: ['C'] [14] ==> ['C', 'E'] [20] [2, 1.0]
WinMinerRule: ['C'] [20] ==> ['C', 'E'] [20] [2, 1.0]
WinMinerRule: ['C'] [7] ==> ['C', 'F'] [20] [2, 1.0]
WinMinerRule: ['C'] [14] ==> ['C', 'F'] [20] [2, 1.0]
WinMinerRule: ['C'] [20] ==> ['C', 'F'] [20] [2, 1.0]
WinMinerRule: ['E'] [7] ==> ['E', 'A'] [20] [6, 0.8888888888888888]
WinMinerRule: ['E'] [14] ==> ['E', 'A'] [20] [6, 0.8888888888888888]
WinMinerRule: ['E'] [20] ==> ['E', 'A'] [20] [6, 0.8888888888888888]
WinMinerRule: ['E'] [7] ==> ['E', 'F'] [20] [5, 0.7777777777777778]
WinMinerRule: ['E'] [14] ==> ['E', 'F'] [20] [5, 0.7777777777777778]
WinMinerRule: ['E'] [20] ==> ['E', 'F'] [20] [5, 0.7777777777777778]
```


## 1. Przyjęte założenia projektowe
Tematem projektu jest wyszukiwanie reguł epizodycznych, czyli wzorców, które można 
wydobyć z sekwencji, aby odkryć możliwe zależności między wystąpieniami typów zdarzeń 
(słów, znaków) w analizowanej sekwencji. W tym celu stosuje się różne algorytmy wykrywania 
często występujących epizodów w sekwencjach.
Naszym nadrzędnym celem jest analiza sekwencji wydarzeń i odkrywanie powtarzających się 
epizodów. Najpierw sformułujemy koncepcję sekwencji zdarzeń, a następnie przyjrzymy się 
bardziej szczegółowo wybranym odcinkom.

## 2. Krótki opis wybranych zbiorów danych
### 2.1. Sekwencje DNA
Zestaw danych zawiera wygenerowaną losowo sekwencję DNA, przetworzoną do 
odpowiedniego formatu tablicowego. 
### 2.2. Oznaczenia alarmów
Zestaw danych zawiera wybrane sekwencje alarmów w postaci liter A-F. Dane są losowo 
wygenerowaną sekwencją, przetworzoną do odpowiedniego formatu tablicowego. Dane 
zostały wykorzystane w artykule.

## 3. Krótki opis kluczowych definicji reguł epizodycznych
### 3.1. Zdarzenia epizodyczne
Traktujemy dane wejściowe jako sekwencję zdarzeń, w której każde zdarzenie ma przypisany 
czas występowania. Biorąc pod uwagę zbiór E typów zdarzeń, zdarzenie jest parą (A, t), gdzie 
A ∈ E jest typem zdarzenia i t jest liczbą całkowitą oznaczającą czas wystąpienia zdarzenia. 
Rodzaj zdarzenia może faktycznie zawierać kilka atrybutów; dla uproszczenia rozważamy tutaj 
tylko przypadek, w którym rodzaj zdarzenia jest pojedynczą wartością.
### 3.2. Odcinek
Nieformalnie odcinek jest częściowo uporządkowanym zbiorem wydarzeń zachodzących 
razem. Odcinki można opisać jako skierowane grafy acykliczne.

## 4. Eksperymenty
Eksperymenty przeprowadzone zostaną na różnych zbiorach danych, w celu dokładnej analizy 
skuteczności algorytmu. Zastosujemy strojenie parametrów algorytmu takich jak:
* σ - próg częstotliwości w przedziale 0 < σ ≤ 1
* γ - próg ufności w przedziale 0 < γ ≤ 1
* step - krok spadku ufności
* width - zakres wyszukiwanych wzorców
Ponieważ algorytm jest deterministyczny, wystarczy jednokrotne jego wykonanie dla każdego 
zestawu parametrów.

### Plan eksperymentów:
* Sprawdzenie działania algorytmu dla poszczególnych parametrów.
* Zbadanie typu występowania zdarzeń (występujące w tym samym czasie czy nie).
* Wpływ wartości poszczególnych parametrów na czas działania algorytmu.
* Porównanie z innymi implementacjami:
  - sposoby generowania zdarzeń;
  - badania na różnych zbiorach danych;
  - badanie poprawności implementacji (porównanie wyników).

## 5. Wyniki eksperymentów
Testy wykonywane były na zbiorze danych sekwencji DNA wygenerowanej losowo. Testy 
wykonywano dla różnych parametrów sprawdzając zachowanie algorytmu. 
### 5.1. Sprawdzenie działania algorytmu dla poszczególnych parametrów.
Sprawdzaliśmy ilość odnalezionych reguł (o wsparciu większym niż 2 i minimalnej ufności 
większej lub równej 0.75 oraz minimalnej częstotliwości równej 0.1) w zależności od wartości 
parametrów max_width oraz step.
### 5.2. Zbadanie typu występowania zdarzeń (występujące w tym samym czasie czy nie).
Po szczegółowym zbadaniu typów występowania zdarzeń doszliśmy do wniosku, że nie 
pokrywają się one w czasie. Każde kolejne zdarzenie rozpoczyna się po zakończeniu 
poprzedniego zdarzenia.
### 5.3. Wpływ wartości poszczególnych parametrów na czas działania algorytmu.
Poszczególne parametry z pewnością wpływają na czas działania algorytmu, jednakże przy 
współczesnych parametrach sprzętowych komputerów osobistych różnice w czasie są 
niezauważalne. Zmiany poszczególnych parametrów mają jednak duży wpływ na ładowanie 
się wyników. W przypadku uruchomienia algorytmu dla minimalnej ufności 0.1 liczba 
rezultatów jest znacząco wyższa niż w przypadku wyników dla minimalnej ufności na poziomie 1.
### 5.4. Porównanie z innymi implementacjami. 
Z powodu braku podobnych implementacji w celu weryfikacji wyników zastosowaliśmy inny
zbiór danych (sekwencje alarmów zastosowane w artykule), na których również 
przeprowadziliśmy podobne badania. Wyniki pokrywały się z oczekiwaniami.

## 6. Dyskusja i wnioski
Przedstawione w artykule wyniki odnosiły się do różnych zastosowań reguł sekwencyjnych. 
Odnoszono się do artykułu, w którym analizowano kod genetyczny, aby znaleźć zależności 
u osób z miażdżycą, w celu ochrony przed przyszłymi chorobami serca. Autorzy artykułu 
z kolei zajęli się badaniem sejsmicznym, aby określić częstotliwość możliwych trzęsień ziemi. 
W obu przypadkach jednak naukowcy zgodnie stwierdzili, że narzędzie jedynie wskazuje 
pewne parametry ekspertom w tych dziedzinach i nie można wyciągać jednoznacznych 
wniosków z otrzymanych wyników. 
Oczywistymi i nasuwającym się wnioskiem natomiast jest przypuszczenie, że im dłuższe 
odcinki i wyższa czułość, tym większa szansa na to, że znaleziona zależność rzeczywiście może 
być istotna w kontekście badań nad realnymi danymi. Podobnie jak autorzy artykułu, my 
również nie znaleźliśmy lokalnego maksimum na randomizowanych sekwencjach. 

## 7. Wykorzystane technologie i środowisko testowe
* Wykorzystany język programowania: Python 3.9.
* Środowisko testowe: Linux Ubuntu 20.04.
* Parametry sprzętu wykorzystanego do testów:
  - Procesor AMD Ryzen 5 5600H
  - 16 GB RAM

## 8. Literatura
N. Meger, C. Rigotti: Constraint-Based Mining of Episode Rules and Optimal Window Sizes 
PKDD'04, Pisa, Italy.
