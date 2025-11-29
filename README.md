# CT Preprocessing Scripts

This project contains two scripts to normalize NIfTI CT scans using **MONAI**.

### 1. `main.py` (Preprocessing)
Performs batch processing on raw data with the following steps:
* **Recursive Search:** Finds all `.nii.gz` files in nested directories.
* **Reorientation:** Standardizes image orientation to **RAS** (Right-Anterior-Superior).
* **Intensity Clipping:** Clamps pixel values (HU) to the range **[-50, 250]** to focus on relevant tissue.
* **Output:** Saves processed images while strictly preserving the original folder structure (Patient/Series hierarchy).

### 2. `verify_data.py` (Validation)
A helper script to verify the processing results.
* Iterates through the output folder.
* Checks min/max pixel values for every file.
* Confirms that all data falls strictly within the **[-50, 250]** range.

### Requirements
* `monai`
* `nibabel`
* `numpy`
