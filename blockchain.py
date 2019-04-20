import functools
import hashlib
import json
# Reward given to miners for creating a new block
MINING_REWARD = 1.5
# Starting block for the blockchain
genesis_block = {
    'previous_hash': ' ',
    'index': 0,
    'transactions': []
}
# Initialise the empty blockchain list
blockchain = [genesis_block]
# Unhandled Transactions
open_transactions = []
# Owner of the blockchain node
owner = 'Tiago'
# Registered Participants: Ourselves & others sending/receiving coins
participants = {'Tiago'}


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()


def mine_block():
    """Create a new block and add open transactions to it."""
    # Fetch the currently last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block (=> to be able to compare it to the stored hash value)
    hashed_block = hash_block(last_block)

    # Miners should be rewarded, so let's create a reward transaction
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)

    return True

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


################################ Verification Functions ##############################################
def verify_transaction(transaction):
    """Verify a transaction by checking whether the sender has sufficient coins.

    Arguments:
        :transaction: The transaction that should be verified.
    """
    sender_balance = get_balance(transaction['sender'])

    return sender_balance >= transaction['amount']


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

########################################################################################################

######################################### Getter Functions #############################################
def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_transaction_value():
    tx_recipient = input('Please enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))

    # Concatenates the 2 variables into a tuple
    return tx_recipient, tx_amount


def get_balance(participants):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participants] for block in blockchain]
    
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participants]

    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participants] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    # Returns Total
    return amount_received - amount_sent

########################################################################################################

############################################ Printing Functions ########################################
def get_user_choice():
    return input('Your choice: ')


def print_block_elements():
    print('Outputting Block...')
    for block in blockchain:
        print(block)
    else:
        print('*' * 40)

########################################################################################################

quit_app = False

while quit_app == False:
    print('\nPlease choose:')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output Blockchain')
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
            print('*' * 40)
            print('Transaction Added!')

        else:
            print('\n')
            print('*' * 40)
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
        print('*' * 40)
        print('{}\'s Current Balance: {:6.2f}'.format(
            'Tiago', get_balance('Tiago')))
        print('*' * 40)

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
        print('*' * 40)
        print('{}\'s Current Balance: {:6.2f}'.format(
            'Tiago', get_balance('Tiago')))
        print('*' * 40)

    if not verify_chain():
        print_block_elements()
        print('Invalid Blockchain!')
        break

print('*' * 40)
print('{}\'s Current Balance: {:6.2f} \n'.format('Tiago', get_balance('Tiago')))
print('Application Closed.')
print('*' * 40, '\n')
