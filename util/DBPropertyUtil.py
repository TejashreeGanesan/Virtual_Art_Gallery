import os

class PropertyUtil:

    @staticmethod
    def get_property_string(file_path = 'config/db.properties'):
        properties = {}
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key,value = line.split('=', 1)
                        properties[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: Property file '{file_path}' not found.")

        except Exception as e:
            print(f"Error reading property file: {e}")
        return properties