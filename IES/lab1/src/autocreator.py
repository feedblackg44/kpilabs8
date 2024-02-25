import csv
import random


class AutoCreator:
    def __init__(self, *_, **kwargs) -> None:
        data_names = kwargs.get("data_names", None)
        data_types = kwargs.get("data_type", [float])
        bounds = kwargs.get("bounds", [(0, 10)])

        self.data_names = data_names
        self.data_types = data_types
        self.bounds = bounds

    def create(self, filename: str, row_count: int):
        with open(filename, "w") as file:
            writer = csv.writer(file)
            if self.data_names is not None:
                writer.writerow(self.data_names)
            for _ in range(row_count):
                writer.writerow(self._generate_row())

    def _generate_row(self):
        return [self._generate_data(data_type, bounds) for data_type, bounds in zip(self.data_types, self.bounds)]

    @staticmethod
    def _generate_data(data_type, bounds):
        if data_type == int:
            return random.randint(*bounds)
        return random.uniform(*bounds)

