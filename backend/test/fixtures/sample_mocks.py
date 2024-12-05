from datetime import datetime

import pytest

from app.utils.classes import Magazine, ArticlePageScan, ArticleFigure, Article


@pytest.fixture
def mock_magazine():
    return Magazine(
        id="1",
        name="Test Magazine",
        date=datetime(2024, 1, 1),
        publisher="Publisher A",
        edition="First Edition",
        abstract="Test abstract",
        genres=["genre1"],
        categories=["cat1"],
        created_on=datetime(2024, 1, 1),
        edited_on=datetime(2024, 1, 2)
    )


@pytest.fixture
def mock_article():
    return Article(
        id="1",
        magazine_id="1",
        title="Test Article",
        author="John Doe",
        content="Some content",
        page_offsets=[1, 2],
        page_range=[3, 4],
        page_scans=[ArticlePageScan(1, "image_data_1", datetime(2024, 1, 1))],
        figures=[ArticleFigure(1, "Caption 1", "image_data_2")],
        created_on=datetime(2024, 1, 1),
        edited_on=datetime(2024, 1, 2)
    )
