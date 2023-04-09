#username - noamshaib, kochavap
#id1      - 209277888
#name1    - noam shaib
#id2      - 208910117
#name2    - kochava pavlov

import math
import random

"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type value: str
	@param value: data of your node
	"""
	def __init__(self, value=None):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0



	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		return self.right

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def getParent(self):
		return self.parent

	"""return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""
	def getValue(self):
		return self.value

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def getHeight(self):
		return self.height

	"""returns the size

		@rtype: int
		@returns: the size of self, 0 if the node is virtual
		"""

	def getSize(self):
		return self.size


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.left = node


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node

	"""sets value

	@type value: str
	@param value: data
	"""
	def setValue(self, value):
		self.value = value

	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, h):
		self.height = h

	"""sets the size of the node

		@type s: int
		@param s: the size
		"""

	def setSize(self, s):
		self.size = s

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		return self.value is not None


"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		self.len = 0
		self.firstval = None
		self.lastval = None
		# add your fields here


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.root is None


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if i >= self.len or i < 0:
			return None
		return self.find(i+1).getValue()


	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):
		fixNum = 0
		if self.root is None:							#the tree is empty
			self.root = AVLNode(val)
			self.root.left = AVLNode()
			self.root.right = AVLNode()
			self.root.size = 1
			self.root.height = 0
			self.len += 1
			self.lastval = val
			self.firstval = val  # the first and the last nodes are root
			return fixNum
		elif i == self.len:   							#the max index
			a = self.root
			while a.right.value is not None:			#size fixed inside
				a.size += 1
				a = a.right
			a.size += 1
			a.right.value = val				#update val
			a.right.left = AVLNode()		#update left child
			a.right.right = AVLNode()		#update right child
			a.right.parent = a				#update parent
			a.right.size = 1				#update size
			a.right.height = 0
			self.len += 1
			#a is the parent of the inserted node
			self.lastval = val							#update the last node on the "list"
		else:   #i<len
			curr = self.find(i+1)
			if curr.left.value is None:
				a = curr    							#a is the parent of the inserted node
				curr.left.value = val
				curr.left.parent = curr
				curr = curr.left
				curr.left = AVLNode()
				curr.right = AVLNode()
				curr.size = 1
				curr.height = 0
				self.len += 1
				if i == 0:
					self.firstval = val
			else:
				pre = self.predecessor(curr)
				a = pre        #a is the parent of the inserted node
				pre.right.value = val
				pre.right.parent = pre
				pre = pre.right
				pre.right = AVLNode()
				pre.left = AVLNode()
				pre.size = 1
				pre.height = 0
				self.len += 1
			s = a
			while s is not None:
				s.size += 1
				s = s.parent


		while a is not None:	 	#fix the height
			tmp = a.height
			a.height = max(a.left.height, a.right.height) + 1
			bf = a.left.height - a.right.height
			if abs(bf) < 2 and tmp == a.height:
				return fixNum
			elif abs(bf) < 2 and tmp != a.height:
				a = a.parent
			else: #abs(bf)=2
				fixNum += self.rotate(a, bf)
				a = a.parent

		return fixNum


	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		if i >= self.len or i < 0:		#if index i not exist
			return -1
		else:
			fixNum = 0
			y = self.find(i+1)
			if i == 0:
				if self.len == 1:												#delete the root and len=1
					self.firstval = None
				else:															#delete the root and suc(0) exsist
					self.firstval = self.successor(y).value
			if i == self.len-1:
				if self.len == 1:												#len=1 so i=0, the last is None
					self.lastval = None
				else:															#prede() exist
					self.lastval = self.predecessor(y).value
			if y.right.value is None and y.left.value is None:					#y is leaf
				self.deleteleaf(y)
				y = y.parent													#y is the parent of the deleted node
			elif y.right.value is None and y.left.value is not None:			#y has *only* left son
				self.deletewithoneleftson(y)
				y = y.parent													#y is the parent of the deleted node
			elif y.right.value is not None and y.left.value is None:			# y has *only* right son
				self.deletewithonerightson(y)
				y = y.parent													#y is the parent of the deleted node
			else:																# y has two sons
				z = self.successor(y)
				if z.right.value is None and z.left.value is None:  			# z is leaf
					self.deleteleaf(z)
				else:															#z has only right son
					self.deletewithonerightson(z)
				y.value = z.value														#replace y's value to z
				y = z.parent													#y is the parent of the deleted node (z.parent hasnt chacged after deletation)

			if y is not None:
				if y.parent is not None:
					s = y.parent
					while s is not None:
						s.size -= 1
						s = s.parent

			while y is not None:
				oldheight = y.height
				y.height = max(y.left.height, y.right.height) + 1
				bf = y.left.height - y.right.height
				if abs(bf) < 2 and oldheight == y.height:
					self.len -= 1
					return fixNum
				elif abs(bf) < 2 and oldheight != y.height:
					y = y.parent
				else:									#bf=2
					tmp = y.parent						#y's parent maybe chance after rotation
					fixNum += self.rotate(y, bf)		#fix the tree and add rotations
					y = tmp
		self.len -= 1
		return fixNum

	def deleteleaf(self, y):
		if self.root is y:  													# y is the root
			self.root = None
		else:  																	# y is not the root
			if y.parent.right is y:  											# y is right son of his parent
				y.parent.right = AVLNode()
			else:  																# y is left son of his parent
				y.parent.left = AVLNode()
		y = y.parent  															# change the pointer y to y's parent (also if None)
		if y is not None:  														# fix only the size of parent (the height not because needed)
			y.size -= 1

	def deletewithoneleftson(self, y):												# y has *only* left son
		if self.root is y:
			self.root = y.left
		else:  																	# y is not root
			if y.parent.left is y:  											# y is left son of his parent
				y.parent.left = y.left
			else:  																# y is right son of his parent
				y.parent.right = y.left
		y.left.parent = y.parent
		y = y.parent  															# change the pointer y to y's parent (also if None)
		if y is not None:														# fix only the size of parent (the height not because needed)
			y.size -= 1

	def deletewithonerightson(self, y):											# y has *only* right son
		if self.root is y:
			self.root = y.right
		else:  																	# y is not root
			if y.parent.left is y:  											# y is left son of his parent
				y.parent.left = y.right
			else:  																# y is right son of his parent
				y.parent.right = y.right
		y.right.parent = y.parent
		y = y.parent  															# change the pointer y to y's parent (also if None)
		if y is not None:														# fix only the size of parent (the height not because needed)
			y.size -= 1



	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		return self.firstval

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		return self.lastval

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		L = []
		if self.len == 0:
			return L
		self.inOrderLTARec(self.root, L)
		return L

	def inOrderLTARec(self, node, array):
		if node.getValue() is not None:  # node is not virtual
			self.inOrderLTARec(node.left, array)
			array.append(node.getValue())
			self.inOrderLTARec(node.right, array)

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return self.len

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""

	def sort(self):
		arrayOfvals = self.listToArray()
		sortedArrayOfVals = self.mergesort(arrayOfvals)
		returnVal = AVLTreeList()
		returnVal.root = self.arrayToAVL(sortedArrayOfVals, 0, len(sortedArrayOfVals) - 1)
		returnVal.len = returnVal.root.size
		return returnVal

	def merge(self, A, B):
		n = len(A)
		m = len(B)
		C = [None for i in range(n + m)]

		a = 0
		b = 0
		c = 0
		while a < n and b < m:  # more element in both A and B
			if A[a] < B[b]:
				C[c] = A[a]
				a += 1
			else:
				C[c] = B[b]
				b += 1
			c += 1

		C[c:] = A[a:] + B[b:]  # append remaining elements (one of those is empty)

		return C

	def mergesort(self, lst):
		n = len(lst)
		if n <= 1:
			return lst
		else:  # two recursive calls, then merge
			return self.merge(self.mergesort(lst[0:n // 2]), self.mergesort(lst[n // 2:n]))

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""

	def permutation(self):
		arrayOfVals = self.listToArray()
		for i in range(len(arrayOfVals) - 1, 0, -1):
			j = random.randint(0, i + 1)
			arrayOfVals[i], arrayOfVals[j] = arrayOfVals[j], arrayOfVals[i]
		returnVal = AVLTreeList()
		returnVal.root = self.arrayToAVL(arrayOfVals, 0, self.len - 1)
		returnVal.len = returnVal.root.size
		return returnVal


	def arrayToAVL(self, array, firstInsex, lastIndex):
		if firstInsex > lastIndex:
			return AVLNode()
		medianIndex = math.ceil((lastIndex + firstInsex) / 2)
		currentRootVal = array[medianIndex]
		currentRoot = AVLNode(currentRootVal)  # define the "root" of this sub-tree
		currentRoot.left = self.arrayToAVL(array, firstInsex, medianIndex - 1)
		currentRoot.right = self.arrayToAVL(array, medianIndex + 1, lastIndex)
		if currentRoot.left.value is not None:  # left child is a real node
			currentRoot.left.parent = currentRoot
		if currentRoot.right.value is not None:  # right child is a real node
			currentRoot.right.parent = currentRoot
		currentRoot.height = max(currentRoot.left.height, currentRoot.right.height) + 1
		currentRoot.size = currentRoot.left.size + currentRoot.right.size + 1
		return currentRoot


	"""concatenates lst to self, after this method lst changes
	
	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		if self.len == 0 and lst.len == 0:
			return 0
		if self.len == 0:
			self.root = lst.root
			self.len = lst.len
			self.firstval = lst.firstval
			self.lastval = lst.lastval
			lst.root = None
			lst.len = 0
			lst.firstval = None
			lst.lastval = None
			return self.root.height
		if lst.len == 0:
			return self.root.height
		returnVal = abs(self.root.height - lst.root.height)
		newLast = lst.lastval
		if self.root.height <= lst.root.height:     # lst is higher or same height
			if self.len == 1:
				lst.insert(0, self.root.value)
				self.root = lst.root
				self.len = lst.len
				self.firstval = lst.firstval
				self.lastval = lst.lastval
				lst.root = None
				lst.len = 0
				lst.firstval = None
				lst.lastval = None
				return returnVal
			xVal = self.lastval
			self.delete(self.len - 1)               # delete x
			x = AVLNode(xVal)
			x.height = 0
			x.size = 1
			a = self.root
			b = lst.root
			c = None
			while b.height > a.height:				# stop when b.height <= a.height(=h)
				c = b
				b = b.left
			x.left = a
			a.parent = x
			x.right = b
			b.parent = x
			if c is None:									# b is root, so x is new root
				self.root = x
				x.height = a.height + 1                     # a.height = h, b.height = h or h-1
				x.size = x.left.size + x.right.size + 1
			else:
				c.left = x
				x.parent = c
				x.height = a.height + 1 					#a.height = h, b.height = h or h-1
				x.size = x.left.size + x.right.size + 1
				c.size = c.left.size + c.right.size + 1
				self.root = lst.root

		else:                                               # self is higher
			if lst.len == 1:
				self.insert(self.len, lst.root.value)
				lst.root = None
				lst.len = 0
				lst.firstval = None
				lst.lastval = None
				return returnVal
			xVal = lst.firstval
			lst.delete(0)                                   # delete x
			x = AVLNode(xVal)
			x.height = 0
			x.size = 1
			a = lst.root
			b = self.root
			c = None
			while b.height > a.height:                     # stop when b.height <= a.height(=h)
				c = b
				b = b.right
			x.left = b
			b.parent = x
			x.right = a
			a.parent = x
			if c is None:                                   # b is root, so x is new root
				self.root = x
				x.height = a.height + 1                     # a.height = h, b.height = h or h-1
				x.size = x.left.size + x.right.size + 1
			else:
				c.right = x
				x.parent = c
				x.height = a.height + 1                     # a.height = h, b.height = h of h-1
				x.size = x.left.size + x.right.size + 1

		while c is not None:
			c.height = max(c.left.height, c.right.height) + 1
			c.size = c.left.size + c.right.size + 1
			bf = c.left.height - c.right.height
			if abs(bf) < 2:
				c.size = c.left.size + c.right.size + 1
				c = c.parent
			else:                             # |bf| >= 2
				tmp = c.parent                # c's parent may chance after rotation
				self.rotate(c, bf)            # fix the tree and add rotations
				c = tmp
		self.lastval = newLast
		self.len = self.root.size
		lst.root = None
		lst.len = 0
		lst.firstval = None
		lst.lastval = None
		return returnVal

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		L = self.listToArray()
		for i in range(len(L)):
			if L[i] == val:
				return i
		return -1

	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return self.root

	"returns the node in index 0<=i<len (rank i+1)"
	def find(self, i):
		return self.findRec(self.root, i)

	def findRec(self, a, i):
		r = a.left.size + 1
		if i == r:
			return a
		if i < r:
			return self.findRec(a.left, i)
		else:  # (i > r)
			return self.findRec(a.right, i - r)

	"""fix the tree after insert\delete\concat

		@rtype: AVLNode
		@returns: None
		"""

	def rotate(self, y, bf):
		if bf == -2:
			yr = y.right
			bf_yr = yr.left.height - yr.right.height
			if bf_yr == 0 or bf_yr == -1:
				self.lefttrot(y)
				return 1
			else: #bf_yr = 1
				self.rightrot(y.right)
				self.lefttrot(y)
				return 2
		else: #bf == 2
			yl = y.left
			bf_yl = yl.left.height - yl.right.height
			if bf_yl == 0 or bf_yl == 1:
				self.rightrot(y)
				return 1
			else: #bf_yr = -1
				self.lefttrot(y.left)
				self.rightrot(y)
				return 2

	def rightrot(self, c):		#turn right the bow BC   b is c.right and c is the c
		b = c.left
		br = b.right
		if self.root is c:					#change the parent pointer
			self.root = b
		else:
			if c.parent.right is c:			#c is a right son of his parent
				c.parent.right = b
			else:							#c is a left son of his parent
				c.parent.left = b
		#the rotation
		b.parent = c.parent
		b.right = c
		c.parent = b
		c.left = br
		br.parent = c
		#fix the height:
		c.height = max(c.right.height, c.left.height)+1
		b.height = max(b.right.height, b.left.height)+1
		#fix the size:
		c.size = c.right.size + c.left.size + 1
		b.size = b.right.size + b.left.size + 1

	def lefttrot(self, a):		#turn left the bow AB  b is c.right (a is the criminal *or* the son of the criminal)
		b = a.right
		bl = b.left
		if self.root is a:					#change the parent pointer
			self.root = b
		else:
			if a.parent.right is a:			#a is right son of his parent
				a.parent.right = b
			else:							#a is left son of his parent
				a.parent.left = b
		#the rotation:
		b.parent = a.parent
		b.left = a
		a.parent = b
		a.right = bl
		bl.parent = a
		#fix the height:
		a.height = max(a.right.height, a.left.height)+1
		b.height = max(b.right.height, b.left.height)+1
		#fix the size:
		a.size = a.right.size + a.left.size + 1
		b.size = b.right.size + b.left.size + 1



	"""finds the successor

					@rtype: AVLNode
					@returns: Node if exist, None if not
					"""

	def successor(self, currentNode):
		succ = currentNode                          #the node that the func will return
		if currentNode.right.value is not None:     #curr has a right child
			succ = currentNode.right
			while succ.left.value is not None:      #find the minimun in this sub tree
				succ = succ.left
			return succ
		else:                                       #curr doesnt have a right child
			if self.root is currentNode:
				return None
			previousNodeVisited = succ
			succ = succ.parent
			while succ is not None:                 #find the first time prev is a lef child
				if succ.left is previousNodeVisited:
					return succ
				previousNodeVisited = succ
				succ = succ.parent
		return None


	"""finds the predecessor

				@rtype: AVLNode
				@returns: Node if exist, None if not
				"""

	def predecessor(self, currentNode):
		pre = currentNode                          #the node that the func will return
		if currentNode.left.value is not None:     #curr has a left child
			pre = currentNode.left
			while pre.right.value is not None:      #find the maximum in this sub tree
				pre = pre.right
			return pre
		else:                                       #curr doesnt have a left child
			if self.root is currentNode:
				return None
			previousNodeVisited = pre
			pre = pre.parent
			while pre is not None:                 #find the first time prev is a lef child
				if pre.right is previousNodeVisited:
					return pre
				previousNodeVisited = pre
				pre = pre.parent
		return None


