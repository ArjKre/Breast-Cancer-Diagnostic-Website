from pathlib import Path

dataset = Path("../dataset")

benign = list((dataset / "benign").glob("*"))
malignant = list((dataset / "malignant").glob("*"))

print(f"Benign Images: {len(benign)}")
print(f"Malignant Images: {len(malignant)}")
