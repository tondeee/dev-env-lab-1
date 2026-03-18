import os
import sys
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import visualization


class VisualizationPathTests(unittest.TestCase):
    def test_uses_env_override_for_dataset_path(self):
        expected = "/tmp/local-dataset.csv"

        with mock.patch.dict(
            os.environ, {"VISUALIZATION_DATA_FILE": expected}, clear=False
        ):
            self.assertEqual(visualization.get_dataset_path(), expected)


if __name__ == "__main__":
    unittest.main()
