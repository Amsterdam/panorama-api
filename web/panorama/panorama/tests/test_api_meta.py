from rest_framework.test import APIClient

# Project
from .test_api_base import PanoramaApiTest


class ApiMetasTest(PanoramaApiTest):
    def test_get_status_health(self):
        """
        Tests Health status
        """
        response = self.client.get("/status/health")
        self.assertEqual(response.status_code, 200)

    def test_cors(self):
        """
        Cross Origin Requests should be allowed.
        """
        response = APIClient().get("https://api.data.amsterdam.nl/panorama/panoramas/?lat=52.3779561&lon=4.8970701",
            HTTP_REFERER = "https://foo.google.com",
            HTTP_HOST = "api.data.amsterdam.nl",
            HTTP_ORIGIN = "https://foo.google.com"
        )

        self.assertTrue("Access-Control-Allow-Origin" in response.headers)
        self.assertEquals("*", response.headers["Access-Control-Allow-Origin"])
