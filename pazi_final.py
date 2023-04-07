import os

def encode_img(input_img_name, output_img_name, degree, byte_num):
    text = str(input())

    image = open(input_img_name, 'rb')
    enc_image = open(output_img_name, 'wb')

    if degree % 2 != 0 and degree != 1 and i > 4 and i < 1:
        print("invalid degree")
        return 0

    if len(text) >= os.stat(input_img_name).st_size * degree / 8 - 54 - byte_num:
        print("text is too long or byte_num is too big")
        return 0
    
    img_mask = '0' * (8-degree)
    text_mask = '1' * (8-degree)
    for i in range(degree):
         text_mask += '0'
         img_mask = '1' + img_mask
    img_mask = int(img_mask, 2)
    text_mask = int(text_mask, 2)
    enc_image.write(image.read(54))
    image.seek(byte_num, 1)
    enc_image.seek(byte_num, 1)
    
    
    for i in range(len(text)):
        symbol = text[i]
        symbol = ord(symbol)
        #print(symbol)
        for j in range(0, 8, degree):
            img_byte = int.from_bytes(image.read(1), 'little') & img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree)
            img_byte |= bits
            enc_image.write(img_byte.to_bytes(1, 'little'))
            symbol <<= degree

    enc_image.write(image.read())
    image.close()
    enc_image.close()

    return 1


def decode_image(enc_img, len_text, degree, byte_num):
    degree = int(degree)
    len_text = int(len_text)
    if degree % 2 != 0 and degree != 1:
        print("invalid degree")
        return 0


    if len_text >= os.stat(enc_img).st_size * degree / 8 - 54 - byte_num:
        print("Too much symbols to read or byte_num is too big")
        return 0

    
    img = open(enc_img, 'rb')
    img.seek(54)
    img.seek(byte_num, 1)
    img_mask = '1' * (8-degree)
    
    for i in range(degree):
         
         img_mask = '0' + img_mask
    img_mask = int(img_mask, 2)
    
    text = ''
    for i in range(len_text):
        symbol = 0
        for i in range(0, 8, degree):
            img_byte = int.from_bytes(img.read(1), 'little') & img_mask
            symbol <<= degree
            symbol |= img_byte
        #print(symbol)
        text += chr(symbol)

    print(text)
    img.close()
    return True


#encode_img('pazi.bmp', 'pa.bmp', 4)
#decode_image('pa.bmp', 9, 4)

print('encode or decode?')
comnd = str(input())

if comnd == 'encode':
    print('enter input_img_path')
    input_img_name = str(input())
    print('enter output_img_path')
    output_img_name = str(input())
    print('input degree')
    degree = int(input())
    print('input byte from which encoding starts')
    byte_num = int(input())
    print('input text')
    encode_img(input_img_name=input_img_name, output_img_name=output_img_name, degree=degree, byte_num= byte_num)
elif comnd == 'decode':
    print('enter encoded_img')
    encoded_img = str(input())
    print('text length')
    len_text = str(input())
    print('input degree')
    degree = int(input())
    print('input byte from which decoding starts')
    byte_num = int(input())
    decode_image(enc_img=encoded_img, len_text= len_text, degree=degree, byte_num=byte_num)
else:
    print('unknown commamd')
    