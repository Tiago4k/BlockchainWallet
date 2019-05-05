from blockchain import Blockchain
from utility.verification import Verification
from uuid import uuid4
from wallet import Wallet


class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.chain:
            print('Outputting Block')
            print(block)
        else:
            print('-' * 40)

    def listen_for_input(self):
        quit_app = False

        while quit_app == False:
            print('\nPlease choose:')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output Blockchain')
            print('4: Output Balance')
            print('5: Create Wallet')
            print('6: Load Wallet')
            print('7: Save Keys')
            print('Q: Exit application')
            print('\n')

            user_choice = self.get_user_choice()
            print('\n')

            if user_choice == '1':
                tx_data = self.get_transaction_value()

                # Unpacks the data in tuple
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('\n')
                    print('*' * 40)
                    print('Transaction Added!')

                else:
                    print('\n')
                    print('*' * 40)
                    print('Transaction Failed!')
                    print('Insufficient Funds!')

                print(self.blockchain.get_open_transactions())

            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining Failed! Got a wallet?')

            elif user_choice == '3':
                self.print_block_elements()

            elif user_choice == '4':
                print('*' * 40)
                print('{}\'s Current Balance: {:6.2f} \n'.format(
                    self.wallet.public_key, self.blockchain.get_balance()))

            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '7':
                self.wallet.save_keys()

            elif user_choice == 'Q' or user_choice == 'q':
                print('Quitting Application \n')
                quit_app = True

            else:
                print('Invalid Choice')

            if user_choice != 'Q' and user_choice != 'q' and user_choice != '4':
                print('\n')
                print('*' * 40)
                print('{} Current Balance: {:6.2f}'.format(
                    self.wallet.public_key, self.blockchain.get_balance()))
                print('*' * 40)
                print('\n')

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_block_elements()
                print('Invalid Blockchain!')
                break

            print('Balance of {}: {:6.2f}'.format(
                self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('User left!')

        print('Done!')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
