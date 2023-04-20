import csv
import sqlite3


conn = sqlite3.connect('investor.db')
c = conn.cursor()


class DbManagement:

    def repl(self, row):
        return [None if x.strip() == "" else x for x in row]

    def create_companies_table(self):
        c.execute("CREATE TABLE IF NOT EXISTS companies (ticker VARCHAR PRIMARY KEY, name VARCHAR, sector VARCHAR);")
        conn.commit()

    def create_financial_table(self):
        c.execute('''CREATE TABLE IF NOT EXISTS financial (ticker VARCHAR PRIMARY KEY, ebitda FLOAT, sales FLOAT, 
        net_profit FLOAT, market_price FLOAT,  net_debt FLOAT,  
        assets FLOAT, equity FLOAT, cash_equivalents FLOAT, liabilities FLOAT);''')
        conn.commit()

    def read_csv(self, filename, operation):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                row = self.repl(row)
                if operation == "create_company":
                    self.create_company_entry(row[0], row[1], row[2])
                elif operation == "create_financial":
                    self.create_financial_entry(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    def create_company_entry(self, *args):
        c.execute("INSERT INTO companies (ticker, name, sector) VALUES (?, ?, ?)", args)
        conn.commit()

    def create_financial_entry(self, *args):
        c.execute(
            "INSERT INTO financial (ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)
        conn.commit()

    def update_financial_entry(self, *args):
        c.execute(f"UPDATE financial SET ebitda = ?, sales = ?, net_profit = ?, market_price = ?, net_debt = ?, assets = ?, equity = ?, cash_equivalents = ?, liabilities = ? WHERE LOWER(ticker) = ?", args)
        conn.commit()

    def delete_company(self, company):
        c.execute(f"DELETE FROM companies WHERE LOWER(ticker) = ?", (company,))
        c.execute(f"DELETE FROM financial WHERE LOWER(ticker) = ?", (company,))
        conn.commit()

    def get_top_ten(self, param1, param2, param3):
        result = c.execute(f"""SELECT ticker, ROUND({param1} / {param2}, 2) 
                                      FROM financial
                                      ORDER BY ROUND({param1} / {param2}, 2) DESC
                                      LIMIT 10""").fetchall()
        print(param3)
        for entry in result:
            print(entry[0], entry[1])

    def show_all_companies(self):
        c.execute(f"SELECT ticker, name, sector FROM companies ORDER BY ticker")
        result = c.fetchall()
        print("COMPANY LIST")
        for entry in result:
            print(*entry, end="\n")

    def show_companies(self, companies_to_show, operator, table):
        if operator == "LIKE":
            name = f'%{companies_to_show.lower()}%'
            what_to_find = "name"
        elif operator == "=":
            name = companies_to_show.lower()
            what_to_find = "ticker"
        c.execute(f"SELECT * FROM {table} WHERE LOWER({what_to_find}) {operator} ?", (name,))
        result = c.fetchall()
        conn.commit()
        return result


try:
    DbManagement().create_companies_table()
    DbManagement().create_financial_table()
    DbManagement().read_csv('test/companies.csv', "create_company")
    DbManagement().read_csv('test/financial.csv', "create_financial")
except:
    pass
