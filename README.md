# Projekt_2_MySQL_s_testovanim_oprava
# Správce úkolů (Python + MySQL)

Konzolová aplikace pro správu úkolů s využitím MySQL databáze a sadu automatizovaných testů v pyestu. Projekt ukazuje základní CRUD operace (vytvoření, čtení, aktualizace, smazání) nad databází.

# Požadavky

- Python 3.x, nejlépe 3.13
- Nainstalovaný MySQL Server
- Knihovna "mysql-connector-python"
- "pytest" a "playwright"  pro spuštění testů 

# Instalace závislostí
- Nainstalujte potřebné balíčky:

- pip install mysql-connector-python
- pip install pytest
- pip install pytest-playwright
- playwright install


# Příprava MySQL databáze

1. Přihlaste se do MySQL.
2. Vytvořte databázi pro projekt, například: CREATE DATABASE název_vaší_db
3. V souboru "MySQL_Python_kod.py" doplňte své přihlašovací údaje k databázi ve funkci "pripojeni_k_db()":
   
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="VAŠE_HESLO",
    database="název_vaší_db" 
)

Ujistěte se, že zadaný název databáze (database="název_vaší_db") odpovídá databázi, kterou jste vytvořili.

# První spuštění aplikace

1. Ujistěte se, že MySQL server běží a přihlašovací údaje v "MySQL_Python_kod.py" jsou správné.
2. V konzoli přejděte do složky s projektem.
3. Spusťte hlavní program (Zakladni_program.py):

Při prvním spuštění aplikace se v databázi automaticky vytvoří tabulka "spravce_ukolu" (pokud ještě neexistuje).

# Ovládání programu
Po spuštění se zobrazí hlavní menu:

- 1 – Přidat nový úkol  
  Zadáte název a popis úkolu; aplikace uloží úkol do databáze. 
- 2 – Zobrazit všechny úkoly  
  Vypíše aktuální úkoly (např. s vybranými stavy). 
- 3 – Aktualizovat úkol  
  Zobrazí seznam úkolů, vyberete ID úkolu a nový stav („probíhá“ / „hotovo“). ]
- 4 – Odstranit úkol  
  Zobrazí seznam úkolů, vyberete ID úkolu k smazání. 
- 5 – Konec programu  
  Zavře připojení k databázi (pokud je otevřené) a ukončí aplikaci.

# Spuštění testů
Pokud máte nainstalovaný pytest a připravenou databázi (stejné přihlašovací údaje jako v aplikaci), můžete spustit automatizované testy příkazem v terminálu: 
pytest 
popřípadě: python -m pytest (v případě nefunkčnosti klasického : pytest)

Testy provádějí:
- pozitivní a negativní test přidání úkolu 
- pozitivní a negativní test aktualizace úkolu 
- pozitivní a negativní test smazání úkolu 

Každý test si připraví vlastní testovací data v databázi a po skončení testu je opět smaže, aby se databáze zbytečně neplnila testovacími záznamy. 

# Poznámky
- před spuštěním si doplňte vlastní hodnoty v "MySQL_Python_kod.py".
- Projekt je zaměřený na lokální běh (MySQL na "localhost"); vzdálený přístup k databázi není v rámci zadání řešen.
