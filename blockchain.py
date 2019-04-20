MINING_REWARD = 1.5

# Initialise blockchain using genesis_block
# Using genesis_block allows us to add our first value
# to the blockchain without causing any errors
genesis_block = {'previous_hash': ' ', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
open_transactions = []
# Owner to become a dynamic variable
owner = 'Tiago'
participants = {'Tiago'}
quit_app = False


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])

    return sender_balance >= transaction['amount']


# Adds a transaction that accepts 3 arguments.
# Recipient must always be supplied whilst send and owner are optional.
# Function creates a dictonary and adds it to open_transactions
def add_transaction(recipient, sender=owner, amount=1.0):

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True

    return False


# Returns each key from the transaction dictonary in the blockchain
# and concatenates the keys by using a comprehension list
def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participants):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participants] for block in blockchain]

    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participants]

    tx_sender.append(open_tx_sender)

    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participants] for block in blockchain]

    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]

    return amount_received - amount_sent


def mine_block():
    last_block = blockchain[-1]

    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }

    open_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)

    return True


def get_transaction_value():
    tx_recipient = input('Please enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))

    # Concatenates the 2 variables into a tuple
    return tx_recipient, tx_amount


def get_user_choice():
    return input('Your choice: ')


def print_block_elements():
    print('Outputting Block...')
    for block in blockchain:
        print(block)
    else:
        print('*' * 30)


# Function to verify the blockchain. This prevents with tampering of the blockchain.
# Checks if the first block of a given chain matches the entire previous block's value
def verify_chain():
    """Verify the current block and returns True if it's valid, or False if it's not valid."""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


while quit_app == False:
    print('\nPlease choose:')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain')
    print('4: Output Participants')
    print('5: Output Balance')
    print('H: Manipulate chain')
    print('Q: Exit application')
    print('\n')

    user_choice = get_user_choice()
    print('\n')

    if user_choice == '1':
        tx_data = get_transaction_value()

        # Unpacks the data in tuple
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('\n')
            print('*' * 30)
            print('Transaction Added!')

        else:
            print('\n')
            print('*' * 30)
            print('Transaction Failed!')
            print('Insufficient Funds!')


        # print(open_transactions)

    elif user_choice == '2':
        if mine_block():
            open_transactions = []

    elif user_choice == '3':
        print_block_elements()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        pass

    elif user_choice == 'H' or user_choice == 'h':

        if len(blockchain) >= 1:
            # Tries to manipulate the blockchain by sending money from one account to the other without authority
            blockchain[0] = {
                'previous_hash': ' ',
                'index': 0,
                'transactions': [{'sender': 'Bob', 'recipient': 'Tiago', 'amount': 100}]
            }

    elif user_choice == 'Q' or user_choice == 'q':
        print('Quitting Application \n')
        quit_app = True

    else:
        print('Invalid Choice')

    if user_choice != 'Q' and user_choice != 'q':
        print('*' * 30)
        print("Current Balance: ", get_balance('Tiago'))
        print('*' * 30)
    
    if not verify_chain():
        print_block_elements()
        print('Invalid Blockchain!')
        break

print('*' * 30)
print("Current Balance: ", get_balance('Tiago'))
print('Application Closed.')
print('*' * 30, '\n')
