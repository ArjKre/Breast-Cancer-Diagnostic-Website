import shutil
from pathlib import Path

import pandas as pd

ROOT = Path("../dataset")
CSV_DIR = ROOT / "csv"
JPEG_DIR = ROOT / "jpeg"

BENIGN_DIR = ROOT / "benign"
MALIGNANT_DIR = ROOT / "malignant"

BENIGN_DIR.mkdir(parents=True, exist_ok=True)
MALIGNANT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Load metadata
# -------------------------

mass_train = pd.read_csv(CSV_DIR / "mass_case_description_train_set.csv")

mass_test = pd.read_csv(CSV_DIR / "mass_case_description_test_set.csv")

calc_train = pd.read_csv(CSV_DIR / "calc_case_description_train_set.csv")

calc_test = pd.read_csv(CSV_DIR / "calc_case_description_test_set.csv")

cases = pd.concat(
    [
        mass_train,
        mass_test,
        calc_train,
        calc_test,
    ],
    ignore_index=True,
)

dicom_info = pd.read_csv(CSV_DIR / "dicom_info.csv")

# -------------------------
# Build lookup table
# -------------------------

lookup = {}

for _, row in dicom_info.iterrows():
    image_path = str(row["image_path"])

    jpeg_folder = Path(image_path).parent.name

    lookup[jpeg_folder] = image_path

# -------------------------
# Copy images
# -------------------------

copied = 0
missing = 0

for _, row in cases.iterrows():
    pathology = str(row["pathology"]).strip()

    image_file_path = str(row["image file path"])

    parts = image_file_path.split("/")

    if len(parts) < 2:
        continue

    jpeg_folder = parts[2]

    if jpeg_folder not in lookup:
        missing += 1
        continue

    jpg_rel_path = lookup[jpeg_folder]

    jpg_name = Path(jpg_rel_path).name

    jpg_source = JPEG_DIR / jpeg_folder / jpg_name

    if not jpg_source.exists():
        missing += 1
        continue

    if pathology == "MALIGNANT":
        target_dir = MALIGNANT_DIR

    elif pathology in [
        "BENIGN",
        "BENIGN_WITHOUT_CALLBACK",
    ]:
        target_dir = BENIGN_DIR

    else:
        continue

    new_name = f"{copied}_{jpg_name}"

    shutil.copy2(
        jpg_source,
        target_dir / new_name,
    )

    copied += 1

print(f"Copied: {copied}")
print(f"Missing: {missing}")
