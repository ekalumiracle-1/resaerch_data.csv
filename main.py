import csv
import math
from collections import defaultdict


def analyse_research_data(input_file, output_file):
    """
    Analyse antimicrobial inhibition-zone measurements.

    Calculates:
    - Number of replicates
    - Mean inhibition zone
    - Sample standard deviation
    """

    results = defaultdict(list)

    # Read experimental data
    with open(input_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "extract",
            "microorganism",
            "replicate",
            "inhibition_zone_mm"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV file is missing required columns.")

        for row in reader:
            extract = row["extract"].strip()
            microorganism = row["microorganism"].strip()

            if not extract or not microorganism:
                raise ValueError("Extract and microorganism cannot be empty.")

            replicate = int(row["replicate"])
            measurement = float(row["inhibition_zone_mm"])

            if replicate < 1:
                raise ValueError("Replicate must be at least 1.")

            if not math.isfinite(measurement) or measurement < 0:
                raise ValueError("Measurement must be a finite non-negative number.")

            key = (extract, microorganism)
            results[key].append(measurement)

    if not results:
        raise ValueError("No experimental measurements found.")

    # Calculate statistical summaries
    with open(output_file, "w", newline="") as file:
        fieldnames = [
            "extract",
            "microorganism",
            "replicates",
            "mean_mm",
            "standard_deviation_mm"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for (extract, microorganism), values in sorted(results.items()):

            count = len(values)
            mean = sum(values) / count

            # Sample standard deviation
            if count > 1:
                variance = sum(
                    (value - mean) ** 2 for value in values
                ) / (count - 1)

                standard_deviation = math.sqrt(variance)
            else:
                standard_deviation = 0.0

            writer.writerow({
                "extract": extract,
                "microorganism": microorganism,
                "replicates": count,
                "mean_mm": round(mean, 2),
                "standard_deviation_mm": round(
                    standard_deviation, 2
                )
            })

    print("Research data analysis completed!")
    print("Results saved to:", output_file)


if __name__ == "__main__":
    analyse_research_data(
        "research_data.csv",
        "results.csv"
    )
