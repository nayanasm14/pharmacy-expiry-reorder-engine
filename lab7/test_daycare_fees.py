"""Hypothesis fuzz tests for daycare_fees.py (Lab 7).

Run: python3 -m pytest test_daycare_fees.py
"""
import math

from hypothesis import given, settings, strategies as st
from daycare_fees import parse_enrolment, hours_average, payable_fee

AGE_GROUPS = st.sampled_from(["infant", "toddler", "preschool"])
HOURS = st.floats(min_value=0, max_value=168, allow_nan=False)
WHOLE_HOURS = st.integers(min_value=0, max_value=168)
MONEY = st.floats(min_value=0, max_value=1e9, allow_nan=False)

# Random text plus inputs that look almost valid (the usual bug triggers)
NASTY_TEXT = (
    st.text()
    | st.none()
    | st.sampled_from(["", ":", "|", ",", "toddler:", ":25", "a:b:c",
                       "toddler:nan", "toddler:inf", "toddler:-5",
                       "20,,30", "nan,20", "3000|nan", "1e308|0",
                       "-100|5", "3000|250|10"])
)


# ---------- 1. No-crash fuzzing: any input, the function must not raise ----

@settings(max_examples=500)
@given(NASTY_TEXT)
def test_parse_enrolment_no_crash(s):
    try:
        parse_enrolment(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_enrolment crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(NASTY_TEXT)
def test_hours_average_no_crash(s):
    try:
        hours_average(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"hours_average crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(NASTY_TEXT)
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"payable_fee crashed on {s!r} with: {e!r}"


# ---------- 2. Output must always be sensible (no nan / inf / negatives) ---

@given(NASTY_TEXT)
def test_parse_enrolment_output_is_valid(s):
    try:
        result = parse_enrolment(s)
    except Exception:  # pylint: disable=broad-except
        return  # crashes are reported by the no-crash test
    if result is not None:
        _, hours = result
        assert math.isfinite(hours) and 0 <= hours <= 168, result


@given(NASTY_TEXT)
def test_payable_fee_output_is_valid(s):
    try:
        result = payable_fee(s)
    except Exception:  # pylint: disable=broad-except
        return
    if result is not None:
        assert math.isfinite(result) and result >= 0, result


# ---------- 3. Correct results for valid generated inputs -----------------

@given(AGE_GROUPS, HOURS)
def test_parse_enrolment_valid_roundtrip(age_group, hours):
    assert parse_enrolment(f"  {age_group} : {hours}") == (
        age_group.title(), hours)


@given(st.lists(WHOLE_HOURS, min_size=1, max_size=20))
def test_hours_average_matches_true_mean(values):
    csv = ",".join(str(v) for v in values)
    expected = sum(values) / len(values)
    assert math.isclose(hours_average(csv), expected, abs_tol=0.01)


@given(MONEY, MONEY)
def test_payable_fee_matches_formula(fee, discount):
    expected = max(fee * 1.18 - discount, 0)
    assert math.isclose(payable_fee(f"{fee}|{discount}"), expected,
                        rel_tol=1e-9, abs_tol=0.01)
