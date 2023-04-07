import numpy as np
import codecs

n_rounds = 8
mod = 65536 # 2**16



def key_from_text(text):
    key = ''
    for i in range(len(text)):
        symb = bin(ord(text[i]))[2::]
        #print(symb)
        symb = '0' * (8 - len(symb)) + symb
        key += symb
    if len(key) != 128:
        key = key + '0' * (128 - len(key))
    return key

def gcdExtended(a, b):
    if a == 0 :
        return b,0,1
    gcd,x1,y1 = gcdExtended(b%a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd,x,y



def Factor(n):
    Ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            Ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        Ans.append(n)
    return Ans


def mult_module(a,b):
    
    factor_a = Factor(a)
    factor_b = Factor(b)
    res = int(1)
    min_len = min(len(factor_a), len(factor_b))
    max_len = max(len(factor_a), len(factor_b))
    for i in range(min_len):
        
        res =(((res * factor_a[i]) % (mod+1)) * factor_b[i]) % (mod+1)
    if max_len != min_len:
        for i in range(max_len - min_len):

            if max_len == len(factor_b):
                
                res = (res * factor_b[min_len+i]) % (mod + 1)
            if max_len == len(factor_a):
                
                res = (res * factor_a[min_len+i]) % (mod + 1)
    return res


def generate_matrixes(key_init):
    key_matrix = np.ones((9,6), dtype=int)
    for i in range(9):
        for j in range(6):
            key_matrix[i][j] = int(key_init[j * 16:(j + 1) * 16], base=2)   
        key_init = key_init[25::] + key_init[0:25]

    decode_key_matrix = np.ones((9,6), dtype = int)
    for j in range(6):
        for i in range(9):
            if j == 0 or j == 3:
                if key_matrix[8-i][j] == 0:
                    x = 0
                else:
                    gcd, x, y = gcdExtended(key_matrix[8-i][j], mod + 1)
                decode_key_matrix[i][j] = x % (mod + 1)
            if j == 1:
                if i == 2 or i == 8:
                    decode_key_matrix[i][j] = ((-1) * key_matrix[8-i][1]) % mod
                else:
                    decode_key_matrix[i][j] = ((-1) * key_matrix[8-i][2]) % mod

            if j == 2:
                if i == 1 or i == 8:
                    decode_key_matrix[i][j] = ((-1) * key_matrix[8-i][2]) % mod
                else:
                    decode_key_matrix[i][j] = ((-1) * key_matrix[8-i][1]) % mod
            if j == 4 or j == 5:
                if i != 8:
                    decode_key_matrix[i][j] = key_matrix[7-i][j]
                else: decode_key_matrix[i][j] = 1
    print('key matrix = \n',key_matrix)
    print('decode_matrix = \n',decode_key_matrix)
    return key_matrix, decode_key_matrix




def mod_text(file_name,key_matrix, file_name2):
    enc_text = ''
    allbits = ''
    enc_bit = ''
    file = codecs.open(file_name, 'r', encoding='utf-8')
    text = file.read()
    file.close()


    for i in range(len(text)):
            
            if ((i + 1) % 8 == 0 or i == len(text) - 1):
                
                symb = text[i]
            
                bits =  bin(ord(symb))[2::]
                if len(bits) != 8:
                    bits = '0' * (8 - len(bits)) + bits
                
                allbits += bits
                if len(allbits) != 64:
                    allbits = allbits + '0' * (64 - len(allbits))
                #print(allbits)
                P1 = int(str(allbits[0:16]), base=2)
                P2 = int(str(allbits[16:32]), base=2)
                P3 = int(str(allbits[32:48]), base=2)
                P4 = int(str(allbits[48::]), base=2)
                for round in range(n_rounds):
                    
                    K1 = key_matrix[round][0]
                    K2 = key_matrix[round][1]
                    K3 = key_matrix[round][2]
                    K4 = key_matrix[round][3]
                    K5 = key_matrix[round][4]
                    K6 = key_matrix[round][5]
 
                    st1 = mult_module(P1, K1)      
                    st2 = (K2 + P2) % mod
                    st3 = (K3 + P3) % mod
                    st4 = mult_module(K4, P4)
                    st5 = st1 ^ st3
                    st6 = st2 ^ st4
                    st7 = mult_module(st5, K5)
                    st8 = (st6 + st7) % mod
                    st9 = mult_module(st8, K6)
                    st10 = (st9 + st7) % mod
                    P1 = st1 ^ st9
                    P2 = st3 ^ st9
                    P3 = st2 ^ st10 
                    P4 = st4 ^ st10
                
                    if round == 7:
                        res1 = P1
                        res2 = P2
                        res3 = P3
                        res4 = P4

                        K1 = key_matrix[8][0]
                        K2 = key_matrix[8][1]
                        K3 = key_matrix[8][2]
                        K4 = key_matrix[8][3]
                        
                        res1 = bin(mult_module(res1, K1))[2::]
                        res2 = bin((res3 + (K2)) % mod )[2::]
                        res3 = bin((P2 + (K3)) % mod)[2::]
                        res4 = bin(mult_module(res4, K4) % (mod + 1))[2::]
                        if len(res1) != 16:
                            res1 = '0' * (16 - len(res1)) + res1
                        if len(res2) != 16:
                            res2 = '0' * (16 - len(res2)) + res2
                        if len(res3) != 16:
                            res3 = '0' * (16 - len(res3)) + res3
                        if len(res4) != 16:
                            res4 = '0' * (16 - len(res4)) + res4
                        
                        res = res1 + res2 + res3 + res4
                        #print(res)
                        enc_bit += res
                        for q in range(8):
                            symb = res[8*q: (q+1)*8]
                            #print(symb)
                            enc_text += (chr(int(symb, base=2)))
                        #print(enc_text)
                        allbits = ''

                    '''
                    else: 
                        res1 = bin(st11)[2::]
                        if len(res1) != 16:
                            res1 = '0' * (16 - len(res1)) + res1
                    
                        res2 = bin(st12)[2::]
                        if len(res2) != 16:
                            res2 = '0' * (16 - len(res2)) + res2

                        res3 = bin(st13)[2::]
                        if len(res3) != 16:
                            res3 = '0' * (16 - len(res3)) + res3
                        
                        res4 = bin(st14)[2::]
                        if len(res4) != 16:
                            res4 = '0' * (16 - len(res4)) + res4
                    
                        allbits = res1 + res3 + res2 + res4
                        
                        #print('key =',key)
                        '''
            

                
            else:
                symb = text[i]
                
                bits =  bin(ord(symb))[2::]
                if len(bits) != 8:
                    bits = '0' * (8 - len(bits)) + bits

                allbits += bits
    f = codecs.open(file_name2, 'w+', encoding='utf-8')
    f.write(enc_text)
    f.close()    
    return (enc_text)

key = key_from_text('qwertasdqwertasd')
print('key =', key)

e_mat, d_mat = generate_matrixes(key)
qwe = mod_text('text.txt', e_mat, 'enc.txt')
print('cipher_text =')
print(qwe)

enc = mod_text('enc.txt', d_mat, 'dec.txt')
print('decoded text =', enc)