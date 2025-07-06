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
           print("The destination directory does not exist. Creating the new folder...")
           dst.mkdir(parents=True, exist_ok=True)

    #COPY
    files_copied = 0

    for dir_path, _, filenames in os.walk(src):
        for file in filenames:
            src_file = Path(dir_path) / file
            relative_path = src_file.relative_to(src)
            dst_file = dst /relative_path

            needs_copy = False
            #If the file doesn't exist in the destination path
            if not dst_file.exists():
                needs_copy = True
            else:
                #Only if the file sizes are the same, we verify their hashes
                if src_file.stat().st_size != dst_file.stat().st_size:
                    needs_copy = True
                else:
                    src_hash = get_file_hash(src_file)
                    dst_hash = get_file_hash(dst_file)
                    if src_hash != dst_hash:
                        needs_copy = True
            if needs_copy:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")
                files_copied += 1

    if files_copied == 0:
        print("All files are up to date.")

    #DELETE
    files_deleted = 0

    for dir_path, _, filenames in os.walk(dst):
        for file in filenames:
            dst_file = Path(dir_path) / file
            relative_path = dst_file.relative_to(dst)
            src_file = src / relative_path

            if not src_file.exists():
                dst_file.unlink()  # Elimina el archivo
                print(f"Deleted {dst_file} (no longer exists in source)")
                files_deleted += 1

    print(f"Sync complete: {files_copied} file(s) copied, {files_deleted} deleted.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DuoSync - Synchronize two folders by copying new or modified files."
    )
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("destination", help="Path to the destination folder")

    args = parser.parse_args()

    sync_dirs(args.source, args.destination)

















































