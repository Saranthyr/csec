import os
import subprocess

key = subprocess.run('openssl rand -hex 16', capture_output=True).stdout

f = open('key.txt', 'wb+')
f.write(key)
f.close()


def image_enc(mode, inputfile, keyfile):
    file = open(inputfile, 'rb')
    data = file.read()
    file.close()
    header = data[:53]
    contents = data[53:]

    f = open(f'{"temp_" + mode + "benc"}', 'wb+')
    f.write(contents)
    f.close()

    subprocess.run(f'openssl enc -aes-256-{mode} -in {"temp_" + mode + "benc"} -out '
                   f'{"temp_" + mode + "aenc"} '
                   f'-pass file:{keyfile}')
    os.remove(f'{"temp_" + mode + "benc"}')

    f = open(f'{"temp_" + mode + "aenc"}', 'rb')
    contents = f.read()
    data = header + contents
    f.close()
    os.remove(f'{"temp_" + mode + "aenc"}')
    f = open(f'{inputfile.split(".")[0] + "_" + mode + "." + inputfile.split(".")[1]}', 'wb+')
    f.write(data)
    f.close()


def image_dec(mode, inputfile, keyfile):
    file = open(inputfile, 'rb')
    data = file.read()
    file.close()
    header = data[:53]
    contents = data[53:]

    f = open(f'{"temp_" + mode + "bdec"}', 'wb+')
    f.write(contents)
    f.close()

    subprocess.run(f'openssl enc -d -aes-256-{mode} -in {"temp_" + mode + "bdec"} -out {"temp_" + mode + "dec"} '
                   f'-pass file:{keyfile}')
    os.remove(f'{"temp_" + mode + "bdec"}')

    f = open(f'{"temp_" + mode + "dec"}', 'rb')
    contents = f.read()
    data = header + contents
    f.close()
    os.remove(f'{"temp_" + mode + "dec"}')
    f = open(f'{"dec_" + inputfile.split(".")[0] + "." + inputfile.split(".")[1]}', 'wb+')
    f.write(data)
    f.close()


image_enc('cbc', 'tux.bmp', 'key.txt')
image_enc('ecb', 'tux.bmp', 'key.txt')
image_enc('cfb', 'tux.bmp', 'key.txt')
image_enc('ofb', 'tux.bmp', 'key.txt')

image_dec('cbc', 'tux_cbc.bmp', 'key.txt')
image_dec('ecb', 'tux_ecb.bmp', 'key.txt')
image_dec('cfb', 'tux_cfb.bmp', 'key.txt')
image_dec('ofb', 'tux_ofb.bmp', 'key.txt')

