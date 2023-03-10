# Python
import unittest
import logging

# Project
from django.conf import settings
from .. import object_store

log = logging.getLogger(__name__)


@unittest.skipIf(
    settings.PANORAMA_OBJECTSTORE_PASSWORD == "insecure",
    "Panorama objectstore tests skipped: no password set in the environment",
)
class TestObjectStore(unittest.TestCase):
    """Panorama objectstore tests."""

    object_store = object_store.ObjectStore()

    def test_get_months(self):
        months = self.object_store.get_subdirs("2016", "")
        self.assertGreater(len(months), 4)
        self.assertEqual("03/", months[0])

    def test_get_subdirs(self):
        """Check day files."""
        days = self.object_store.get_subdirs("2016", "03/")
        self.assertGreater(len(days), 1)
        self.assertEqual("03/17/", days[0])

    def test_get_subdirs_trajectories(self):
        trajectories = self.object_store.get_subdirs("2016", "03/17/")
        self.assertGreater(len(trajectories), 0)
        self.assertEqual("03/17/TMX7315120208-000020/", trajectories[0])

    def test_get_pano_csvs(self):
        panorama_csvs = self.object_store.get_csv_type(
            "2016", "03/21/TMX7315120208-000021/", "panorama"
        )
        self.assertGreater(len(panorama_csvs), 0)
        self.assertEqual(
            "03/21/TMX7315120208-000021/panorama1.csv", panorama_csvs[0]["name"]
        )

    def test_get_trajectory_csvs(self):
        trajectory_csvs = self.object_store.get_csv_type(
            "2016", "03/17/TMX7315120208-000020/", "trajectory"
        )
        self.assertGreater(len(trajectory_csvs), 0)
        self.assertEqual(
            "03/17/TMX7315120208-000020/trajectory.csv", trajectory_csvs[0]["name"]
        )

    def test_get_csvs(self):
        """Check panorama1.csv files."""
        panorama_csvs = self.object_store.get_csvs("panorama")
        self.assertGreater(len(panorama_csvs), 2)
        self.assertEqual(
            "03/17/TMX7315120208-000020/panorama1.csv", panorama_csvs[0]["name"]
        )

    def test_get_panorama_store_object(self):
        panorama_csv = self.object_store.get_csv_type(
            "2016", "03/21/TMX7315120208-000021/", "panorama"
        )[0]
        csv = self.object_store.get_panorama_store_object(panorama_csv)
        self.assertIsNotNone(csv)

    def test_get_csv_to_read_runs(self):
        panorama_csv = self.object_store.get_csv_type(
            "2016", "03/21/TMX7315120208-000021/", "panorama"
        )[0]
        response = self.object_store.get_panorama_store_object(panorama_csv)
        import csv

        rows = csv.reader(
            iter(response.decode("utf-8").split("\n")),
            delimiter="\t",
            quotechar=None,
            quoting=csv.QUOTE_NONE,
        )
        headers = next(rows)
        log.info("header +  firstrow: %s" % str(dict(zip(headers, next(rows)))))

    def test_get_objects_pages(self):
        """Count 2016 files."""
        big_dir = "07/07/TMX7315120208-000104/"
        self.assertGreater(
            len(self.object_store.get_datapunt_store_objects("2016" + "/" + big_dir)),
            10000,
        )
        # self.object_store.RESP_LIMIT = 1000
        self.assertGreater(
            len(
                self.object_store.get_panorama_store_objects(
                    "2016", "03/21/TMX7315120208-000021"
                )
            ),
            2,
        )
