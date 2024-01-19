from simple_sqlite_class import SqlPractice

db_file = 'database.db'

if __name__ == "__main__":

    db = SqlPractice(db_file)

    first_table = """
    -- first_table table
    CREATE TABLE IF NOT EXISTS first_table (
        strategy text PRIMARY KEY,
        opis text NOT NULL,
        wynik REAL,
        status text
    );
    """

    second_table = """
    -- second_table table
    CREATE TABLE IF NOT EXISTS second_table (
        strategy text NOT NULL,
        uwagi_techniczne text NOT NULL,
        data_wprowadzenia text,
        FOREIGN KEY (strategy) REFERENCES first_table (strategy)
    );
    """

    db.execute_sql(first_table)
    db.add_data('first_table', ("ma_cross", "prosta strategia przecięcia dwóch średnich kroczących",
                -23.55, "Wycofana"))
    db.add_data('first_table', ("monkey_strategy", "otwieranie i zamykanie losowo o losowych godzinach",
                                0.0, "Nie stosowana"))
    db.add_data('first_table', ("XGB_ML", "uczenie na podstawie doskonałych modeli bazujących na przeszłych notowaniach",
                                0.0, "Faza testowa"))

    db.execute_sql(second_table)
    db.add_data('second_table', ("ma_cross", "parametry zależne od backtestu", "2020-06-01"))
    db.add_data('second_table', ("XGB_ML", "tworzenie syntetycznych modeli służących jako dane do nauki modelu ML", "2023-10-01"))
    db.add_data('second_table', ("XGB_ML", "parametryzacja modelu uczącego", "2023-12-01"))

    input("Przystanek na sprawdzenie db")

    db.update('first_table', 'monkey_strategy', status='Faza testowa')

    input("Przystanek na sprawdzenie db")

    db.delete_all('second_table')
