from DbManagement import DbManagement


class Calculator:

    def __init__(self):
        self.main_menu = {"0": "Exit", "1": "CRUD operations", "2": "Show top ten companies by criteria"}
        self.crud_menu = {"0": "Back", "1": "Create a company", "2": "Read a company", "3": "Update a company",
                          "4": "Delete a company", "5": "List all companies"}
        self.top_ten = {"0": "Back", "1": "List by ND/EBITDA", "2": "List by ROE", "3": "List by ROA"}

    def __repr__(self):
        return "Welcome to the Investor Program!"

    def process_company_info(self, ticker, operation):
        if operation == "CREATE":
            ticker = input("Enter ticker (in the format 'MOON'):\n")
            company = input("Enter company (in the format 'Moon Corp'):\n")
            industries = input("Enter industries (in the format 'Technology'):\n")
        ebitda = input("Enter ebitda (in the format '987654321'):\n")
        sales = input("Enter sales (in the format '987654321'):\n")
        net_profit = input("Enter net profit (in the format '987654321'):\n")
        market_price = input("Enter market price (in the format '987654321'):\n")
        net_debt = input("Enter net debt (in the format '987654321'):\n")
        assets = input("Enter assets (in the format '987654321'):\n")
        equity = input("Enter equity (in the format '987654321'):\n")
        cash_equivalents = input("Enter cash equivalents (in the format '987654321'):\n")
        liability = input("Enter liabilities (in the format '987654321'):\n")

        if operation == "CREATE":
            DbManagement().create_company_entry(ticker, company, industries)
            DbManagement().create_financial_entry(ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity,
                                              cash_equivalents, liability)
            print("Company created successfully!")

        if operation == "UPDATE":
            DbManagement().update_financial_entry(ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity,
                                              cash_equivalents, liability)
            print("Company updated successfully!")


    def get_company_params(self, param, param1, param2):
        try:
            print(f"{param} = {round(param1 / param2, 2)}")
        except:
            print(f"{param} = None")

    def show_menu(self, menu_name, menu):
        print(menu_name)
        for number, option in menu.items():
            print(number, option, sep=' ', end="\n")

    def process_main_menu(self):
        inp = input("Enter an option:")
        if inp == "0":
            print("Have a nice day!")
            exit(0)
        elif inp == "1":
            self.show_menu("CRUD MENU", self.crud_menu)
            self.process_crud_menu()
        elif inp == "2":
            self.show_menu("TOP TEN MENU", self.top_ten)
            self.process_top_menu()
        else:
            print("Invalid option!")

    def process_top_menu(self):
        inp = input("Enter an option:")
        if inp == "1":
            DbManagement().get_top_ten("net_debt", "ebitda", "TICKER ND/EBITDA")
        elif inp == "2":
            DbManagement().get_top_ten("net_profit", "equity", "TICKER ROE")
        elif inp == "3":
            DbManagement().get_top_ten("net_profit", "assets", "TICKER ROA")
        else:
            print("Invalid option!")

    def process_crud_menu(self):
        inp = input("Enter an option:\n")
        if inp == "1":
            self.process_company_info("", "CREATE")
        if inp == "2":
            company_to_show = input("Enter company name:\n")
            companies_to_show = DbManagement().show_companies(company_to_show, "LIKE", "companies")
            if len(companies_to_show) > 0:
                print(*[f'{index} {x[1]}' for index, x in enumerate(companies_to_show)], sep="\n")
                company_ticker_to_read = companies_to_show[int(input("Enter company number:"))]
                print(company_ticker_to_read[0], company_ticker_to_read[1])
                company_to_read = DbManagement().show_companies(company_ticker_to_read[0], "=", "financial")[0]
                self.get_company_params("P/E", company_to_read[4], company_to_read[3])
                self.get_company_params("P/S", company_to_read[4], company_to_read[2])
                self.get_company_params("P/B", company_to_read[4], company_to_read[6])
                self.get_company_params("ND/EBITDA", company_to_read[5], company_to_read[1])
                self.get_company_params("ROE", company_to_read[3], company_to_read[7])
                self.get_company_params("ROA", company_to_read[3], company_to_read[6])
                self.get_company_params("L/A", company_to_read[9], company_to_read[6])

            else:
                print("Company not found!")
        if inp == "3":
            company_to_update = input("Enter company name:\n")
            try:
                companies_to_update = DbManagement().show_companies(company_to_update, "LIKE", "companies")
                print(*[f'{index} {x[1]}' for index, x in enumerate(companies_to_update)], sep="\n")
                company_ticker_to_update = companies_to_update[int(input("Enter company number:"))][0]
                company_to_update = DbManagement().show_companies(company_ticker_to_update, "=", "financial")
                self.process_company_info(company_to_update[0][0].lower(), "UPDATE")
            except Exception as e:
                print(e)
                print("Company not found!")
        if inp == "4":
            company_to_delete = input("Enter company name:\n")
            try:
                companies_to_delete = DbManagement().show_companies(company_to_delete, "LIKE", "companies")
                print(*[f'{index} {x[1]}' for index, x in enumerate(companies_to_delete)], sep="\n")
                company_ticker_to_delete = companies_to_delete[int(input("Enter company number:"))][0]
                DbManagement().delete_company(company_ticker_to_delete.lower())
                print("Company deleted successfully!")
            except Exception as e:
                print("Company not found!")
        if inp == "5":
            DbManagement().show_all_companies()

