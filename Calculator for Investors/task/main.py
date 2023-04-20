from DbManagement import DbManagement


class Calculator:

    def __init__(self):
        self.main_menu = {"0": "Exit", "1": "CRUD operations", "2": "Show top ten companies by criteria"}
        self.crud_menu = {"0": "Back", "1": "Create a company", "2": "Read a company", "3": "Update a company",
                          "4": "Delete a company", "5": "List all companies"}
        self.top_ten = {"0": "Back", "1": "List by ND/EBITDA", "2": "List by ROE", "3": "List by ROA"}

    def __repr__(self):
        return "Welcome to the Investor Program!"

    def process_company_info(self, operation):
        params = []
        if operation == "CREATE":
            for key, value in {"ticker": "MOON", "company": "Moon Corp", "industries": "Technology"}:
                params.append(input(f"Enter {key} (in the format '{value}'):\n"))
        for element in ('ebitda', 'sales', 'net_profit', 'market_price', 'net_debt', 'assets', 'equity', 'cash_equivalents', 'liability'):
            params.append(input(f"Enter {element} (in the format '987654321'):\n"))

        if operation == "CREATE":
            DbManagement().create_company_entry(params)
            DbManagement().create_financial_entry(params)
            print("Company created successfully!")

        if operation == "UPDATE":
            DbManagement().update_financial_entry(params)
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
            self.process_company_info("CREATE")
        if inp == "2":
            company_to_show = input("Enter company name:\n")
            companies_to_show = DbManagement().show_companies(company_to_show, "LIKE", "companies")
            if len(companies_to_show) > 0:
                print(*[f'{index} {x[1]}' for index, x in enumerate(companies_to_show)], sep="\n")
                company_ticker_to_read = companies_to_show[int(input("Enter company number:"))]
                print(company_ticker_to_read[0], company_ticker_to_read[1])
                company_to_read = DbManagement().show_companies(company_ticker_to_read[0], "=", "financial")[0]
                for key, value in {"P/E": [company_to_read[4], company_to_read[3]], "P/S": [company_to_read[4], company_to_read[2]],
                    "P/B": [company_to_read[4], company_to_read[6]], "ND/EBITDA": [company_to_read[5], company_to_read[1]],
                    "ROE": [company_to_read[3], company_to_read[7]], "ROA": [company_to_read[3], company_to_read[6]],
                    "L/A": [company_to_read[9], company_to_read[6]]}:
                    self.get_company_params(key, value[0], value[1])

            else:
                print("Company not found!")
        if inp == "3":
            company_to_update = input("Enter company name:\n")
            try:
                companies_to_update = DbManagement().show_companies(company_to_update, "LIKE", "companies")
                print(*[f'{index} {x[1]}' for index, x in enumerate(companies_to_update)], sep="\n")
                self.process_company_info("UPDATE")
            except:
                print("Company not found!")
        if inp == "4":
            company_to_delete = input("Enter company name:\n")
            try:
                companies_to_delete = DbManagement().show_companies(company_to_delete, "LIKE", "companies")
                print(*[f'{index} {x[1]}' for index, x in enumerate(companies_to_delete)], sep="\n")
                company_ticker_to_delete = companies_to_delete[int(input("Enter company number:"))][0]
                DbManagement().delete_company(company_ticker_to_delete.lower())
                print("Company deleted successfully!")
            except:
                print("Company not found!")
        if inp == "5":
            DbManagement().show_all_companies()
