from threading import Thread
from pathlib import Path
import sys


class Sorter:
    EXTENSIONS = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'video': ('AVI', 'MP4', 'MOV', 'MKV'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
        'archives': ('ZIP', 'GZ', 'TAR'),
    }

    folder_names = EXTENSIONS.keys()

    def __init__(self, path: Path) -> None:
        self.path = path

    def on_folder(self, folder_path):
        raise NotImplementedError

    def move_file(self, file_path: Path):
        file_extension = file_path.suffix[1:].upper()

        for file_type, file_extensions in self.EXTENSIONS.items():
            folder_path = Path(sys.argv[1]).joinpath(file_type)

            if not folder_path.exists():
                folder_path.mkdir(exist_ok=True)

            if file_extension in file_extensions:
                new_name = file_path.name

                new_path = folder_path.joinpath(new_name)

                while new_path.exists():
                    new_name = f'{new_path.stem}_1{new_path.suffix}'
                    new_path = new_path.with_name(new_name)

                file_path.rename(new_path)
                return new_name

    def sort_file(self):
        for file_path in self.path.iterdir():
            if file_path.is_dir():
                self.on_folder(file_path)
            else:
                self.move_file(file_path)


class Worker(Thread, Sorter):
    def __init__(self, item: Path) -> None:
        Thread.__init__(self)
        Sorter.__init__(self, item)

    def run(self):
        super().sort_file()

    def on_folder(self, folder_path):
        worker = Worker(folder_path)
        worker.start()


def main():
    main_thread = Worker(Path(sys.argv[1]))
    main_thread.start()
    main_thread.join()


if __name__ == "__main__":
    main()
