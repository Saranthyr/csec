import os
import subprocess
from dotenv import load_dotenv


def generate_empty_hash(data):
    # deleting endline symbol
    hash_base = subprocess.run(f"openssl dgst -sha1 "
    f"{str(os.path.dirname(os.path.realpath('__file__')))}\leasing.txt", capture_output=True)
    for i in range(len(data)):
        li = list(data)
        li[i] = '\u200b' + li[i]
        data_new = "".join(li)
        file1 = open(f"{str(os.path.dirname(os.path.realpath('__file__'))) + str(os.environ['FILE_LOCATION_EMPTY'])}"
                     f"{str(i)}.txt", "w+", encoding="utf-8")
        file1.write(data_new)
        file1.close()
        hash_new = subprocess.run(f"openssl dgst -sha1 "
                              f"{str(os.path.dirname(os.path.realpath('__file__')))+str(os.environ['FILE_LOCATION_EMPTY'])}"
                              f"{str(i)}.txt", capture_output=True)
        print(f"Comparing hash for emptyfile{i}.txt")
        print("Base file hash: " + str(hash_base.stdout).split('= ')[1].strip('\\rn\''))
        print("New file hash: " + str(hash_new.stdout).split('= ')[1].strip('\\rn\''))
        if hash_base == hash_new:
            print("Hash exact")
            print("Starting size: " +
                  str(os.path.getsize(f"{str(os.path.dirname(os.path.realpath('__file__')))}\leasing.txt")))
            print("Final size: " +
                  str(os.path.getsize(
                      f"{str(os.path.dirname(os.path.realpath('__file__'))) + str(os.environ['FILE_LOCATION_EMPTY'])}"
                      f"{str(i)}.txt")))
            break
        else:
            print("Different hashes")
            print("Starting size: " +
                  str(os.path.getsize(f"{str(os.path.dirname(os.path.realpath('__file__')))}\leasing.txt")))
            print("Final size: " +
                  str(os.path.getsize(f"{str(os.path.dirname(os.path.realpath('__file__')))+str(os.environ['FILE_LOCATION_EMPTY'])}"
                                      f"{str(i)}.txt")))
            os.remove(f"{str(os.path.dirname(os.path.realpath('__file__')))+str(os.environ['FILE_LOCATION_EMPTY'])}{str(i)}.txt")


def generate_hash_with_conjunction(data):
    conjunctions = [' а ', ' в ', ' от ', ' на ', ' за ', ' по ', ' но ']
    hash_base = subprocess.run(f"openssl dgst -sha1 "
                               f"{str(os.path.dirname(os.path.realpath('__file__')))}leasing.txt", capture_output=True)
    for word in conjunctions:
        if data.find(word) != -1:
            data_new = data.replace(word, '')
            file1 = open(f"{str(os.path.dirname(os.path.realpath('__file__'))) + str(os.environ['FILE_LOCATION_CONJUNCTION'])}"
                     f"{word}.txt", "w+", encoding="utf-8")
            file1.write(data_new)
            file1.close()
            hash_new = subprocess.run(f"openssl dgst -sha1 "
                              f"{str(os.path.dirname(os.path.realpath('__file__')))+str(os.environ['FILE_LOCATION_CONJUNCTION'])}"
                              f"{word}.txt", capture_output=True)
            print(f"Comparing hash for conjfile_{word}.txt")
            if hash_base == hash_new:
                print("Hash exact")
                print("Starting size: " +
                      str(os.path.getsize(f"{str(os.path.dirname(os.path.realpath('__file__')))}\leasing.txt")))
                print("Final size: " +
                      str(os.path.getsize(
                          f"{str(os.path.dirname(os.path.realpath('__file__'))) + str(os.environ['FILE_LOCATION_CONJUNCTION'])}"
                          f"{word}.txt")))
                break
            else:
                print("Different hashes")
                print("Starting size: " +
                      str(os.path.getsize(f"{str(os.path.dirname(os.path.realpath('__file__')))}\leasing.txt")))
                print("Final size: " +
                      str(os.path.getsize(
                          f"{str(os.path.dirname(os.path.realpath('__file__'))) + str(os.environ['FILE_LOCATION_CONJUNCTION'])}"
                          f"{word}.txt")))
                os.remove(
                          f"{str(os.path.dirname(os.path.realpath('__file__'))) + str(os.environ['FILE_LOCATION_CONJUNCTION'])}"
                          f"{word}.txt")
