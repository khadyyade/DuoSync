import os
import shutil
from pathlib import Path
import argparse
import hashlib

def get_file_hash(file_path):
    file_hash = hashlib.md5() #MD5 is an algorithm that generates a unique 128-bit hash number (32 hexadecimal characters) for any data
    with open(file_path, "rb") as f:#MD5 only works with bytes, not with text
        for block in iter(lambda: f.read(4096), b""): #It reads the file in 4KB blocks until there is nothing left to read
            file_hash.update(block) #For every block, we update the hash number
    return file_hash.hexdigest()

def sync_dirs(src_path, dst_path):
    src = Path(src_path)
    dst = Path(dst_path)

    if not src.exists():
       print("The source directory does not exist")
       return
    else:
       if not dst.exists():
           print("The destination directory does not exist")
           return

    files_copied = 0

    for dir_path, _, filenames in os.walk(src):
        for file in filenames:
            src_file = Path(dir_path) / file
            relative_path = src_file.relative_to(src)
            dst_file = dst /relative_path

            #If the file doesn't exist in the destination path or the file in the source path has been modified
            if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")
                files_copied += 1

    if files_copied == 0:
        print("All files are up to date.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DuoSync - Synchronize two folders by copying new or modified files."
    )
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("destination", help="Path to the destination folder")

    args = parser.parse_args()

    sync_dirs(args.source, args.destination)

















































