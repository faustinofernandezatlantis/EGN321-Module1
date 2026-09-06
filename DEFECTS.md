# EGN 321 — Module 1 Defect Report

## Student Information
- **Name:** [Faustino Fernandez]
- **Date:** September 3, 2026

## Workbook Reviewed
- **Workbook:** `TANK_FILL_rev4.xlsx`
- **Worksheet(s) Reviewed:** `Tank Fill`, `Field Notes`, `Read Me`

## 1. Workbook Purpose
The workbook is designed to log tank-fill runs and estimate the total liquid volume added (in U.S. gallons) across multiple operations. It takes physical tank dimensions (length and width in feet) and measured liquid depth from field logs, converts the volume from cubic feet to U.S. gallons, and aggregates the total volume added across all reported runs.

## 2. Defect Summary

| # | Location | Defect | Correct Behavior | Impact | Confidence |
|---|---|---|---|---|---|
| 1 | `Tank Fill`!E13 | Incorrect depth unit (`2.5` in vs `2.5` ft) | Change E13 to `30` in | Understates R-108 volume by 1,028.57 gal | High |
| 2 | `Tank Fill`!G25 | Truncated sum range (`G6:G17`) | Update formula to `=SUM(G6:G23)` | Omits 6 runs (4,619.22 gal / 35.1% total) | High |
| 3 | `Tank Fill`!G6:G23 | Hardcoded conversion factor (`7.48052`) | Move factor to a parameter cell | Reduces auditability and precision | High |


## 3. Defect 1
### Location
- **Worksheet:** `Tank Fill`
- **Cell/Range:** `E13`

### Existing Formula or Value
`2.5`

### Problem Identified
The value `2.5` was entered directly into column E ("Fill Depth (in)"), treating 2.5 as inches. However, the source log (`Field Notes`!E11) records this measurement as `2.5 ft` with the technician note: *"Handwritten field value entered as recorded"*. 

### Why This Is a Defect
Column E in the `Tank Fill` worksheet explicitly requires depth in **inches**, and the formula in column G (`=C13*D13*(E13/12)*7.48052`) divides `E13` by `12` under the assumption that `E13` is in inches. Entering `2.5` directly caused a double reduction by a factor of 12 (dividing $2.5\text{ ft}$ by $12$ yields $0.2083\text{ ft}$ instead of $2.5\text{ ft}$). $2.5\text{ ft}$ is equivalent to $30\text{ inches}$.

### Correct Formula, Value, Range, or Unit
- **Correct Value:** `30` (inches) in cell `E13`.
- **Alternative Correct Formula:** `=2.5 * 12` in cell `E13`.

### Impact on the Result
The calculated volume for run R-108 in cell `G13` currently evaluates to **93.51 gal**. Correcting `E13` to 30 inches yields the true volume of **1,122.08 gal**, preventing an understatement of **1,028.57 gal** for this single run.

### Estimated Age of the Defect
This defect was introduced when data from the handwritten field log was transcribed into the `Tank Fill` worksheet. Because the operator note in cell `F13` ("Transferred from handwritten field log") explicitly acknowledges manual transfer, the error likely occurred during the manual data entry pass for run R-108.

### Verification
- Hand Calculation: $10\text{ ft} \times 6\text{ ft} \times 2.5\text{ ft} = 150\text{ ft}^3$.
- Volume in gallons: $150\text{ ft}^3 \times 7.48052\text{ gal/ft}^3 = 1,122.078\text{ gal}$.
- Setting `E13` = `30` inches yields $30 / 12 = 2.5\text{ ft}$, matching source record `Field Notes`!E11 ($2.5\text{ ft}$).

---

## 4. Defect 2
### Location
- **Worksheet:** `Tank Fill`
- **Cell/Range:** `G25`

### Existing Formula or Value
`=SUM(G6:G17)`

### Problem Identified
The `SUM` formula in cell `G25` terminates at row 17, completely omitting rows G18 through G23 (Runs R-113 to R-118).

### Why This Is a Defect
Rows 18 through 23 represent valid, fully populated production runs (R-113 through R-118) with measured depths and valid volume calculations in column G. Truncating the range at `G17` silently ignores 6 out of 18 fill operations.

### Correct Formula, Value, Range, or Unit
- **Correct Formula:** `=SUM(G6:G23)`

### Impact on the Result
- Currently reported total volume (`G25`): **8,527.79 gal** (sum of R-101 through R-112).
- True sum of all 18 runs (before Defect 1 correction): **13,147.01 gal**.
- Excluded volume from runs R-113 to R-118: **4,619.22 gal**.
- This single defect causes an unrecorded volume deficit of **35.1%** in the total fill log.

