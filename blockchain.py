import hashlib 
import json 
from time import time 
from uuid import uuid4
from textwrap import dedent
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the Genesis Block (Block with no predecessor)
        self.new_block(previous_hash=1, proof = 100)

    def new_block(self,proof, previous_hash = None):
        # Creats a new Block and adds it to the chain
        """
        
            proof: <int> The proof given by the Proof of Work algorithm
            previous_hash: <str> Hash of previous Block 
            return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        # Reset the curretn list of transactions 
        self.current_transactions = []

        self.chain.append(block)
        return block
        
    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions 
        """ Creates a new transaction to go into the next mined Block 
        
            sender:<str> Address of the Sender 
            recipient: <str> Address of the Sender 
            ammount: <int> Amount 
            return: <int> The index of the Block that will hold the current transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,

        })
        
        return self.last_block['index'] + 1 
    
    def proof_of_work(self, last_proof):
        """
        Proof of Work Algorithm:
            Find a number p such that hash(pp`) contains leading 4 zeros, where p is the previous p`
            p is the previos proof and p` is the new proof 
        last_proof: <int,
        return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof +=1 

        return proof
    
    def valid_proof(self,last_proof,proof):
        """
        Validates the Proof: Does the hash contain 4 leading zeros 
            last_proof: <int> Previous Proof 
            proof: <int> Current Proof 
            return: <bool> Treu if correct, False if not 
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        # Hashes a Block 
        """
        Create a SHA-256 hash of a Block 
            block: <dict> Block 
            return: <str>
        """
        
        # We must make sure the the Dictionary is Ordered or we'll have inconsistent hashes 
    
    @property
    def last_block(self):
        # Returns the last Block in that chain 
        return self.chain[-1]
    
    def register_node(self,address):
        """
        Add a new node to the list of nodes
        address: <str> Address of node. Eg.
        'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    def valid_chain(self, chain):
        """
        Determine if a give blockchain is valid 
        :param chain: <list> a blockchain 
        :return: <bool> True if valid, False if not 
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            #Check that the hash of the block is correct 
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            #Check that the Proof of Work is correct 
            if not self.valid_proof(last_block['proof'],block['proof']):
                return False
            
            last_block = block 
            current_index += 1 

        return True 
    
    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts 
        by replacing our chain with the longest one in the network.
        :return: <bool> True if the chain was replaced False if not
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for the chains longer than ours max_lenght = len(self.chain)

        # Grab and verift and chains from all the nodes in our network 
        for node in neighbours:
            response = request.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
            
        # Replace our chain if we discovers a new, valid chain longer than ours 
                    
        if new_chain:
            self.chain = new_chain
            return True 
        return False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# Update the get_chain function
@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('node')
    if nodes is None:
        return "Error: Please supply a valid list of nodes",400
    
    for node in nodes: 
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)