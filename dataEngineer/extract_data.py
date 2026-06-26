import subprocess
import os

# Configuration
BASE_DIR = r"C:\Users\Developer\Documents\Projects\final-ml-project"
QGIS_BATCH = r"C:\Program Files\QGIS 3.44.11\bin\qgis_process-qgis-ltr.bat"
VECTOR_INPUT = rf"{BASE_DIR}\cobertura_elev_prec.gpkg"
OUTPUT_GPKG = rf"{BASE_DIR}\zonal_statistics_all_months.gpkg"

# Month mapping: (two-digit month, 3-letter prefix with underscore)
MONTHS = [
    ("09", "sep_"),
    ("10", "oct_"),
    ("11", "nov_"),
    ("12", "dic_"),
]
RASTER_BAND = 1
STATISTICS = [2, 5, 6, 7]

for month_num, prefix in MONTHS:
    raster_path = rf"{BASE_DIR}\wc2.1_30s_prec_{month_num}.tif"
    if not os.path.exists(raster_path):
        print(f"Warning: Raster file not found for month {month_num}: {raster_path}")
        continue
    print(f"Processing month {month_num} ({prefix})...")
    
    # Use the batch file which sets up all QGIS environment variables
    params = f'{{"INPUT":"{VECTOR_INPUT}","INPUT_RASTER":"{raster_path}","RASTER_BAND":{RASTER_BAND},"COLUMN_PREFIX":"{prefix}","STATISTICS":[2,5,6,7],"OUTPUT":"{OUTPUT_GPKG}"}}'
    
    # Call through cmd.exe to use the batch file
    cmd = f'cmd /c "{QGIS_BATCH}" --tool native:zonalstatisticsfb --params "{params}" --output json'
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Completed: {prefix} columns added to {OUTPUT_GPKG}")
    else:
        print(f"  Error (exit code {result.returncode}): {result.stderr[:200]}")

print(f"\nAll months processed successfully!")
print(f"Output saved to: {OUTPUT_GPKG}")
   
