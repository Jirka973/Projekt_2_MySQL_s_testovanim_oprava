from datetime import datetime 
import mysql.connector


# Vytvoření kurzoru pro provádění SQL příkazů.
# Před spuštěním nezapomeň vyplnit své přihlašovací údaje k MySQL databázi v proměnných password a database. 
def pripojeni_k_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="XXXX",  
            database="XXXX"  
        )
        return conn

    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}\n") 


# Funkce pro přidání úkolu do databáze. 
# Formátování data je provedeno pomocí modulu datetime, který získá aktuální datum a převede ho do formátu "YYYY-MM-DD".
def pridat_ukol_do_db(conn, nazev, popis):
    now=datetime.now()
    datum = now.strftime("%Y-%m-%d")

    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO spravce_ukolu (Nazev, Popis, Datum_vytvoreni) VALUES (%s, %s, %s)", (nazev, popis, datum))
        conn.commit()

        if cursor.rowcount == 1:
            print(f"Úkol '{nazev}' byl úspěšně uložen do databáze.\n")
            return True
        else:
            print(f"Úkol '{nazev}' se nepodařilo uložit.\n")
            return False

    except mysql.connector.Error as err:
        print(f"Chyba při ukládání úkolu do databáze: {err}\n")
        return False

    finally:
        if cursor:
            cursor.close()



# Funkce pro vytvoření tabulky v databázi.
def vytvoreni_tabulky(conn):
    cursor = None

    try:
        
        cursor = conn.cursor()

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS spravce_ukolu (
            ID INT AUTO_INCREMENT PRIMARY KEY, 
            Nazev varchar (255) Not NULL,
            Popis varchar (255) Not NULL,
            Stav ENUM ("nezahájeno", "probíhá", "hotovo")
            DEFAULT "nezahájeno" ,
            Datum_vytvoreni DATE
            ); 
        ''')
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}\n")  

    finally:
        if cursor:
            cursor.close()
        

# Funkce pro zobrazení úkolů z databáze.
def zobrazit_ukoly_v_db(conn): 

    cursor = None   
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Nazev, Popis, Stav FROM spravce_ukolu where Stav = 'nezahájeno' or Stav = 'probíhá' ORDER BY ID")
        return cursor.fetchall() 

    except mysql.connector.Error as err:
        print(f"Chyba při zobrazování úkolů: {err}\n")
        return []
    
    finally: 
        if cursor:
            cursor.close()
        



# Funkce pro smazání úkolu z databáze.
def smazat_ukol_z_db(conn, id_ukolu): 
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM spravce_ukolu WHERE ID = %s", (id_ukolu,))
        conn.commit()

        if cursor.rowcount == 1:
            print(f"Úkol s ID {id_ukolu} byl smazán.\n")
            return True
        else:
            print(f"Úkol s ID {id_ukolu} nebyl nalezen. Žádný úkol nebyl smazán.\n")
            return False
    except mysql.connector.Error as err:
        print(f"Chyba při mazání úkolu: {err}\n")
        return False
    finally:
        if cursor:
            cursor.close()
        
        



# Funkce pro aktualizaci úkolu v databázi.
def aktualizovat_ukol_v_db(conn, id_ukolu, novy_stav):
    cursor = None   

    try:
        if novy_stav not in ["probíhá", "hotovo"]:
            return False

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE spravce_ukolu SET Stav = %s WHERE ID = %s",
            (novy_stav, id_ukolu)
        )
        conn.commit()

        if cursor.rowcount == 1:
            print(f"Úkol s ID {id_ukolu} byl aktualizován.\n")
            return True
        else:
            print(f"Úkol s ID {id_ukolu} nebyl nalezen. Žádný úkol nebyl aktualizován.\n")
            return False

    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}\n")
        return False

    finally:
        if cursor:
            cursor.close()


# Funkce pro vyhledání úkolu podle ID v databázi. 
def najdi_ukol_podle_id(conn, id_ukolu):
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ID, Nazev, Popis, Stav FROM spravce_ukolu WHERE ID = %s",
            (id_ukolu,)
        )
        return cursor.fetchone()

    except mysql.connector.Error as err:
        print(f"Chyba při hledání úkolu: {err}\n")
        return None

    finally:
        if cursor:
            cursor.close()




