import hashlib
import os
import time
from dotenv import load_dotenv
from hash_gen_and_check import generate_empty_hash, generate_hash_with_conjunction

data = open("leasing.txt", "r", encoding="utf-8").read()
load_dotenv()


start_time = time.time()
generate_empty_hash(data)
generate_hash_with_conjunction(data)
final_time = time.time() - start_time
print("Program worktime: " + str(final_time))
