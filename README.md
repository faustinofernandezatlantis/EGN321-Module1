# Tank Fill Calculation Tool

## Purpose
This tool replaces the legacy spreadsheet calculation (`TANK_FILL_rev4.xlsx`) with a reliable, testable, and maintainable Python implementation. It computes the total liquid volume added (in U.S. gallons) to rectangular storage tanks during fill operations.

## Inputs

| Input | Description | Unit |
|---|---|---|
| `length_ft` | Tank base length | Feet (`ft`) |
| `width_ft` | Tank base width | Feet (`ft`) |
| `depth_in` | Measured liquid depth added | Inches (`in`) |

## Output
- **Calculated Volume:** Total liquid volume added, returned in U.S. Gallons (`gal`).

## Calculation
The calculation process follows three steps:
1. Converts the fill depth from inches to feet ($depth\_ft = depth\_in / 12$).
2. Computes the liquid volume in cubic feet ($volume\_cuft = length\_ft \times width\_ft \times depth\_ft$).
3. Converts the cubic feet volume into U.S. gallons using the conversion factor ($volume\_gallons = volume\_cuft \times 7.48051948$).

## Formula / Constant Source
- **Volumetric Conversion Factor:** `GALLONS_PER_CUBIC_FOOT = 7.48051948`
- **Source:** Exact physical relationship where $1\text{ cu ft} = 1728\text{ in}^3 / 231\text{ in}^3\text{ per U.S. gallon} \approx 7.48051948\text{ gal}$.

## Assumptions
- The storage tank is rectangular with uniform vertical cross-sections.
- Temperature and liquid expansion effects are negligible.
- Inputs represent active, non-zero positive liquid fill measurements.

## Inputs the Tool Rejects
- **Negative or Zero Dimensions:** Any value where `length_ft <= 0`, `width_ft <= 0`, or `depth_in <= 0` raises a `ValueError`.
- **Invalid Data Types:** Any non-numeric input (such as strings, `None`, or boolean values) raises a `TypeError`.

## Known Limitations
- Does not support cylindrical, conical, or irregular tank geometries.
- Does not account for fluid density, temperature expansion, or ullage limits.

## Verification & Test Cases

The tool is verified against known-correct rows from `TANK_FILL_rev4.xlsx`:
1. **Run R-101:** $10\text{ ft} \times 6\text{ ft} \times 24\text{ in} \rightarrow 897.66\text{ gal}$
2. **Run R-113:** $12\text{ ft} \times 5\text{ ft} \times 18\text{ in} \rightarrow 673.25\text{ gal}$
3. **Defect 1 Regression (Run R-108):** Ensures $2.5\text{ ft}$ from field notes is passed as $30\text{ in}$, resulting in $1122.08\text{ gal}$ instead of the erroneous $93.51\text{ gal}$.

## Running the Code
Import the function in Python:

```python
from src.tank_fill import calculate_tank_volume

volume = calculate_tank_volume(length_ft=10.0, width_ft=6.0, depth_in=24.0)

Running the Tests

pytest
