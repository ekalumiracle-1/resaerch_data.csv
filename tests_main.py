
import csv
import os
import tempfile
import unittest

from main import analyse_research_data


class ResearchAnalysisTest(unittest.TestCase):

    def test_mean_and_standard_deviation(self):

        with tempfile.TemporaryDirectory() as folder:

            input_file = os.path.join(folder, "input.csv")
            output_file = os.path.join(folder, "output.csv")

            with open(input_file, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "extract",
                    "microorganism",
                    "replicate",
                    "inhibition_zone_mm"
                ])

                writer.writerow(["A", "Bacteria", 1, 15])
                writer.writerow(["A", "Bacteria", 2, 17])
                writer.writerow(["A", "Bacteria", 3, 16])

            analyse_research_data(input_file, output_file)

            with open(output_file, newline="") as file:
                result = list(csv.DictReader(file))

            self.assertEqual(len(result), 1)
            self.assertEqual(float(result[0]["mean_mm"]), 16.0)
            self.assertEqual(
                float(result[0]["standard_deviation_mm"]),
                1.0
            )
            self.assertEqual(int(result[0]["replicates"]), 3)


if __name__ == "__main__":
    unittest.main()
