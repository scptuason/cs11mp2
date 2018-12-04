# Enigma Engine
# Ryan Marcel Ibay (2018-21278)
# Shawn Christian Tuason (2018-02438)
# Please type your names and student numbers!

# File Editing (Cipher and Message):
def SaveItem(item, file_name):          # Lets you write a certain item on a file.
	file = open(file_name, "w")
	file.write(item)
	file = file.close()

def OpenItem(file_name):                # Lets you read a file, then returns the first item.
	file = open(file_name, "r")
	file_l = []
	for item in file:
		file_l.append(item)
	file.close()
	return file_l[0]

# Encrypting Algorithms:
def CaesarE(mode, message, key):        # Follows a Caesar Cipher mode; takes in a message and key;
	max_k = 26                      # each letter in the message will be replaced by its succeeding
	translated = ''                 # letter in accordance with the English alphabet.
	for symbol in message:          
		if symbol.isalpha():
			num = ord(symbol)
			num += key
			if symbol.isupper():
				if num > ord('Z'):
					num -= 26
				elif num < ord('A'):
					num += 26
			elif symbol.islower():
				if num > ord('z'):
					num -= 26
				elif num < ord('a'):
					num += 26

			translated += chr(num)
		else:
			translated += symbol

	return translated

def SubstitutionCipherE(mode, message, key):    # Takes in Substitution Cipher Mode, a message, and a key.
	alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	message = message.lower()               # Converts first the message to lowercase,
	message = list(message)                 # then makes it a list containing its letters;
	key = list(key)                         # it will also happen to the key.

	full_message = []

	for m in message:                       # Each letter of the message will be replaced
		if m == ' ':                    # by the corresponding letter in the encryption key.
			full_message.append(m)
		elif m in alph:
			for item in alph:
				if m == item:
					match = alph.index(item)
					code = key[match]
					full_message.append(code)
		else:
			full_message.append(m)
	s = ''
	return s.join(full_message)     

 # Decrypting Alogrithms
def CaesarD(mode, message, key):                        # Takes in Caesar Cipher Mode, a message, and a key.
	max_k = 26
	translated = ''
	key = -key                                      # For this mode, the key will be the negative value of the inputted key.
	for symbol in message:                          # Each letter in the encrypted message will be replaced by its
		if symbol.isalpha():                    # preceding letter in accordance with the English alphabet.
			num = ord(symbol)
			num += key
			if symbol.isupper():
				if num > ord('Z'):
					num -= 26
				elif num < ord('A'):
					num += 26
			elif symbol.islower():
				if num > ord('z'):
					num -= 26
				elif num < ord('a'):
					num += 26
			translated += chr(num)
		else:
			translated += symbol
	return translated

def SubstitutionCipherD(mode, message, key):            # Takes in Substitution Cipher Mode, a message, and a key.
	alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	message = message.lower()                       # Converts first the message to lowercase,
	message = list(message)                         # then makes it a list containing its letters;
	key = list(key)                                 # it will also happen to the key.
	full_message = []
	for m in message:	
		if m == ' ':
			full_message.append(m)
		elif m in key:
			for item in key:
				if m == item:
					match = key.index(item)
					code = alph[match]
					full_message.append(code)
		else:
			full_message.append(m)
	s = ''
	return s.join(full_message)
	if mode[0] == 'd' or 'D' or 'Decrypt' or 'decrypt':
		key = -key
