
# Ze souboru MySQL_Python_kod.py importujeme funkce pro práci s databází a správu úkolů.
from MySQL_Python_kod import (
    pripojeni_k_db,
    vytvoreni_tabulky,
    zobrazit_ukoly_v_db,
    aktualizovat_ukol_v_db,
    smazat_ukol_z_db,
    pridat_ukol_do_db
)


# Základní funkce pro interakci s uživatelem.
def hlavni_menu(conn):
    print("Správce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit všechny úkoly")
    print("3. Aktualizovat úkol")
    print("4. Odstranit úkol")
    print("5. Konec programu\n")

    vybrana_moznost = input("Vyberte možnost (1-5): ")
    print(" ")

    if vybrana_moznost == "1":
        pridat_ukol(conn)
    elif vybrana_moznost == "2":
        zobrazit_ukoly(conn)
    elif vybrana_moznost == "3":
        aktualizovat_ukol(conn)
    elif vybrana_moznost == "4":
        smazat_ukol(conn)
    elif vybrana_moznost == "5":
        ukoncit_program(conn)
    else:
        print("Neplatná možnost. Vyber číslo od 1 do 5!")



# Funkce níže slouží k přidání úkolu do databáze.
def pridat_ukol(conn):
    nazev_ukolu = input("Zadejte název úkolu: ").strip()
    while not nazev_ukolu:
        print("Název úkolu nemůže být prázdný. Zadejte platný název.")
        nazev_ukolu = input("Zadejte název úkolu: ").strip()

    popis_ukolu = input("Zadejte popis úkolu: ").strip()
    while not popis_ukolu:
        print("Popis úkolu nemůže být prázdný. Zadejte platný popis.")
        popis_ukolu = input("Zadejte popis úkolu: ").strip()

    vysledek = pridat_ukol_do_db(conn, nazev_ukolu, popis_ukolu)
    
    if vysledek:
        print(f"Úkol '{nazev_ukolu}' byl úspěšně přidán do databáze.\n")
    else:
        print(f'Úkol "{nazev_ukolu}" se nepodařilo přidat do databáze.\n')


# Tato funkce slouží k zobrazení úkolů z databáze.
def zobrazit_ukoly(conn):
    ukoly = zobrazit_ukoly_v_db(conn)

    if ukoly:
        print("Seznam úkolů: ") 
        for id, nazev, popis, stav in ukoly:
            print(f" [ID: {id}] {nazev}: {popis} (Stav: {stav})")
        print()
    else:
        print("Žádné úkoly nenalezeny.\n")

# Tato funkce slouží k aktualizaci úkolu v databázi.
def aktualizovat_ukol(conn):
    ukoly = zobrazit_ukoly_v_db(conn)

    if not ukoly:
        print("Žádné úkoly nenalezeny")
        return

    print("Seznam úkolů:")
    for id_ukolu, nazev, popis, stav in ukoly:
        print(f"[ID: {id_ukolu}] {nazev}: {popis} (Stav: {stav})")

    zadany_vstup = input("\nZadej ID úkolu, který chceš aktualizovat: ")

    try:
        id_ukolu = int(zadany_vstup)
    except ValueError:
        print("Neplatný vstup pro ID úkolu.\n")
        return

    print("Vyber nový stav úkolu:")
    print("1. Probíhá")
    print("2. Hotovo")

    volba = input("Zadej číslo nového stavu: ")

    if volba == "1":
        novy_stav = "probíhá"
    elif volba == "2":
        novy_stav = "hotovo"
    else:
        print("Neplatná volba. Žádný úkol nebyl aktualizován.\n")
        return

    vysledek = aktualizovat_ukol_v_db(conn, id_ukolu, novy_stav)

    if vysledek:
        print(f"Stav úkolu s ID {id_ukolu} byl aktualizován.\n")
    else:
        print(f"Úkol s ID {id_ukolu} nebyl nalezen.\n")
    # Zde by mělo následovat výběr úkolu k aktualizaci
    # a následná aktualizace

# Tato funkce slouží k odstranění úkolu z databáze.
def smazat_ukol(conn):
    ukoly = zobrazit_ukoly_v_db(conn)

    if not ukoly:
        print("Žádné úkoly nenalezeny.\n")
        return

    print("Seznam úkolů:")
    for id_ukolu, nazev, popis, stav in ukoly:
        print(f"[ID: {id_ukolu}] {nazev}: {popis} (Stav: {stav})")

    zadany_vstup = input("Zadej ID úkolu, který chceš smazat: ")

    try:
        id_ukolu = int(zadany_vstup)
    except ValueError:
        print("Neplatný vstup pro ID úkolu.\n")
        return

    vysledek = smazat_ukol_z_db(conn, id_ukolu)

    if vysledek:
        print(f"Úkol s ID {id_ukolu} byl smazán.\n")
    else:
        print(f"Úkol s ID {id_ukolu} nebyl nalezen.\n")

# Funkce pro ukončení programu a uzavření připojení k databázi.
def ukoncit_program(conn):
    if conn:
        conn.close()
    print("Program se ukončil.")
    exit()


if __name__ == "__main__":
    conn = pripojeni_k_db()
    if conn is None:
        print("Nepodařilo se připojit k databázi.")
    else:   
        vytvoreni_tabulky(conn)

    while True:
        hlavni_menu(conn)