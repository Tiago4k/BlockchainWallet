from blockchain import Blockchain
from utility.verification import Verification
from uuid import uuid4

class Node:
    def __init__(self):
        #self.id = str(uuid4())
        self.id = 'Tiago'
        self.blockchain = Blockchain(self.id)


    def get_transaction_value(self):
        tx_recipient = input('Please enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        # Concatenates the 2 variables into a tuple
        return tx_recipient, tx_amount

    def get_user_choice(self):
        return input('Your choice: ')

    def print_block_elements(self):
        print('Outputting Block...')
        for block in self.blockchain.get_chain():
            print(block)
        else:
            print('*' * 40)

    def listen_for_input(self):
        quit_app = False

        while quit_app == False:
            print('\nPlease choose:')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output Blockchain')
            print('4: Output Balance')
            print('Q: Exit application')
            print('\n')

            user_choice = self.get_user_choice()
            print('\n')

            if user_choice == '1':
                tx_data = self.get_transaction_value()

                # Unpacks the data in tuple
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
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
                self.blockchain.mine_block()

            elif user_choice == '3':
                self.print_block_elements()

            elif user_choice == '4':
                print('*' * 40)
                print('{}\'s Current Balance: {:6.2f} \n'.format(self.id, self.blockchain.get_balance()))

            elif user_choice == 'Q' or user_choice == 'q':
                print('Quitting Application \n')
                quit_app = True

            else:
                print('Invalid Choice')

            if user_choice != 'Q' and user_choice != 'q' and user_choice != '4':
                print('\n')
                print('*' * 40)
                print('{}\'s Current Balance: {:6.2f}'.format(
                    self.id, self.blockchain.get_balance()))
                print('*' * 40)
                print('\n')

            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_block_elements()
                print('Invalid Blockchain!')
                break

        print('*' * 40)
        print('{}\'s Current Balance: {:6.2f} \n'.format(
            self.id, self.blockchain.get_balance()))
        print('Application Closed.')
        print('*' * 40, '\n')

node = Node()
node.listen_for_input() 