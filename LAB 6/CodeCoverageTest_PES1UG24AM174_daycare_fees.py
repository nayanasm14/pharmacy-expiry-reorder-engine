"""Code (line) coverage tests for daycare_fees.py.

Goal: execute every line of daycare_fees.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM174_daycare_fees.py
    coverage report -m
"""
import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


# ---------- extra_hours_fee ----------

def test_within_included_hours():
    # extra <= 0 -> return 0
    assert extra_hours_fee("toddler", 20, False) == 0


def test_unknown_age_group_raises():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("teen", 10, False)


def test_negative_hours_raises():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


def test_preschool_with_sibling_extra_hours():
    # included = 30 + 5 (sibling) = 35, extra = 5, rate = 9
    assert extra_hours_fee("preschool", 40, True) == 45


def test_infant_more_than_20_extra_hours():
    # included = 20, extra = 25, rate = 14 + 5 + 3 = 22
    assert extra_hours_fee("infant", 45, False) == 550


# ---------- enrolment_allowed ----------

def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True


def test_enrolment_immunisation_pending_old_enough():
    assert enrolment_allowed(15, 0, True) is True


def test_enrolment_too_young():
    assert enrolment_allowed(3, 5, False) is False


# ---------- pickup_status ----------

def test_pickup_aftercare_on_time():
    # cutoff = 20
    assert pickup_status(25, True, False) == "on_time"


def test_pickup_friday_late():
    # cutoff = 10 + 10 = 20; 5 >= 20 - 15 -> late
    assert pickup_status(5, False, True) == "late"


def test_pickup_overdue():
    # cutoff = 20 + 10 = 30; 0 < 15 -> overdue
    assert pickup_status(0, True, True) == "overdue"
