import pytest
from src.tank_fill import calculate_tank_volume, GALLONS_PER_CUBIC_FOOT

# ----------------------------------------------------------------------
# 1. Known-Correct Workbook Cases (2 required)
# ----------------------------------------------------------------------

def test_known_correct_run_101():
    """Verify Run R-101 against verified workbook values (10ft x 6ft x 24in)."""
    result = calculate_tank_volume(length_ft=10.0, width_ft=6.0, depth_in=24.0)
    expected = 10.0 * 6.0 * (24.0 / 12.0) * GALLONS_PER_CUBIC_FOOT
    assert result == pytest.approx(expected, rel=1e-5)
    assert result == pytest.approx(897.662, abs=1e-2)


def test_known_correct_run_113():
    """Verify Run R-113 against verified workbook values (12ft x 5ft x 18in)."""
    result = calculate_tank_volume(length_ft=12.0, width_ft=5.0, depth_in=18.0)
    expected = 12.0 * 5.0 * (18.0 / 12.0) * GALLONS_PER_CUBIC_FOOT
    assert result == pytest.approx(expected, rel=1e-5)
    assert result == pytest.approx(673.247, abs=1e-2)


# ----------------------------------------------------------------------
# 2. Defect Regression Case (Defect 1 Protection)
# ----------------------------------------------------------------------

def test_defect1_regression_unit_conversion():
    """
    Regression Test for Defect 1 (Run R-108):
    Ensures that depth_in=30.0 (converted from 2.5 ft) computes ~1122.08 gal.
    """
    wrong_spreadsheet_volume = 10.0 * 6.0 * (2.5 / 12.0) * 7.48052  # ~93.51 gal
    correct_volume = calculate_tank_volume(length_ft=10.0, width_ft=6.0, depth_in=30.0)
    
    assert correct_volume == pytest.approx(1122.078, abs=1e-2)
    assert correct_volume > wrong_spreadsheet_volume * 10


# ----------------------------------------------------------------------
# 3. Invalid-Input Cases (2 required)
# ----------------------------------------------------------------------

def test_reject_negative_or_zero_dimensions():
    """Verify that negative or zero dimensions raise ValueError."""
    with pytest.raises(ValueError, match="Tank length must be strictly positive"):
        calculate_tank_volume(length_ft=-10.0, width_ft=6.0, depth_in=24.0)

    with pytest.raises(ValueError, match="Tank width must be strictly positive"):
        calculate_tank_volume(length_ft=10.0, width_ft=0.0, depth_in=24.0)

    with pytest.raises(ValueError, match="Fill depth must be strictly positive"):
        calculate_tank_volume(length_ft=10.0, width_ft=6.0, depth_in=-5.0)


def test_reject_invalid_input_types():
    """Verify that non-numeric types raise TypeError."""
    with pytest.raises(TypeError, match="length_ft must be a valid number"):
        calculate_tank_volume(length_ft="10", width_ft=6.0, depth_in=24.0)

    with pytest.raises(TypeError, match="depth_in must be a valid number"):
        calculate_tank_volume(length_ft=10.0, width_ft=6.0, depth_in=None)
