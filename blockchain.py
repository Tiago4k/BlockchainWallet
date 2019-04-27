import functools
import hashlib
import json
import pickle

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

# Reward given to miners for creating a new block
MINING_REWARD = 5.5
# Initialise the empty blockchain list
blockchain = []
# Unhandled Transactions
open_transactions = []
# Owner of the blockchain node
owner = 'Tiago'


def load_data():
    """Initialize blockchain + open transactions data from a file."""
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            blockchain = json.loads(file_content[0][:-1])
            # We need to convert  the loaded data because Transactions should use OrderedDict
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(
                    tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(
                    block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])

                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            # We need to convert  the loaded data because Transactions should use OrderedDict
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions

    except (IOError, IndexError):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initialising empty blockchain list
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = []


load_data()


def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                                                                 tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # save_data = {
            #     'chain' : blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving Failed!')


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participants):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender ==
                  participants] for block in blockchain]

    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [
        tx.amount for tx in open_transactions if tx.sender == participants]

    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participants] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(
        tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    # Returns Total
    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# Adds a transaction that accepts 3 arguments.
# Recipient must always be supplied whilst send and owner are optional.
# Function creates a dictonary and adds it to open_transactions
def add_transaction(recipient, sender=owner, amount=1.0):

    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it."""
    # Fetch the currently last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block (=> to be able to compare it to the stored hash value)

    hashed_block = hash_block(last_block)

    proof = proof_of_work()
    # Miners should be rewarded, so let's create a reward transaction
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)

    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)

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
        print('*' * 40)


quit_app = False

while quit_app == False:
    print('\nPlease choose:')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output Blockchain')
    print('4: Output Balance')
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
            save_data()

    elif user_choice == '3':
        print_block_elements()

    elif user_choice == '4':
        pass

    elif user_choice == 'Q' or user_choice == 'q':
        print('Quitting Application \n')
        quit_app = True

    else:
        print('Invalid Choice')

    if user_choice != 'Q' and user_choice != 'q' and user_choice != '4':
        print('\n')
        print('*' * 40)
        print('{}\'s Current Balance: {:6.2f}'.format(
            'Tiago', get_balance('Tiago')))
        print('*' * 40)
        print('\n')
    
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_block_elements()
        print('Invalid Blockchain!')
        break

print('*' * 40)
print('{}\'s Current Balance: {:6.2f} \n'.format('Tiago', get_balance('Tiago')))
print('Application Closed.')
print('*' * 40, '\n')
