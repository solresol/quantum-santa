from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from worldmap import plot_world_map


@pytest.fixture
def mock_empty_db():
    with patch('worldmap.sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = []
        yield mock_conn

@pytest.fixture
def mock_malformed_db():
    with patch('worldmap.sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = [('invalid',)]
        yield mock_conn

@pytest.fixture
def mock_populated_db():
    with patch('worldmap.sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = [
            (0, 45.0, 90.0, 1000000),
            (1, 50.0, 100.0, 2000000)
        ]
        yield mock_conn

def test_empty_database(mock_empty_db):
    df = plot_world_map()
    assert df.empty

def test_malformed_database(mock_malformed_db):
    df = plot_world_map()
    assert df.empty

def test_populated_database(mock_populated_db):
    df = plot_world_map()
    assert not df.empty
    assert len(df) == 2
    assert df.iloc[0]['latitude'] == 45.0
    assert df.iloc[1]['longitude'] == 100.0
