from main import Calculator


if __name__ == '__main__':

    calculator = Calculator()
    print(calculator)

    while True:
        calculator.show_menu("MAIN MENU", calculator.main_menu)
        calculator.process_main_menu()

    conn.close()
