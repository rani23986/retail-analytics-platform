import os


class DataSaver:

    def __init__(self, output_path):
        self.output_path = output_path

    def save_all(self, datasets):

        os.makedirs(self.output_path, exist_ok=True)

        for name, df in datasets.items():

            output_file = os.path.join(self.output_path, name)

            df.to_csv(output_file, index=False)

        print("All cleaned datasets saved successfully.")