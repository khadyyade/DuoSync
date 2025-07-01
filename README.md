# DuoSync

**DuoSync** is a simple and efficient folder synchronization tool built in Python. It compares two directories and copies only files that are new or updated, preserving folder structure. 
It is designed especially for users with a dual-boot setup (Linux ↔ Windows), where one partition can be mounted and updated safely from the other.

## Features

- Copies only **new or modified files**
- Preserves the **directory structure**
- Automatically creates missing folders in the destination
- Prints each copied file for clarity
- Includes a simple test block with hardcoded paths

---

## Usage

Currently, you can run the script with predefined paths by editing the variables at the bottom of `duosync.py`:

```bash
python3 duosync.py
