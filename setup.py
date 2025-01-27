import os
import zipfile
import stat

def ensure_local_bin():
    local_bin_path = os.path.expanduser("~/.local/bin")
    if not os.path.exists(local_bin_path):
        try:
            os.makedirs(local_bin_path, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory {local_bin_path}: {e}")
            return local_bin_path, False
    return local_bin_path, True

def unzip_binaries(zip_file_path, target_dir):
    if not os.path.exists(zip_file_path):
        print(f"Error: {zip_file_path} not found.")
        return False
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        return True
    except zipfile.BadZipFile as e:
        print(f"Error: Invalid zip file {zip_file_path}: {e}")
        return False

def make_files_executable(target_dir):
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                st = os.stat(file_path)
                os.chmod(file_path, st.st_mode | stat.S_IEXEC)
            except OSError as e:
                print(f"Error setting executable permission for {file_path}: {e}")

def main():
    local_bin_path, success = ensure_local_bin()
    if success:
        zip_file_path = "binaries.zip"
        if unzip_binaries(zip_file_path, local_bin_path):
            make_files_executable(local_bin_path)

if __name__ == "__main__":
    main()
