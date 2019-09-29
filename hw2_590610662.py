FIXED_IP = [2, 6, 3, 1, 4, 8, 5, 7]
FIXED_EP = [4, 1, 2, 3, 2, 3, 4, 1]
FIXED_IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
FIXED_P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
FIXED_P8 = [6, 3, 7, 4, 8, 5, 10, 9]
FIXED_P4 = [2, 4, 3, 1]
 
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]
 
S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]
 
 
def permutate(original, fixed_key):
    new = ''
    for i in fixed_key:
        new += original[i - 1]
    return new
 
 
def left_half(bits):
    return bits[:len(bits)//2]
 
 
def right_half(bits):
    return bits[len(bits)//2:]
 
 
def shift(bits):
    rotated_left_half = left_half(bits)[1:] + left_half(bits)[0]
    rotated_right_half = right_half(bits)[1:] + right_half(bits)[0]
    return rotated_left_half + rotated_right_half
 
 
def key1(K):
    return permutate(shift(permutate(K, FIXED_P10)), FIXED_P8)
 
 
def key2(K):
    return permutate(shift(shift(shift(permutate(K, FIXED_P10)))), FIXED_P8)
 
 
def xor(bits, key):
    new = ''
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new
 
 
def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])
 
 
def f_k(bits, key):
    L = left_half(bits)
    R = right_half(bits)
    bits = permutate(R, FIXED_EP)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_half(bits), S0) + lookup_in_sbox(right_half(bits), S1)
    bits = permutate(bits, FIXED_P4)
    return xor(bits, L)
 
 
def encrypt(plain_text,K):
    bits = permutate(plain_text, FIXED_IP)
    temp = f_k(bits, key1(K))
    bits = right_half(bits) + temp
    bits = f_k(bits, key2(K))
    return permutate(bits + temp, FIXED_IP_INVERSE)
 
 
def decrypt(cipher_text,K):
    bits = permutate(cipher_text, FIXED_IP)
    temp = f_k(bits, key2(K))
    bits = right_half(bits) + temp
    bits = f_k(bits, key1(K))
    return permutate(bits + temp, FIXED_IP_INVERSE)

studen_id = '590610662'.encode('utf8')
cipher = [0b11001101,0b11000011,0b10111001,0b11110111,0b1101000,0b10111001,0b11110111,0b11110111,0b10110110,0b111000,0b111000,0b1010111,0b10111001,0b11110111,0b11000011,0b111000,0b11110111,0b1010111,0b10111001,0b10110110,0b1100011,0b10111001,0b1010111,0b110,0b1010111,0b10110110,0b1010111,0b11001101,0b110,0b111000,0b111000,0b11000011,0b1100011,0b1100011,0b11110111,0b11000011,0b11001101,0b1101000,0b11000011,0b1101000,0b1010111,0b1100011,0b1100011,0b11110111,0b10111001,0b10111001,0b111000,0b1010111,0b10110110,0b111000,0b110,0b11001101,0b111000,0b110,0b11001101,0b110,0b11000011,0b11110111,0b11110111,0b1010111,0b111000,0b111000,0b11110111,0b11110111,0b110,0b11110111,0b11000011,0b10111001,0b11000011,0b1010111,0b1101000,0b11001101,0b11001101,0b11000011,0b10111001,0b11110111]
cipher8bit = []
cipherKey = []
mykey = str(0)

 
for i in range (len(cipher)) :
    temp = str("{0:08b}".format(cipher[i]))
    cipher8bit.append(temp)
   
for i in range(9):
    a = cipher8bit[i]
    cipherKey.append(a)
 
for i in range(1024):
    check = []
    count = 0
    keyy = str("{0:010b}".format(i))
   
    for j in range (len(cipherKey)):
        c = str(cipher8bit[j])
        plaintext = int(decrypt(c,keyy),2)
        
        if (plaintext == int(studen_id[j])):
            check.append(plaintext-48)
            count = count + 1  
        else:
             break
   
    if count >= len(studen_id):
        mykey = i
        break
 
    # print(cipherKey)
    # print(bin(mykey))
    
mykey = str("{0:010b}".format(mykey))

for i in range(1024):
    check = []
    count = 0
   
    print("Key: "+str(keyy))
    for j in range (len(cipher8bit)):
        c = str(cipher8bit[j])
        pain = int(decrypt(c,mykey),2)
       
        if j <= 8:
            if (pain == int(studen_id[j])):
                check.append(pain-48)
                count = count + 1  
            else:
                 break
        else:
            check.append(pain-48)
    if count >= len(studen_id):
        break
 
print(check)