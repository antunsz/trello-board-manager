import re
from datetime import datetime, timedelta
from connection.connect import get_client

client = get_client()

#board = client.get_board('Vida')

board = [board for board in client.list_boards() if board.name == 'Vida'][0]

def _create_new_cards():
    # Get a specific list on the board by its name (assuming the list name is 'Backlog')
    backlog_list = None
    for list_obj in board.list_lists():
        if list_obj.name == 'Backlog':
            backlog_list = list_obj
            break

    if backlog_list is None:
        print("No list named 'Backlog' found!")
        return

    # Get card details from the user
    name = input('Digite o nome do card: ')
    points = input('Digite a quantidade de pontos: ')
    initial_date = input('Digite a data inicial (YYYY-MM-DD): ')
    final_date = input('Digite a data final (YYYY-MM-DD): ')

    # Convert the input dates to datetime objects
    initial_date = datetime.strptime(initial_date, "%Y-%m-%d")
    final_date = datetime.strptime(final_date, "%Y-%m-%d")

    # Create cards for each day in the date range
    current_date = initial_date
    while current_date <= final_date:
        # Create a card for the day
        new_card = backlog_list.add_card(f"({points}) {name}", f"{name} for {current_date.strftime('%Y-%m-%d')}")

        # Set the due date to 22:30 of the current day
        due_datetime = current_date + timedelta(hours=22, minutes=30)
        due_datetime = due_datetime.replace(tzinfo=None)
        new_card.set_due(due_datetime)

        # Move to the next day
        current_date += timedelta(days=1)




def _list_cards():
    list_names = ['Backlog', 'Todo', 'Doing', 'Done']

    # Loop through all lists in each board
    for list_obj in board.list_lists():
        if list_obj.name in list_names:
            print(f"  List: {list_obj.name}")

            # Loop through all cards in each list
            for card in list_obj.list_cards():
                print(f"    Card: {card.name}")

def _reports():
    # Regular expression pattern to find points within ()
    pattern = r'\((\d+)\)'

    # Loop through all boards
    print(f"Board: {board.name}")

    # Loop through all lists in each board
    for list_obj in board.list_lists():
        print(f"  List: {list_obj.name}")

        # Initialize sum of points for this list
        total_points = 0

        # Loop through all cards in each list
        for card in list_obj.list_cards():
            # Try to find points in the card name
            match = re.search(pattern, card.name)
            if match:
                points = int(match.group(1))  # Extract the first capturing group as an integer
                total_points += points
        
        print(f"    Total Points: {total_points}")


def _clear_done():
    # Initialize variables to keep track of earliest and latest dates
    earliest_date = None
    latest_date = None
    
    # List to keep track of 'Done' cards
    done_cards = []
    
    # Loop through all lists in each board
    for list_obj in board.list_lists():
        if list_obj.name == 'Done':
            # Loop through all cards in each 'Done' list
            for card in list_obj.list_cards():
                done_cards.append(card)

                # Convert due date string to datetime object
                due_date = datetime.strptime(card.due, "%Y-%m-%dT%H:%M:%S.%fZ") if card.due else None
                if due_date:
                    # Update earliest and latest dates
                    if earliest_date is None or due_date < earliest_date:
                        earliest_date = due_date
                    if latest_date is None or due_date > latest_date:
                        latest_date = due_date

    if earliest_date is None or latest_date is None:
        print("No cards with due dates in 'Done' lists.")
        return
    
    # Convert datetime to string
    earliest_date_str = earliest_date.strftime("%Y-%m-%d")
    latest_date_str = latest_date.strftime("%Y-%m-%d")
    
    # Create new list with name "Closed <earliest_date> - <latest_date>"
    new_list_name = f"Closed {earliest_date_str} - {latest_date_str}"
    board.add_list(new_list_name)
    
    # Move all cards to the new list
    new_list = board.get_list(new_list_name)
    for card in done_cards:
        card.change_list(new_list.id)

if __name__ == '__main__':
    while True:
        option = input("""
                       1 - Cadastrar novos cards
                       2 - Listar cards
                       3 - Limpar Done
                       4 - Relatório
                       5 - Sair
                       """)

        if option == '1':
            _create_new_cards()

        elif option == '2':
            _list_cards()

        elif option == '3':
            _clear_done()

        elif option == '4':
            _reports()

        elif option == '5':
            exit()
        else:
            print('Opção inválida')

