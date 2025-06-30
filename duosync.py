import os
import shutil
from pathlib import Path

def sync_dirs(src_path, dst_path):
    src = Path(src_path)
    dst = Path(dst_path)

    if not src.exists():
       print("The source directory does not exist")
    else:
       if not dst.exists():
           print("The destination directory does not exist")

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
    #Temporary paths for testing
    source = "/home/jadi/Documentos/prueba1_DuoSync"
    destination = "/mnt/windows/Users/khady/Documents/prueba_destino"
    sync_dirs(source, destination)
















































