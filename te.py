import datetime
import hashlib
import uuid
from flask import Flask, request, render_template

class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0*0
    timestamp = datetime.datetime.now()
    block_id = None

    def __init__(self, data, name):
        self.data = data
        self.blockName = name
        self.block_id = uuid.uuid1()

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf8')+
        str(self.data).encode('utf8')+
        str(self.previous_hash).encode('utf8')+
        str(self.timestamp).encode('utf8')+
        str(self.blockName).encode('utf8'))

        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockName: " + str(self.blockName)+ "\nBlock Data: " + str(self.data) + "\nBlock Id:" + str(self.block_id) + "\nHashes: " + str(self.nonce) + "\n--------------"


class Blockchain:

    diff = 10
    maxNonce = 2**32
    target = 2**(256-diff)

    block = Block("Genesis text", "Genesis")
    dummy = head = block

    def add(self, block):
        block.previous_hash = self.block.hash()
        self.block.next = block
        self.block = self.block.next

    block_ids = {}


    def mine(self, block):
        if block.blockName in self.block_ids:
            block.block_id = self.block_ids[block.blockName]
        else:
            self.block_ids[block.blockName] = block.block_id
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                return block.blockName,block.data,block.block_id
            else:
                block.nonce += 1

    def get_by_id(self, block_id):
        # block_id = uuid.UUID(block_id_str)
        block_id = uuid.UUID(block_id)
        current_block = self.dummy.next
        while current_block is not None:
            if current_block.block_id.hex == block_id:
                return current_block
            current_block = current_block.next
        return None

app = Flask(__name__)
blockchain = Blockchain()
my_dict = []

@app.route('/')
def my_form():
    return render_template('index.html',content = "")

@app.route('/',methods=['POST', 'GET'])
def my_form_post():
	return okay()

def okay():
    if request.method == 'POST' and 'PatientName' in request.form:
        PatientName = request.form['PatientName']
        Details = request.form['Details']
        nm, tx, id = blockchain.mine(Block(Details, PatientName))
        my_dict.append([nm,tx,id])
        return render_template('index.html', name_list = my_dict)
	
    if request.method == 'POST' and 'block_id' in request.form:
        block_id = request.form['block_id']
        block = blockchain.get_by_id(block_id)
        if block is not None:
            return render_template('index.html', content="Block Name: " + block.blockName + "<br>" +
            "Block Data: " + block.data + "<br>" +
            "Block ID: " + block.block_id + "<br>" +
            "--------------")
        else:
            return render_template('index.html', content="Block with ID '{}' not found".format(block_id))
        return render_template('index.html')


if __name__=="__main__":
	app.run(debug=True)