from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from worldmap import plot_world_map


def test_empty_dataframe():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = []
        
        with pytest.raises(RuntimeError, match="No data available to plot. Please check the database content."):
            plot_world_map()

def test_populated_dataframe():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.return_value.fetchall.return_value = [
            (0, 40.7128, -74.0060, 1000000),
            (1, 34.0522, -118.2437, 2000000)
        ]
        mock_cursor.description = [
            ('timezone_offset', None, None, None, None, None, None),
            ('latitude', None, None, None, None, None, None),
            ('longitude', None, None, None, None, None, None),
            ('estimated_number_of_households', None, None, None, None, None, None)
        ]

        try:
            df = plot_world_map()
            assert not df.empty
            assert len(df) == 2
            assert df['latitude'].iloc[0] == 40.7128
            assert df['longitude'].iloc[1] == -118.2437
        except RuntimeError:
            pytest.fail("plot_world_map raised RuntimeError unexpectedly!")
