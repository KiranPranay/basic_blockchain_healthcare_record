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
		return "Block Hash: " + str(self.hash()) + "\nBlockName: " + str(self.blockName)+ "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"


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
	
	
app = Flask(__name__)
blockchain = Blockchain()
my_dict = []

@app.route('/')
def my_form():
	return render_template('index.html',content = "")

@app.route('/',methods=['POST', 'GET'])
def my_form_post():
	PatientName = request.form['PatientName']
	Details = request.form['Details']
	
	nm, tx, id = blockchain.mine(Block(Details, PatientName))
	my_dict.append([nm,tx,id])
	return render_template('index.html', name_list = my_dict)

if __name__=="__main__":
	app.run(debug=True)