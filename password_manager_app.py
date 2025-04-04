from cryptography.fernet import Fernet
import os


class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}


    def create_key(self, path):
        """Generate a new encryption key and save it to a file."""
        try:
            self.key = Fernet.generate_key()
            with open(path, 'wb') as key_file:
                key_file.write(self.key)
            print("Key successfully created.")
        except Exception as e:
            print(f"Error creating key: {str(e)}")


    def load_key(self, path):
        """Load an encryption key from a file."""
        try:
            if not os.path.exists(path):
                raise FileNotFoundError("Key file not found.")
            with open(path, 'rb') as key_file:
                self.key = key_file.read()
            print("Key successfully loaded.")
        except Exception as e:
            print(f"Error loading key: {str(e)}")


    def create_password_file(self, path, initial_values=None):
        """Create a password file and optionally add initial values."""
        self.password_file = path
        try:
            with open(path, 'w') as f:
                f.write("")  # Create an empty file
            if initial_values:
                for site, password in initial_values.items():
                    self.add_password(site, password)
            print("Password file created successfully.")
        except Exception as e:
            print(f"Error creating password file: {str(e)}")


    def load_password_file(self, path):
        """Load a password file and decrypt its contents."""
        try:
            if not os.path.exists(path):
                raise FileNotFoundError("Password file not found.")
            self.password_file = path
            with open(path, 'r') as f:
                for line in f:
                    try:
                        site, encrypted_password = line.strip().split(':')
                        self.password_dict[site] = Fernet(self.key).decrypt(encrypted_password.encode()).decode()
                    except Exception:
                        print(f"Skipping invalid entry in file: {line.strip()}")
            print("Password file loaded successfully.")
        except Exception as e:
            print(f"Error loading password file: {str(e)}")


    def add_password(self, site, password):
        """Add a new password for a given site."""
        try:
            if not self.key:
                raise ValueError("Encryption key not loaded.")
            if not self.password_file:
                raise ValueError("Password file not specified.")


            encrypted_password = Fernet(self.key).encrypt(password.encode()).decode()
            self.password_dict[site] = password


            with open(self.password_file, 'a') as f:
                f.write(f"{site}:{encrypted_password}\n")


            print(f"Password for {site} added successfully.")
        except Exception as e:
            print(f"Error adding password: {str(e)}")


    def get_password(self, site):
        """Retrieve the password for a given site."""
        try:
            return self.password_dict.get(site, "No password found for this site.")
        except Exception as e:
            print(f"Error retrieving password: {str(e)}")
            return None


