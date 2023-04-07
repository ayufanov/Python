import codecs

def generate_s(key):
    S = list(range(256))
    j = int(0)
    for i in range(256):
        j = (j + int(S[i]) + int(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]
    return(S)


def enc(text_file, key, enc_file):
    S = generate_s(key=key)
    x = 0
    y = 0
    enc_text = ''
    file = codecs.open(text_file, 'r', encoding='utf-8')
    text = file.read()
    file.close

    
    for i in range(len(text)):
        x = (x + 1) % 256
        y = (y + S[x]) % 256
        S[x], S[y] = S[y], S[x]
        K = S[(S[x] + S[y]) % 256]
        enc_text += chr((ord(text[i]) ^ K))
        enc_text = str(enc_text)
        f = codecs.open(enc_file, 'w+', encoding='utf-8')
        f.write(enc_text)
        f.close()        

    
    print(enc_text)    
    return enc_text


#e = enc('text.txt', '56', 'enc.txt')
#d = enc('enc.txt', '56', 'dec.txt')

print('enter, filenme with text, key (In octal number system), filename to write encoded or decoded text')
text_file = str(input())
key = str(input())
enc_file = str(input())
enc(text_file, key, enc_file)