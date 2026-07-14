from config import Config
import os, csv

class FileHandler:
    def read_text_file(self, filename: str) -> str:
        path = os.path.join(Config.BASE_PATH, filename)

        if not self.file_exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()

        except Exception as e:
            raise IOError(f"Error reading file {path}: {e}") from e
        
    def read_csv_morse_mapping(self, path: str):
        if not self.file_exists(path):
            raise FileNotFoundError(f"Mapping file not found: {path}")

        encode_map = {}
        decode_map = {}

        try:
            with open(path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    char = row.get("char")
                    morse = row.get("morse")

                    # Skip invalid rows
                    if not char or not morse:
                        continue

                    # Clean data
                    char = char.strip()
                    morse = morse.strip()

                    # Store mappings
                    encode_map[char] = morse
                    decode_map[morse] = char

            return encode_map, decode_map

        except Exception as e:
            raise IOError(f"Error reading Morse CSV file: {path} | {e}") from e
        
    def write_text_file(self, path: str, data: str, overwrite: bool = True) -> None:
        """
        Writes text data to a file safely.

        Args:
            path (str): Output file path.
            data (str): Content to write.
            overwrite (bool): If False, prevents overwriting existing files.

        Raises:
            FileExistsError: If file exists and overwrite is False.
            IOError: If writing fails.
        """

        if not overwrite and self.file_exists(path):
            raise FileExistsError(f"File already exists: {path}")

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(data)

        except Exception as e:
            raise IOError(f"Error writing file {path}: {str(e)}") from e
        
    def write_csv_file(self, path: str, rows: list) -> None:
        """
        Writes rows of data to a CSV file.

        Args:
            path (str): Output file path.
            rows (list): List of dictionaries representing CSV rows.

        Raises:
            IOError: If writing fails.
        """
        try:
            with open(path, "w", encoding="utf-8", newline="") as file:
                if rows:
                    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)

        except Exception as e:
            raise IOError(f"Error writing CSV file {path}: {str(e)}") from e

    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)
        pass
        
    def get_extension(self, path: str) -> str:
        """
        Returns the file extension of a given path.

        Args:
            path (str): File path.

        Returns:
            str: File extension (without dot), or empty string if none.
        """

        _, ext = os.path.splitext(path)
        return ext.lower().lstrip(".")