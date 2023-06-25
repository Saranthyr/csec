import numpy as np
from PIL import Image
import subprocess


def encoding(filename, message):
    src = Image.open(filename, 'r')
    w, h = src.size

    message += '$t3g0'

    msg_bytes = ''.join([format(ord(i), '08b') for i in message])

    src_arr = np.array(list(src.getdata()))

    if src.mode == 'RGB':
        bands = 3
    elif src.mode == 'RGBA':
        bands = 4

    total_size_pix = src_arr.size//bands

    if len(msg_bytes) > total_size_pix:
        print("Can't encode - too small image")
        return 1

    i = 0
    for pix in range(total_size_pix):
        for q in range(0,3):
            if i < len(msg_bytes):
                src_arr[pix][q] = int(bin(src_arr[pix][q])[2:9] + msg_bytes[i], 2)
                i += 1

    src_arr = src_arr.reshape(h, w, bands)
    enc_img = Image.fromarray(src_arr.astype('uint8'), src.mode)
    enc_img.save(filename.split('.')[0] + "_enc." + filename.split('.')[1])


def decoding(filename):
    src_img = Image.open(filename)
    src_arr = np.array(list(src_img.getdata()))

    if src_img.mode == 'RGB':
        bands = 3
    elif src_img.mode == 'RGBA':
        bands = 4

    total_size_pix = src_arr.size // bands

    dec_str = ''

    for pix in range(total_size_pix):
        for q in range(0,3):
            dec_str += (bin(src_arr[pix][q])[2:][-1])

    dec_str = [dec_str[i:i+8] for i in range(0, len(dec_str), 8)]

    det_data = ""
    for i in range(len(dec_str)):
        if det_data[-5:] == '$t3g0':
            break
        else:
            det_data += chr(int(dec_str[i], 2))

    if '$t3g0' in det_data:
        det_data = det_data[:-5]
        return det_data
    else:
        return 1

hash = subprocess.run('openssl dgst -sha1 leasing.txt',capture_output=True)
hash = str(hash.stdout).split('= ')[1].strip('\\rn\'')
print("Leasing.txt hash: " + str(hash))

encoding('28.bmp', hash)
detected_msg = decoding('28_enc.bmp')
if type(detected_msg) != int():
    print("Detected message: " + detected_msg)
    print('Identical hashes? ' + str(detected_msg == hash))
else:
    print("No message was found")
