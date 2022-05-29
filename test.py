import random

try:
    from application import app
    import unittest

except Exception as e:
    print("Something wrong in {}".format(e))


class FlaskServerUnitTest(unittest.TestCase):
    # Check for movie list page response 200
    def test_root_url_status_code(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # Check for detail page response 200
    def test_detail_url_status_code(self):
        tester = app.test_client(self)
        response = tester.get("/45")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # Check if root url content return in application/json
    def test_root_url_content_type(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "application/json")

    # Check if detail url content return in application/json
    def test_detail_url_content_type(self):
        tester = app.test_client(self)
        response = tester.get("/22")
        self.assertEqual(response.content_type, "application/json")

    # Check url data
    def test_root_url_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b"id" in response.data)

    # Check if movie_id exists in details url data
    def test_detail_url_data(self):
        tester = app.test_client(self)
        response = tester.get("/41")
        self.assertTrue(b"movie_id" in response.data)

    # Check if movie name same by same id in list and detail list
    def test_check_if_same_movie_in_list_and_details_by_id(self):
        random_id = random.randint(1,1000)
        tester = app.test_client(self)
        response = tester.get("/")
        res = eval(response.text)['Movies List']
        for data in res:
            if data['id'] == random_id:
                movie_name = data['name']

        tester2 = app.test_client(self)
        response2 = tester.get("/{}".format(random_id))
        res = eval(response2.text)
        for detail in eval(res['Details']):
            try:
                name = detail['name']
            except:
                pass
        self.assertEqual(movie_name, name)


if __name__=='__main__':
    unittest.main()