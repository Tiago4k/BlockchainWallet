# Initialise empty blockchain list
genesis_block = {'previous_hash': ' ', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
quit_app = False
open_transactions = []
owner = 'Tiago'


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# Adds a transaction that accepts 2 arguments, transaction_amount and last_transaction.
# last_transaction is an optional value as it has a default value if no value is assigned
# to the last_transaction parameter
def add_transaction(recipient, sender=owner, amount=1.0):

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''

    for key in last_block:
        values = last_block[key]
        hashed_block += str(values)

    print(hashed_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)


def get_transaction_value():
    tx_recipient = input('Please enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount


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
    print('2: Mine a new block')
    print('3: Output the blockchain')
    print('H: Manipulate chain')
    print('Q: Exit application')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()

        # Unpacks the data in tuple
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)

        print(open_transactions)

    elif user_choice == '2':
        mine_block()

    elif user_choice == '3':
        print_block_elements()

    elif user_choice == 'H':

        if len(blockchain) >= 1:
            # Sets the first element in the blockchain to 2
            blockchain[0] = [2]

    elif user_choice == 'Q':
        print('Quitting Application')
        quit_app = True

    else:
        print('Invalid Choice')

    # if not verify_chain():
    #     print('Invalid Blockchain!')
    #     break

print('Done.')
