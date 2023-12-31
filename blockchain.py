import hashlib 
import json 
from time import time 

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the Genesis Block (Block with no predecessor)
        self.new_block(previous_hash=1, proof = 100)

    def new_block(self,proof, previous_hash = None):
        # Creats a new Block and adds it to the chain
        """
        Structure: 
            proof: <int> The proof given by the Proof of Work algorithm
            previous_hash: <str> Hash of previous Block 
            return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': self.hash(self.chain[-1])
        }

        # Reset the curretn list of transactions 
        self.current_transactions = []

        self.chain.append(block)
        return block
        
    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions 
        """ Creates a new transaction to go into the next mined Block 
        Structure:
            sender:<str> Address of the Sender 
            recipient: <str> Address of the Sender 
            ammount: <int> Amount 
            return: <int> The index of the Block that will hold the current transaction
        """
        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,

        })
        
        return self.last_block['index'] + 1 

    @staticmethod
    def hash(block):
        # Hashes a Block 
        pass 
    
    @property
    def last_block(self):
        # Returns the last Block in that chain 
        pass 
