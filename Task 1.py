import hashlib
import os
import time

def calculate_file_hash(file_path):
    """
    Calculate the hash value of a file using SHA-256.
    """
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

def monitor_files(directory_path, interval=10):
    """
    Monitor a directory for changes in files by calculating and comparing hash values.
    
    :param directory_path: Path to the directory to monitor.
    :param interval: Time (in seconds) to wait before re-checking the files.
    """
    file_hashes = {}

    # Initialize hashes for files in the directory
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                file_hashes[file_path] = file_hash

    print(f"Monitoring changes in directory: {directory_path}")

    while True:
        time.sleep(interval)
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                current_hash = calculate_file_hash(file_path)
                
                if current_hash:
                    if file_path in file_hashes:
                        if file_hashes[file_path] != current_hash:
                            print(f"File changed: {file_path}")
                            file_hashes[file_path] = current_hash
                    else:
                        print(f"New file detected: {file_path}")
                        file_hashes[file_path] = current_hash

if __name__ == "__main__":
    
    directory_to_monitor = r"D:\C++\Coding"  # Replace with your directory
    monitor_files(directory_to_monitor)
