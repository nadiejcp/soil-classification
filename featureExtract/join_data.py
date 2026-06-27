import glob
import os
import pandas as pd
from pathlib import Path

try:
    import geopandas as gpd
except ImportError:
    print("geopandas is required. Install with: pip install geopandas")
    exit(1)


# ──────────────────────────────────────────────
# PART 1 — List .gpkg files & extract attributes to CSV
# ──────────────────────────────────────────────

def get_month_initial():
  """Return the first letter of each month."""
  months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
  ]
  return [m[0] for m in months]


def list_gpkg_files(directory, pattern="*.gpkg"):
  """List all .gpkg files in the given directory."""
  month_initials = get_month_initial()
  gpkg_files = glob.glob(os.path.join(directory, pattern))

  # Filter to only files whose first character is a month initial
  filtered = [f for f in gpkg_files if os.path.basename(f)[0].upper() in month_initials]
  return sorted(filtered)


def extract_attributes_to_csv(gpkg_path, output_dir=None):
  """Load a .gpkg file and extract all attribute table fields into a CSV."""
  base_name = Path(gpkg_path).stem  # e.g., "J_data"
  if os.path.isfile(os.path.join(output_dir, f"{base_name}_{base_name}.csv")):
    print(f"Skipping {base_name}_{base_name}.csv (already exists)")
    return os.path.join(output_dir, f"{base_name}_{base_name}.csv")
  gdf = gpd.read_file(gpkg_path)

  # Get the layer name (first available layer in the GeoPackage)
  layer_name = gdf._layer if hasattr(gdf, '_layer') else Path(gpkg_path).stem

  # Build output filename: use the month-initial prefix + layer name
  csv_filename = f"{base_name}_{layer_name}.csv"

  if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, csv_filename)
  else:
    csv_path = os.path.join(os.path.dirname(gpkg_path), csv_filename)

  # Drop geometry column for the CSV (keep only attribute fields)
  df = gdf.drop(columns=gdf.geometry.name) if hasattr(gdf, 'geometry') and gdf.geometry is not None else pd.DataFrame()

  # Save to CSV
  df.to_csv(csv_path, index=False)
  print(f"  Saved: {csv_path} ({len(df)} rows, {len(df.columns)} columns)")
  return csv_path


# ──────────────────────────────────────────────
# PART 2 — Load CSVs, JOIN on OBJECTID, drop duplicates
# ──────────────────────────────────────────────

def load_csv_files(directory):
  """Load all CSV files from a directory into a dict of DataFrames."""
  csv_files = glob.glob(os.path.join(directory, "*.csv"))
  dfs = {}
  for f in sorted(csv_files):
    name = Path(f).stem  # e.g., "J_layer1"
    df = pd.read_csv(f)
    dfs[name] = df
    print(f"  Loaded: {os.path.basename(f)} ({len(df)} rows, {len(df.columns)} columns)")
  return dfs


def join_csvs_on_objectid(dfs):
  """
  Join all DataFrames on OBJECTID column.
  - Inner join keeps only rows where OBJECTID exists in ALL tables.
  - Drops duplicate columns (columns that appear in multiple DFs except the key).
  """
  if not dfs:
      return pd.DataFrame()

  # Verify OBJECTID exists in every DataFrame
  for name, df in dfs.items():
    if "OBJECTID" not in df.columns:
      print(f"  WARNING: '{name}' does NOT have an OBJECTID column — skipping.")
      return None

  # Start with the first DataFrame
  result = list(dfs.values())[0]
  remaining_keys = list(dfs.keys())[1:]

  for key in remaining_keys:
    df = dfs[key]

    # Identify duplicate columns (same name in both, excluding OBJECTID)
    common_cols = set(result.columns) & set(df.columns) - {"OBJECTID"}

    if common_cols:
      print(f"  Dropping duplicate columns from '{key}': {common_cols}")
      df = df.drop(columns=common_cols)

    # Inner join on OBJECTID
    result = pd.merge(
      result, df,
      on="OBJECTID",
      how="inner",
      suffixes=("_left", "_right")
    )

  return result


def main():
  # ── Step 1: Extract .gpkg → CSV ──
  print("=" * 60)
  print("STEP 1: Extract GeoPackage attributes to CSV")
  print("=" * 60)

  gpkg_dir = Path(__file__).parent  # Default to script directory
  output_dir = Path(__file__).parent  # Default to script directory

  print(f"\nSearching in: {gpkg_dir}")
  print(f"Month initials used: {get_month_initial()}\n")

  gpkg_files = list_gpkg_files(gpkg_dir)
  gpkg_files.append(os.path.join(gpkg_dir, "cobertura_elev_prec.gpkg"))  # Include the combined file if it exists
  gpkg_files.append(os.path.join(gpkg_dir, "bulk.gpkg"))  # Include the combined file if it exists
  gpkg_files.append(os.path.join(gpkg_dir, "cation.gpkg"))  # Include the combined file if it exists
  gpkg_files.append(os.path.join(gpkg_dir, "nitrogen.gpkg"))  # Include the combined file if it exists
  gpkg_files.append(os.path.join(gpkg_dir, "soc.gpkg"))  # Include the combined file if it exists
  print(f"\nTotal files: {len(gpkg_files)}\n")
  csv_paths = []
  for gpkg_path in gpkg_files:
    try:
      csv_path = extract_attributes_to_csv(gpkg_path, output_dir)
      csv_paths.append(csv_path)
    except Exception as e:
      print(f"  ERROR processing {os.path.basename(gpkg_path)}: {e}")

  # ── Step 2: Load CSVs & JOIN on OBJECTID ──
  print("\n" + "=" * 60)
  print("STEP 2: Load CSVs and JOIN on OBJECTID")
  print("=" * 60)

  csv_dir = output_dir if output_dir else gpkg_dir
  dfs = load_csv_files(csv_dir)

  if not dfs:
    print("No CSV files found to join.")
    return

  result = join_csvs_on_objectid(dfs)

  if result is None or result.empty:
    print("Join produced no results. Check that OBJECTID values match across tables.")
    return

  # Save the joined result
  output_csv = os.path.join(csv_dir, "joined_all_tables.csv")
  result.to_csv(output_csv, index=False)
  print(f"\n  Joined result saved to: {output_csv} ({len(result)} rows, {len(result.columns)} columns)")


if __name__ == "__main__":
  main()
