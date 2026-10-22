from src.clean_data import clean_email, clean_name, clean_phone


def test_clean_name():
    assert clean_name("  BLUE SKY CONSULTING  ") == "Blue Sky Consulting"
    assert clean_name("Desert Peak  Services") == "Desert Peak Services"


def test_clean_email():
    assert clean_email(" ACCOUNTS@BLUESKY.COM ") == "accounts@bluesky.com"
    assert clean_email("") == ""


def test_clean_phone():
    assert clean_phone("(602) 555-0102") == "602-555-0102"
    assert clean_phone("6025550101") == "602-555-0101"
    assert clean_phone("") == ""
