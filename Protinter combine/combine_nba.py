import pandas as pd
import numpy as np

def process_csv(file_path):
    """
    Reads a CSV file, assumes header is present and the 5th column contains the distance values.
    Returns a pandas Series of float distances.
    """
    df = pd.read_csv(file_path)
    # Assuming the fifth column (index 4) contains the distance values.
    # Convert to numeric (ignoring non-numeric issues) and drop NaN values.
    distances = pd.to_numeric(df.iloc[:, 4], errors='coerce').dropna()
    return distances

def compute_stats(series):
    """
    Given a pandas Series, compute a dictionary with common stats.
    """
    stats = {}
    stats['count'] = series.count()
    stats['mean'] = series.mean() if stats['count'] > 0 else np.nan
    stats['stdev'] = series.std() if stats['count'] > 1 else np.nan
    stats['min'] = series.min() if stats['count'] > 0 else np.nan
    stats['q0.25'] = series.quantile(0.25) if stats['count'] > 0 else np.nan
    stats['q0.5'] = series.quantile(0.5) if stats['count'] > 0 else np.nan
    stats['q0.75'] = series.quantile(0.75) if stats['count'] > 0 else np.nan
    stats['max'] = series.max() if stats['count'] > 0 else np.nan
    return stats

# File names and corresponding desired stats in order
files_and_stats = [
    # (filename, [list of desired stat keys in order])
    ("result_hydrophobic.csv", ["stdev", "min", "q0.5"]),
    ("result_hbond_main_side.csv", ["count", "mean", "stdev", "min", "max"]),
    ("result_arosul.csv", ["count", "stdev", "min"]),
    ("result_hbond_side_side.csv", ["count", "stdev", "min"]),
    ("result_disulphide.csv", ["count", "stdev", "q0.5"]),
    ("result_ionic.csv", ["count", "stdev", "min", "q0.25"]),
    ("result_hbond_main_main.csv", ["count", "mean", "stdev", "min", "q0.25", "q0.5", "q0.75", "max"]),
    ("result_cationpi.csv", ["count", "stdev", "min"]),
    ("result_aroaro.csv", ["count", "stdev", "min"]),
]

# Create a list to hold all output values in the specified order.
output_values = []

for filename, stat_keys in files_and_stats:
    try:
        distances = process_csv(filename)
        stats = compute_stats(distances)
        # Append each requested statistic in order
        for key in stat_keys:
            output_values.append(stats.get(key, np.nan))
    except Exception as e:
        # In case the file is missing or an error occurs, append NaNs for the expected number of stats.
        print(f"Error processing {filename}: {e}")
        output_values.extend([np.nan] * len(stat_keys))

# Create a DataFrame with one row containing all the parameters.
# Define column names in the order specified.
columns = [
    "hydrophobic_stdev", "hydrophobic_min", "hydrophobic_0.5",
    "hbond_main_side_count", "hbond_main_side_mean", "hbond_main_side_stdev", "hbond_main_side_min", "hbond_main_side_max",
    "arosul_count", "arosul_stdev", "arosul_min",
    "hbond_side_side_count", "hbond_side_side_stdev", "hbond_side_side_min",
    "disulphide_count", "disulphide_stdev", "disulphide_0.5",
    "ionic_count", "ionic_stdev", "ionic_min", "ionic_0.25",
    "hbond_main_main_count", "hbond_main_main_mean", "hbond_main_main_stdev", "hbond_main_main_min",
    "hbond_main_main_0.25", "hbond_main_main_0.5", "hbond_main_main_0.75", "hbond_main_main_max",
    "cationpi_count", "cationpi_stdev", "cationpi_min",
    "aroaro_count", "aroaro_stdev", "aroaro_min"
]

if len(output_values) != len(columns):
    print("Warning: Number of computed values does not match expected columns!")

result_df = pd.DataFrame([output_values], columns=columns)

# Write the resulting DataFrame to a CSV file.
result_df.to_csv("combined_results.csv", index=False)
print("Combined results written to combined_results.csv")
