from seer_study.disclosure import rounded_count

MASK = "<5"


def test_rounded_count_rounds_half_up():
    assert rounded_count(1234, threshold=5, mask=MASK, rounding=10) == 1230
    assert rounded_count(1235, threshold=5, mask=MASK, rounding=10) == 1240
    assert rounded_count(7, threshold=5, mask=MASK, rounding=10) == 10


def test_rounded_count_masks_small_counts_but_not_zero():
    assert rounded_count(3, threshold=5, mask=MASK, rounding=10) == MASK
    assert rounded_count(1, threshold=5, mask=MASK, rounding=10) == MASK
    assert rounded_count(0, threshold=5, mask=MASK, rounding=10) == 0


def test_rounding_of_one_keeps_exact_counts():
    assert rounded_count(1234, threshold=5, mask=MASK, rounding=1) == 1234
