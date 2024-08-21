import pytest
import pandas as pd
from src.scraper import scrape_quotes

def test_scrape_quotes():
    df = scrape_quotes()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert 'text' in df.columns
    assert 'author' in df.columns
    assert 'tags' in df.columns
    assert 'about' in df.columns

if __name__ == '__main__':
    pytest.main()
