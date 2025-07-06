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

def is_mounted(partition_path): #Function for verifying if the path is mounted
    return os.path.ismount(partition_path)

def mount_partition(device, partition_path):
    print(f"Attempting to mount {device} on {partition_path}...")

    try:
        os.makedirs(partition_path, exist_ok=True)
        result = os.system(f"sudo mount {device} {partition_path}")

        if result != 0:
            print("❌ Failed to mount partition. You may need to shut down Windows completely or disable Fast Startup.")
            return False
        return True
    except Exception as e:
        print(f"❌ Error while trying to mount: {e}")
        return False

def sync_dirs(src_path, dst_path, dry_run=False):
    src = Path(src_path)
    dst = Path(dst_path)

    if not src.exists():
       print("The source directory does not exist")
       return
    else:
       if not dst.exists():
           print("The destination directory does not exist." +
                 " Would create the new folder..." if dry_run else " Creating the new folder...")
           if not dry_run:
               try:
                   dst.mkdir(parents=True, exist_ok=True)
               except Exception as e:
                   print(f"Failed to create the destination folder: {e}")
                   return
    #COPY
    files_copied = 0
    dry_files_copied = 0

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
                if not dry_run:
                    try:
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        print(f"Copied {src_file} to {dst_file}")
                        files_copied += 1
                    except Exception as e:
                        print(f"❌ Failed to copy {relative_path}: {e}")
                else:
                    print(f"Would copy {src_file} to {dst_file}")
                    dry_files_copied += 1

    #DELETE
    files_deleted = 0
    dry_files_deleted = 0

    for dir_path, _, filenames in os.walk(dst):
        for file in filenames:
            dst_file = Path(dir_path) / file
            relative_path = dst_file.relative_to(dst)
            src_file = src / relative_path

            if not src_file.exists():
                if not dry_run:
                    try:
                        dst_file.unlink()  #Deletes the file
                        print(f"Deleted {dst_file} (no longer exists in source)")
                        files_deleted += 1
                    except Exception as e:
                        print(f"Failed to delete {relative_path}: {e}")
                else:
                    print(f"Would delete {dst_file} (no longer exists in source)")
                    dry_files_deleted += 1

    if files_copied == 0 and files_deleted == 0 and not dry_run:
        print("All files are up to date.")

    action = "Would " if dry_run else ""
    copied = files_copied if not dry_run else dry_files_copied
    deleted = files_deleted if not dry_run else dry_files_deleted
    print(f"Sync {'simulation' if dry_run else 'complete'}: "
          f"{action}copy {copied} file(s), {action}delete {deleted} file(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DuoSync - Synchronize two folders by copying new or modified files."
    )
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("destination", help="Path to the destination folder")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the sync without actually copying or deleting files")

    args = parser.parse_args()

    if args.destination.startswith("/mnt/windows") and not is_mounted("/mnt/windows"):
        mounted=mount_partition("/dev/nvme0n1p3", "/mnt/windows")
        if not mounted:
            print("Failed to mount Windows partition. Exiting.")
            exit(1)

    sync_dirs(args.source, args.destination, args.dry_run)


