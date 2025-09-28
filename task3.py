import os
import random
import string
from pathlib import Path

class TestDataGenerator:
    def __init__(self, base_dir="test_data"):
        self.base_dir = Path(base_dir)
        if not self.base_dir.exists():
            self.base_dir.mkdir()

    def generate_file(self, file_path, size):

        characters = string.ascii_letters + string.digits + string.punctuation + " "
        content = ''.join(random.choice(characters) for _ in range(size))

        # Ensure the parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def generate_multiple_files(self, count, min_size=100, max_size=1000):

        for i in range(count):
            filename = f"file_{i + 1}.txt"
            size = random.randint(min_size, max_size)
            file_path = self.base_dir / filename
            self.generate_file(file_path, size)

    def generate_folder_structure(self, max_depth=3, max_folders=5, max_files=3):


        def create_random_structure(current_path, current_depth):
            if current_depth >= max_depth:
                return

            # Random number of folders at this level
            num_folders = random.randint(1, max_folders)
            for i in range(num_folders):
                folder_name = f"folder_{current_depth}_{i + 1}"
                folder_path = current_path / folder_name
                folder_path.mkdir(exist_ok=True)

                # Random number of files in this folder
                num_files = random.randint(0, max_files)
                for j in range(num_files):
                    filename = f"file_{current_depth}_{i + 1}_{j + 1}.txt"
                    file_path = folder_path / filename
                    size = random.randint(50, 500)
                    self.generate_file(file_path, size)

                # Randomly decide to create subfolders
                if random.choice([True, False]):
                    create_random_structure(folder_path, current_depth + 1)

        create_random_structure(self.base_dir, 0)

    def clear_test_directory(self):

        if self.base_dir.exists():
            for item in self.base_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    import shutil
                    shutil.rmtree(item)

    def fill_directory(self, total_files=20, max_depth=3, max_folders_per_level=4, max_files_per_folder=3):

        self.clear_test_directory()

        self.generate_folder_structure(
            max_depth=max_depth,
            max_folders=max_folders_per_level,
            max_files=max_files_per_folder
        )


        current_file_count = self.count_files()
        remaining_files = total_files - current_file_count

        if remaining_files > 0:
            self.generate_multiple_files(remaining_files)

    def count_files(self):

        file_count = 0
        for root, dirs, files in os.walk(self.base_dir):
            file_count += len(files)
        return file_count


# Demonstration that follows all requirements
if __name__ == "__main__":
    generator = TestDataGenerator()

    # Clear any existing data first
    generator.clear_test_directory()

    print("1. Generating single file...")
    file_path = generator.base_dir / "single_test_file.txt"
    generator.generate_file(file_path, 500)

    print("2. Generating multiple files...")
    generator.generate_multiple_files(5, min_size=200, max_size=800)

    print("3. Generating random folder structure...")
    generator.generate_folder_structure(max_depth=3, max_folders=4, max_files=3)

    print("4. Clearing directory...")
    generator.clear_test_directory()

    print("5. Filling directory with specified parameters...")
    generator.fill_directory(
        total_files=25,  # Total files to create
        max_depth=4,  # Maximum folder depth
        max_folders_per_level=3,  # Max folders per level
        max_files_per_folder=2  # Max files per folder
    )
    print(f"Total files created: {generator.count_files()}")