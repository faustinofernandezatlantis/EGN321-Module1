"""
Module: tank_fill
Description: Rebuilds tank-fill volume calculation for EGN 321 Module 1.
Replaces the inherited spreadsheet calculation with pure functions, explicit 
unit handling, validation, and documented physical constants.
"""

# Physical constant: U.S. Gallons per cubic foot
# 1 cu ft = (12 in)^3 / (231 in^3 / gal) = 1728 / 231 ≈ 7.48051948 gal
GALLONS_PER_CUBIC_FOOT: float = 7.48051948
INCHES_PER_FOOT: float = 12.0


def calculate_tank_volume(length_ft: float, width_ft: float, depth_in: float) -> float:
    """
    Calculates the liquid volume added to a rectangular tank in U.S. gallons.

    Parameters
    ----------
    length_ft : float
        Tank length in feet. Must be strictly positive (> 0).
    width_ft : float
        Tank width in feet. Must be strictly positive (> 0).
    depth_in : float
        Liquid depth added in inches. Must be strictly positive (> 0).

    Returns
    -------
    float
        Calculated liquid volume in U.S. gallons.

    Raises
    ------
    ValueError
        If length_ft, width_ft, or depth_in are less than or equal to zero.
    TypeError
        If any input is not a real numeric value (int or float).
    """
    # Type validation
    for param_name, param_val in [
        ("length_ft", length_ft),
        ("width_ft", width_ft),
        ("depth_in", depth_in),
    ]:
        if isinstance(param_val, bool) or not isinstance(param_val, (int, float)):
            raise TypeError(f"{param_name} must be a valid number (int or float). Got: {type(param_val).__name__}")

    # Boundary / value validation
    if length_ft <= 0:
        raise ValueError(f"Tank length must be strictly positive (> 0). Received: {length_ft}")
    if width_ft <= 0:
        raise ValueError(f"Tank width must be strictly positive (> 0). Received: {width_ft}")
    if depth_in <= 0:
        raise ValueError(f"Fill depth must be strictly positive (> 0). Received: {depth_in}")

    # Unit conversions
    depth_ft: float = depth_in / INCHES_PER_FOOT

    # Volume calculation in cubic feet
    volume_cuft: float = length_ft * width_ft * depth_ft

    # Convert cubic feet to U.S. gallons
    volume_gallons: float = volume_cuft * GALLONS_PER_CUBIC_FOOT

    return volume_gallons
