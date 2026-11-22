"""Daycare enrolment parsing, hours averaging and fee calculation.

Hardened version (Lab 7): every function validates its input and
returns None for anything invalid instead of crashing.
"""
import math

VALID_AGE_GROUPS = {"infant", "toddler", "preschool"}
MAX_WEEKLY_HOURS = 168  # hours in a week
GST_RATE = 1.18


def _to_finite_float(value):
    """Convert a string to a finite float, or return None."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):  # rejects nan, inf, -inf
        return None
    return number


def parse_enrolment(text):
    """Parse 'age_group:hours' into (Age_group, hours) or return None."""
    if not isinstance(text, str) or text.count(":") != 1:
        return None
    age_group, hours = text.split(":")
    age_group = age_group.strip().lower()
    if age_group not in VALID_AGE_GROUPS:
        return None
    hours = _to_finite_float(hours.strip())
    if hours is None or not 0 <= hours <= MAX_WEEKLY_HOURS:
        return None
    return age_group.title(), hours


def hours_average(hours_csv):
    """Return the mean of comma-separated weekly hours or None."""
    if not isinstance(hours_csv, str) or not hours_csv.strip():
        return None
    values = []
    for raw in hours_csv.split(","):
        value = _to_finite_float(raw.strip())
        if value is None or not 0 <= value <= MAX_WEEKLY_HOURS:
            return None
        values.append(value)
    # true division: the original used // and silently truncated
    return round(sum(values) / len(values), 2)


def payable_fee(text):
    """Return fee * GST - discount (never below 0) from 'fee|discount'."""
    if not isinstance(text, str) or text.count("|") != 1:
        return None
    fee, discount = text.split("|")
    fee = _to_finite_float(fee.strip())
    discount = _to_finite_float(discount.strip())
    if fee is None or discount is None or fee < 0 or discount < 0:
        return None
    total = fee * GST_RATE - discount
    if not math.isfinite(total):  # e.g. fee near float max overflows
        return None
    return round(max(total, 0.0), 2)


def main():
    """Read each input from the user and print the result."""
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    if result is None:
        print("Invalid input: use infant/toddler/preschool:hours (0-168)")
    else:
        print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    if result is None:
        print("Invalid input: use comma-separated numbers between 0 and 168")
    else:
        print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    if result is None:
        print("Invalid input: use non-negative numbers as fee|discount")
    else:
        print("Payable Fee:", result)


if __name__ == "__main__":
    main()
