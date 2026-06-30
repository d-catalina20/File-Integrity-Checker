import argparse
import hashlib
import json
import os
from pathlib import Path

DB_FILE = "log_hashes.json"

def calc_hash(file_path):
	sha256 = hashlib.sha256()
	chunk_size = 8192
	try:
		with open(file_path, 'rb') as f:
			while chunk := f.read(chunk_size):
				sha256.update(chunk)
		return sha256.hexdigest()
	except Exception as e:
		print(f"Error reading the file {file_path}: {e}")
		return None

def load_db():
	if os.path.exists(DB_FILE):
		with open(DB_FILE, 'r') as f:
			return json.load(f)
	return {}

def save_db(data):
	with open(DB_FILE, 'w') as f:
		json.dump(data, f, indent=4)

def get_all_files(path):
	p = Path(path)
	if p.is_file():
		return [str(p.resolve())]
	elif p.is_dir():
		return [str(f.resolve()) for f in p.rglob("*") if f.is_file()]
	else:
		print(f"The path {path} is not valid")
		return []

def cmd_init(path):
	db = load_db()
	files = get_all_files(path)

	if not files:
		return

	for f in files:
		h = calc_hash(f)
		if h:
			db[f] = h

	save_db(db)
	print("Hashes stored succesfully.")

def cmd_check(path):
	db = load_db()
	files = get_all_files(path)

	if not files:
		return

	for f in files:
		if f not in db:
			print(f"New file detected (uninitialized): {f}")

		h = calc_hash(f)
		orig_h = db[f]
		if h == orig_h:
			print(f"{f} -> Status: Unmodified")
		else:
			print(f"{f} -> Status: MODIFIED (Hash mismatch! Posible altering!)")

def cmd_update(path):
	db = load_db()
	p = Path(path)

	if not p.is_file():
		print("For update, specify just one file.")
		return

	absolute_path = str(p.resolve())
	h = calc_hash(absolute_path)
	if h:
		db[absolute_path] = h
		save_db(db)
		print(f"Hash updated successfully for {absolute_path}.")

def main():
	parser = argparse.ArgumentParser(description="Tool for checking log integrity")

	subparsers = parser.add_subparsers(dest="command", required=True)

	p_init = subparsers.add_parser("init")
	p_init.add_argument("path", help="Indicate the directory or file you want to initialize")

	p_check = subparsers.add_parser("check")
	p_check.add_argument("path", help = "Indicate the directory or file you want to check")

	p_update = subparsers.add_parser("update")
	p_update.add_argument("path", help="Indicate the directory or file you want to update the hash of")

	args = parser.parse_args()

	if args.command == "init":
		cmd_init(args.path)
	elif args.command == "check":
		cmd_check(args.path)
	elif args.command == "update":
		cmd_update(args.path)

if __name__ == "__main__":
	main()