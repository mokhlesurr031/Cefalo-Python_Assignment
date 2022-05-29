try:
    from application import app
    import unittest

except Exception as e:
    print("Something wrong in {}".format(e))


class FlaskTest(unittest.TestCase):

    # Check for movie list page response 200
    def test_root_url_status_code(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        print(status_code)
        self.assertEqual(status_code, 200)

    # Check for detail page response 200
    def test_detail_url_status_code(self):
        tester = app.test_client(self)
        response = tester.get("/45")
        status_code = response.status_code
        print(status_code)
        self.assertEqual(status_code, 200)

    # Check if root url content return in application/json
    def test_root_url_content_type(self):
        tester = app.test_client(self)
        response = tester.get("/")
        print(response.content_type)
        self.assertEqual(response.content_type, "application/json")

    # Check if detail url content return in application/json
    def test_detail_url_content_type(self):
        tester = app.test_client(self)
        response = tester.get("/22")
        print(response.content_type)
        self.assertEqual(response.content_type, "application/json")

    # # Check url data
    def test_root_url_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b"id" in response.data)
    #
    #
    #   # Check if movie_id exists in details url data
    def test_detail_url_data(self):
        tester = app.test_client(self)
        response = tester.get("/41")
        self.assertTrue(b"movie_id" in response.data)










if __name__=='__main__':
    unittest.main()