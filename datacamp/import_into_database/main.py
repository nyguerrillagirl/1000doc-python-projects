from sqlalchemy import create_engine
import pandas as pd


def import_into_database(df, db_table):
    # Create a PostgreSQL connection engine
    engine = create_engine("postgresql://datacamp:PASSWORD_HERE@localhost:5432/datacampdb")

    # Write DataFrame to PostgreSQL
    df.to_sql(
        name=db_table,
        con=engine,
        if_exists="replace",  # or "append"
        index=False
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_csv("students.csv")
    import_into_database(df, "students")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
