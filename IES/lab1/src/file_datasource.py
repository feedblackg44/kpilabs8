from csv import reader
from datetime import datetime
from dataclasses import fields


class FileDatasource:
    def __init__(self, *args, **kwargs) -> None:
        return_data_type = args[0]
        filetypes = kwargs.get("filetypes")
        filenames = kwargs.get("filenames")

        self.return_data_type = return_data_type
        self.file_names = filenames
        self.file_types = filetypes
        self.files = []

    def read(self):
        data_types = [self._get_field_types(cls) for cls in self.file_types]
        data_sources = [self._read_from_file(file, file_type, data_type) for file, file_type, data_type in
                        zip(self.files, self.file_types, data_types)]
        return self.return_data_type(*data_sources, datetime.now())

    @staticmethod
    def _get_field_types(cls):
        return [field.type for field in fields(cls)]

    @staticmethod
    def _read_from_file(input_file, file_type, data_types):
        csv_reader = reader(input_file)
        while True:
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    continue
                return file_type(
                    *[data_type(row[idx]) for idx, data_type in enumerate(data_types)]
                )
            input_file.seek(0)

    def startReading(self):
        self.files = [open(file_name, "r") for file_name in self.file_names]

    def stopReading(self):
        for file in self.files:
            file.close()
        self.files = []
