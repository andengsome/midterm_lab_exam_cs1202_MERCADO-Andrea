game_library = {
    1: {"Donkey Kong": {"copies_available": 3, "cost": 10}},
    2: {"Super Mario Bros": {"copies_available": 5, "cost": 15}},
    3: {"Tetris": {"copies_available": 2, "cost": 5}}
}

acc_lib = {}

def Avail_games():
    print("Available Games:")
    for index, game in game_library.items():
        game_name = list(game.keys())[0]
        copies_available = game[game_name]["copies_available"]
        cost = game[game_name]["cost"]
        print(f"{index}. {game_name} - Copies available: {copies_available}, Cost: ${cost}")

def register():
    while True:
        try:
            print("\n\nREGISTER PAGE")
            username = input("Please input username: ")
            password = input("Password (must be 8 characters long): ")
            if len(password) >= 8:
                if username in acc_lib:
                    print("Username already exists. Please choose another one.")
                else:
                    print("Account registered successfully.")
                    acc_lib[username] = {
                        "username": username,
                        "password": password,
                        "Balance": 0,
                        "Points": 0,
                        "rented_games": []
                    }
                    menu()
            else:
                print("Password must be at least 8 characters long.")
        except ValueError:
            print("Invalid input.")

def userlogin():
    print("\n\nLOGIN PAGE")
    username = input("Username: ")
    password = input("Password: ")
    if username in acc_lib and acc_lib[username]["password"] == password:
        print("Login Successful")
        user_menu(username)
    else:
        print("Invalid username or password.")

def adminlogin():
    print("\n\nADMIN LOGIN PAGE")
    admin = input("Username: ")
    adminpass = input("Password: ")
    
    if admin == "admin" and adminpass == "adminpass":
        print("Login Successful")
        admin_menu()
    else:
        print("Invalid admin credentials")

def user_menu(username):
    while True:
        print(f"\n\nLogged in as {username}")
        print("1. Rent a game")
        print("2. Return a game")
        print("3. Top-up Account")
        print("4. Display inventory")
        print("5. Redeem free game rental")
        print("6. Check Points")
        print("7. Log out")
        choice = input("Enter your choice: ")

        if choice == "1":
            rent_game(username)
        elif choice == "2":
            return_game(username)
        elif choice == "3":
            top_up(username)
        elif choice == "4":
            inventory(username)
        elif choice == "5":
            redeem(username)
        elif choice == "6":
            check_point(username)
        elif choice == "7":
            print("Logged out successful.")
            menu()
            break
        else:
            print("Please input a valid option. ")

def admin_menu():
    while True:
        print("Admin Menu")
        print("1. Update Game Details")
        print("2. Log out")

        choice = input("Enter your choice: ")

        if choice == "1":
            update_menu()
        elif choice == "2":
            print("Logged out successful.")
            menu()
            break
        else:
            print("Please input a valid option.")

def update_menu():
    print("Update Game Menu")
    print("1. Update game copies available")
    print("2. Update game cost")
    choice = input("Enter your choice: ")

    if choice == "1":
        update_game_copies()
    elif choice == "2":
        update_game_cost()
    else:
        print("Please input a valid option.")

def update_game_copies():
    Avail_games()
    try:
        game_choice = int(input("Enter the number of the game you want to update: "))
        if game_choice in game_library:
            game_name = list(game_library[game_choice].keys())[0]
            new_copies = int(input(f"Enter the new number of copies for {game_name}: "))
            game_library[game_choice][game_name]['copies_available'] = new_copies
            print(f"Updated copies available for {game_name}: {new_copies}")
        else:
            print("Invalid game choice.")
    except ValueError:
        print("Invalid input.")

def update_game_cost():
    Avail_games()
    try:
        game_choice = int(input("Enter the number of the game you want to update: "))
        if game_choice in game_library:
            game_name = list(game_library[game_choice].keys())[0]
            new_cost = float(input(f"Enter the new cost for {game_name}: "))
            game_library[game_choice][game_name]['cost'] = new_cost
            print(f"Updated cost for {game_name}: ${new_cost}")
        else:
            print("Invalid game choice.")
    except ValueError:
        print("Invalid input.")

def rent_game(username, free=False):
    Avail_games()
    try:
        game_choice = int(input("Please select a game to rent: "))
        if game_choice in game_library:
            game_name = list(game_library[game_choice].keys())[0]
            game_info = game_library[game_choice][game_name]

            if game_info['copies_available'] > 0:
                cost = 0 if free else game_info['cost']
                if acc_lib[username]['Balance'] >= cost:
                    print(f"{game_name} rented successfully.")
                    game_info['copies_available'] -= 1
                    acc_lib[username]['Balance'] -= cost
                    acc_lib[username]['rented_games'].append(game_name)
                    print(f"Your new balance: ${acc_lib[username]['Balance']:.2f}")
                    
                    if not free:
                        acc_lib[username]['Points'] += 1
                        print(f"Earned 1 point! You now have {acc_lib[username]['Points']} points.")
                else:
                    print("You do not have enough balance to rent this game.")
            else:
                print("Sorry, no copies available for renting.")
        else:
            print("Invalid game choice.")
    except ValueError:
        print("Invalid input.")

def return_game(username):
    rented_games = acc_lib[username].get('rented_games', [])
    if not rented_games:
        print("You have not rented any games.")
        return

    print("Rented Games:")
    for idx, game_name in enumerate(rented_games, start=1):
        print(f"{idx}. {game_name}")

    try:
        game_choice = int(input("Enter the number of the game you want to return: "))
        if 1 <= game_choice <= len(rented_games):
            game_name = rented_games[game_choice - 1]
            for game_id, game_info in game_library.items():
                if game_name in game_info:
                    game_info[game_name]['copies_available'] += 1
                    break
            
            rented_games.remove(game_name)
            print(f"{game_name} has been returned successfully.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def top_up(username):
    try:
        amount = float(input("Enter the amount you want to top-up: "))
        if amount > 0:
            acc_lib[username]['Balance'] += amount
            print(f"Successfully topped up ${amount:.2f}. Your new balance is ${acc_lib[username]['Balance']:.2f}.")
        else:
            print("Amount must be greater than 0.")
    except ValueError:
        print("Invalid input.")

def inventory(username):
    rented_games = acc_lib[username].get('rented_games', [])
    print("Your Inventory:")
    if rented_games:
        print("Rented Games:")
        for idx, game_name in enumerate(rented_games):
            print(f"{idx + 1}. {game_name}")
    else:
        print("You have not rented any games.")

    balance = acc_lib[username]['Balance']
    print(f"Account Balance: ${balance:.2f}")

def redeem(username):
    points = acc_lib[username]['Points']
    if points >= 10:
        acc_lib[username]['Points'] -= 10
        print("Redeemed a free game rental! 10 points deducted.")
        rent_game(username, free=True)
    else:
        print("You do not have enough points to redeem a free rental. You need at least 10 points.")

def check_point(username):
    points = acc_lib[username]['Points']
    print(f"You have {points} points.")

def menu():
    while True:
        try:
            print("Welcome to the Game Rental System")
            print("1. Display Available Games")
            print("2. Register User")
            print("3. Log in")
            print("4. Admin Log in")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                Avail_games()
            elif choice == "2":
                register()
            elif choice == "3":
                userlogin()
            elif choice == "4":
                adminlogin()
            elif choice == "5":
                print("Exiting the program. Goodbye!")
                return
            else:
                print("Please input a valid option.")
        except ValueError:
            print("Try again.")
            return

menu()