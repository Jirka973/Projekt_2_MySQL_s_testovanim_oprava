import pytest

from MySQL_Python_kod import (
    pripojeni_k_db,
    pridat_ukol_do_db,
    aktualizovat_ukol_v_db,
    smazat_ukol_z_db,
    najdi_ukol_podle_id
)

# Fixture pro vytvoření a uzavření připojení k databázi pro testy.
@pytest.fixture
def db_connection():
    conn = pripojeni_k_db()
    yield conn
    conn.close()


# Pomocná funkce pro testy - vytváří testovací úkol a vrací jeho ID.
def vytvoreni_testovaciho_ukolu(conn, nazev="test_ukol", popis="test_popis"):
    vysledek = pridat_ukol_do_db(conn, nazev, popis)
    assert vysledek is True

    cursor = conn.cursor()
    cursor.execute(
        "SELECT ID FROM spravce_ukolu WHERE Nazev = %s AND Popis = %s ORDER BY ID DESC LIMIT 1",
        (nazev, popis)
    )
    ukol = cursor.fetchone()
    cursor.close()

    return ukol[0]

# Pomocná funkce pro testy - smazání testovacího úkolu.
def smazani_testovaciho_ukolu(conn, id_ukolu):
    smazat_ukol_z_db(conn, id_ukolu)


# Funkce pro pozitivní testování přidání úkolu do databáze.
def test_pridat_ukol_pozitivni(db_connection):
    nazev = "pytest_pridani"
    popis = "pytest_popis"

    vysledek = pridat_ukol_do_db(db_connection, nazev, popis)
    assert vysledek is True

    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT ID FROM spravce_ukolu WHERE Nazev = %s AND Popis = %s ORDER BY ID DESC LIMIT 1",
        (nazev, popis)
    )
    ukol = cursor.fetchone()

    assert ukol is not None

    cursor.execute("DELETE FROM spravce_ukolu WHERE ID = %s", (ukol[0],))
    db_connection.commit()
    cursor.close()

# Funkce pro negativní testování přidání úkolu do databáze s neplatnými vstupy.
def test_pridat_ukol_negativni(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM spravce_ukolu")
    puvodni_pocet = cursor.fetchone()[0]

    vysledek = pridat_ukol_do_db(db_connection, None, "neplatny_popis")

    cursor.execute("SELECT COUNT(*) FROM spravce_ukolu")
    novy_pocet = cursor.fetchone()[0]

    assert vysledek is False
    assert novy_pocet == puvodni_pocet

    cursor.close()


# Funkce pro pozitivní testování aktualizace úkolu v databázi.
def test_aktualizovat_ukol_pozitivni(db_connection):
    id_ukolu = vytvoreni_testovaciho_ukolu(db_connection)

    vysledek = aktualizovat_ukol_v_db(db_connection, id_ukolu, "hotovo")
    assert vysledek is True

    ukol = najdi_ukol_podle_id(db_connection, id_ukolu)
    assert ukol is not None
    assert ukol[3] == "hotovo"

    smazani_testovaciho_ukolu(db_connection, id_ukolu)


# Funkce pro negativní testování aktualizace úkolu v databázi s neexistujícím ID.
def test_aktualizovat_ukol_negativni(db_connection):
    vysledek = aktualizovat_ukol_v_db(db_connection, 999999, "hotovo")
    assert vysledek is False


# Funkce pro pozitivní testování smazání úkolu z databáze.
def test_smazat_ukol_pozitivni(db_connection):
    id_ukolu = vytvoreni_testovaciho_ukolu(db_connection)

    vysledek = smazat_ukol_z_db(db_connection, id_ukolu)
    assert vysledek is True

    ukol = najdi_ukol_podle_id(db_connection, id_ukolu)
    assert ukol is None


# Funkce pro negativní testování smazání úkolu z databáze s neexistujícím ID.
def test_smazat_ukol_negativni(db_connection):
    vysledek = smazat_ukol_z_db(db_connection, 999999)
    assert vysledek is False