### Estimated Age of the Defect
This defect was introduced when new runs (R-113 through R-118) were appended to the worksheet. Notice that tank dimensions change at row 18 from $10\text{ ft} \times 6\text{ ft}$ to $12\text{ ft} \times 5\text{ ft}$. The original author likely set `=SUM(G6:G17)` when the log only contained 12 runs and failed to update the summary range after adding the new batch of runs.

### Verification
- Highlighted range `G6:G23` in Excel/inspection tool.
- Verified that rows 18–23 contain non-zero, active formulas.
- Re-evaluating `=SUM(G6:G23)` accounts for all 18 runs.

---

## 5. Defect 3
### Location
- **Worksheet:** `Tank Fill`
- **Cell/Range:** `G6:G23`

### Existing Formula or Value
`=C6*D6*(E6/12)*7.48052` (copied down through `G23`)

### Problem Identified
The unit conversion factor `7.48052` (gallons per cubic foot) is hardcoded directly inside every calculation formula as an unexplained "magic number".

### Why This Is a Defect
1. Hardcoding numeric constants directly into formulas violates core software and financial engineering spreadsheet design standards.
2. The exact physical conversion factor for $1\text{ ft}^3$ is $\approx 7.48051948\text{ gal}$. Rounding to `7.48052` introduces truncation error across large volume aggregations.
3. If fluid properties or reference standards change (or if temperature adjustments are needed), updating the factor requires altering every individual row formula rather than updating a single metadata cell, making the workbook prone to silent copy-paste errors.

### Correct Formula, Value, Range, or Unit
- **Correct Approach:** Create a dedicated input/parameter cell (e.g., `Tank Fill`!$C$3 or a named range `GAL_PER_CUFT` set to `7.48051948`).
- **Correct Formula:** `=C6*D6*(E6/12)*$C$3` or `=C6*D6*(E6/12)*GAL_PER_CUFT`.

### Impact on the Result
While the immediate numeric impact per row is small (a fraction of a gallon difference due to rounding), the operational risk is high: future maintainers cannot audit where `7.48052` comes from, nor can they safely update calculation logic without risking formula mismatches.

### Estimated Age of the Defect
This defect was present in the original workbook template architecture (`rev1`). It was copied down to every newly added row during subsequent revisions up to `rev4`.

### Verification
- $1\text{ ft}^3 = \frac{1728\text{ in}^3}{231\text{ in}^3/\text{gal}} \approx 7.48051948051948\text{ gal}$.
- Replacing hardcoded `7.48052` with standard parameters improves precision and eliminates formula complexity across all rows.

---

## 6. Additional Suspected Defects
- **Lack of Input Validation / Boundary Checks (Suspected Defect):**
  - **Location:** `Tank Fill`!E6:E23
  - **Observation:** In row 13 (Run R-108), an erroneous depth reading of `2.5` was entered without triggering any warnings or error flags, even though all neighboring readings range between 8 and 32 inches.
  - **Reasoning:** A tank depth of 2.5 inches represents a ~90% drop from preceding fill runs without explanation. The absence of data validation rules (e.g., min/max depth bounds or anomaly detection) allows severe entry errors to pass unnoticed.

---

## 7. Overall Assessment
**No, I would NOT trust this workbook for a real engineering decision.**

The workbook contains severe structural flaws that lead to significant financial and operational miscalculations:
1. **Unreliable Output:** Due to Defect 1 and Defect 2 combined, the reported total volume in `G25` (**8,527.79 gal**) severely understates the true total volume added (**14,175.59 gal** when fully corrected), missing over **5,647.8 gal** (a **39.8% total error**).
2. **Poor Maintainability:** Formulas contain embedded magic numbers, data entry lacks verification against field logs, and ranges do not dynamically adjust when new runs are added.
3. **Lack of Ownership:** As noted in cell `B28`, the original owner is no longer with the company, and no automated tests or audit trails exist to ensure data integrity.

---

## 8. What Should Become a Python Test?

1. **Unit Consistency & Anomaly Boundary Test (Defect 1 Protection):**
   - *Test Logic:* Read raw field notes and verify that depth units match expected column constraints (e.g., raise an error or auto-convert if field notes state `ft` while input expects `in`). Ensure a run volume does not drop below expected historical operational thresholds without explicit verification.
2. **Dynamic Range Aggregation Test (Defect 2 Protection):**
   - *Test Logic:* Verify that the sum of calculated volumes dynamically includes 100% of populated dataset rows (`df['Calculated Volume (gal)'].sum()`), guaranteeing no rows are omitted regardless of how many runs are appended.
3. **Physical Calculation & Known-Value Test (Defect 3 Protection):**
   - *Test Logic:* Assert that a tank run with dimensions $10\text{ ft} \times 6\text{ ft} \times 12\text{ in}$ ($1\text{ ft}$ depth) calculates to exactly $60 \times 7.48051948 = 448.8311688\text{ gal}$ using double-precision floating-point constants rather than hardcoded truncated factors.