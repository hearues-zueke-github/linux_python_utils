#! /usr/bin/python3

import os
import sys

# import pandas as pd # use pd for the dataframe

from hashlib import md5, sha1, sha256, sha3_256
from tqdm import tqdm

# TODO: add later parameter functionality

# default is only    dir and not recursive!
CURRENT_DIR = os.path.abspath(os.curdir)

if __name__ == "__main__":
	argv = sys.argv

	if len(argv) < 2:
		folder_path_rel = '.'
	else:
		folder_path_rel = argv[1]

	if folder_path_rel[0] == '/':
		folder_path_abs = folder_path_rel
	else:
		folder_path_abs = os.path.join(CURRENT_DIR, folder_path_rel)

	assert os.path.exists(folder_path_abs)

	l_column = ['file_name', 'md5', 'sha1', 'sha256', 'sha3_256']

	for root_path, l_dir_name, l_file_name in os.walk(folder_path_abs):
		d_data = {column: [] for column in l_column}

		print(f"root_path: {root_path}")
		for file_name in tqdm(l_file_name):
			file_path = os.path.join(root_path, file_name)

			# continue

			# ignore symlinks for now
			if os.path.islink(file_path):
				continue

			md5_hash = md5()
			sha1_hash = sha1()
			sha256_hash = sha256()
			sha3_256_hash = sha3_256()
			with open(file_path, "rb") as f:
				# Read and update the hash value in blocks of 4K
				for byte_block in iter(lambda: f.read(4096), b""):
					md5_hash.update(byte_block)
					sha1_hash.update(byte_block)
					sha256_hash.update(byte_block)
					sha3_256_hash.update(byte_block)
				
			d_data['file_name'].append(file_name)
			d_data['md5'].append(md5_hash.hexdigest())
			d_data['sha1'].append(sha1_hash.hexdigest())
			d_data['sha256'].append(sha256_hash.hexdigest())
			d_data['sha3_256'].append(sha3_256_hash.hexdigest())

		with open(os.path.join(root_path, '.hashsums.txt'), "w") as f:
			f.write('|'.join(l_column))
			f.write('\n')
			for i in range(0, len(d_data[l_column[0]])):
				f.write(d_data[l_column[0]][i])
				for column in l_column[1:]:
					f.write(f'|{d_data[column][i]}')
				f.write('\n')
