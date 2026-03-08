import sqlite3
import os
from dotenv import load_dotenv
DB_URL = os.getenv("DB_URL")

conn = sqlite3.connect(DB_URL)
conn.row_factory = sqlite3.Row
c = conn.cursor()


show_month_range_query = """
    SELECT id, scrape_date
        FROM mdl_dfrt_check
        WHERE scrape_date >= datetime('now', '-30 days')
        ORDER BY scrape_date DESC;
        """
compare_query = """
    SELECT
        a.model_year,
        a.division,
        a.model,
        a.model_code,
        a.style_name,

        a.invoice_price AS invoice_old,
        b.invoice_price AS invoice_new,
        (b.invoice_price - a.invoice_price) AS invoice_diff,

        a.msrp_price AS msrp_old,
        b.msrp_price AS msrp_new,
        (b.msrp_price - a.msrp_price) AS msrp_diff,

        a.dfrt_price AS dfrt_old,
        b.dfrt_price AS dfrt_new,
        (b.dfrt_price - a.dfrt_price) AS dfrt_diff

    FROM mdl_dfrt_check a
    JOIN mdl_dfrt_check b
      ON a.model_code = b.model_code
     AND a.style_name = b.style_name

    WHERE date(a.scrape_date) = date(?)
      AND date(b.scrape_date) = date(?)

    ORDER BY a.division, a.model, a.style_name
    """

print("Select run range:")
print("1) Compare today with yesterday (or most recent day)")
print("2) Compare today with 7 days ago")
print("3) Compare today with 30 days ago")
print("4) Custom date range")

while True:
    choice = input("Choice: ")
    match choice:
        case "1": 
            break
        case "2":
            date1 = input("Start date (YYYY-MM-DD): ")
            date2 = input("End date (YYYY-MM-DD): ")
            break
        case "3":
            date1 = input("Start date (YYYY-MM-DD): ")
            date2 = input("End date (YYYY-MM-DD): ")
            break
        case "4":
            date1 = input("Start date (YYYY-MM-DD): ")
            date2 = input("End date (YYYY-MM-DD): ")
            break
        case _:
            print("Please select 1–4.")

c.execute(compare_query, (date1, date2))
rows = c.fetchall()

conn.close()