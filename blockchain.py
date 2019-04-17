# Initialise empty blockchain list
blockchain = []
quit_app = False


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# Adds a transaction that accepts 2 arguments, transaction_amount and last_transaction.
# last_transaction is an optional value as it has a default value if no value is assigned
# to the last_transaction parameter
def add_transaction(transaction_amount, last_transaction=[1]):
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    return float(input('Your transaction amount please: '))


def get_user_choice():
    return input('Your choice: ')


def print_block_elements():
    print('Outputting Block...')
    for block in blockchain:
        print(block)
    else:
        print('*' * 20)


# Function to verify the blockchain. This prevents with tampering of the blockchain.
# Checks if the first block of a given chain matches the entire previous block's value
def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        # Check if the current block contains the values of the previous block
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid


while quit_app == False:
    print('Please choose:')
    print('1: Add a new transaction value')
    print('2: Output the blockchain')
    print('3: Manipulate chain')
    print('4: Exit application')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())

    elif user_choice == '2':
        print_block_elements()

    elif user_choice == '3':

        if len(blockchain) >= 1:
            # Sets the first element in the blockchain to 2
            blockchain[0] = [2]

    elif user_choice == '4':
        print('Quitting Application')
        quit_app = True

    else:
        print('Invalid Choice')

    if not verify_chain():
        print('Invalid Blockchain!')
        break

print('Done.')
