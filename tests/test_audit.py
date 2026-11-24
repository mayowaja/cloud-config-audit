import unittest
from audit import evaluate


class AuditTests(unittest.TestCase):
    def test_complete_snapshot(self):
        row = dict(id="a", public_read=True, encrypted=True, access_logging=False)
        self.assertEqual([c["status"] for c in evaluate([row])], ["fail", "pass", "fail"])

    def test_missing_and_null_are_unknown(self):
        self.assertEqual([c["status"] for c in evaluate([{"id": "a", "encrypted": None}])],
                         ["unknown"] * 3)

    def test_invalid_input(self):
        for data in ([], {}, [{"id": " "}], [{"id": "a"}, {"id": "a"}],
                     [{"id": "a", "encrypted": 1}]):
            with self.subTest(data=data), self.assertRaises(ValueError):
                evaluate(data)
