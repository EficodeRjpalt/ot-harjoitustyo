import unittest
from entities.comment import Comment


class TestComment(unittest.TestCase):

    def setUp(self):

        self.test_comment = Comment(
            '25/11/2022 13:37',
            'rjpalt@gmail.com',
            'This issue is total nonsense!'
        )

    def test_timestamp_getter(self):

        self.assertEqual(
            '25/11/2022 13:37',
            self.test_comment.timestamp
        )

    def test_actor_getter(self):

        self.assertEqual(
            'rjpalt@gmail.com',
            self.test_comment.actor
        )

    def test_body_getter(self):

        self.assertEqual(
            'This issue is total nonsense!',
            self.test_comment.body
        )

    def test_str(self):

        self.assertEqual(
            '25/11/2022 13:37; rjpalt@gmail.com; This issue is total nonsense!',
            str(self.test_comment)
        )

    def test_repr(self):

        self.assertEqual(
            '25/11/2022 13:37; rjpalt@gmail.com; This issue is total nonsense!',
            repr(self.test_comment)
        )

    def test_timestamp_setter(self):

        self.test_comment.timestamp = '01-07-1975 21:56:07'

        self. assertEqual(
            self.test_comment.timestamp,
            '01-07-1975 21:56:07'
        )

    def test_actor_setter(self):

        self.test_comment.actor = 'Pormestari Kontiainen'

        self. assertEqual(
            self.test_comment.actor,
            'Pormestari Kontiainen'
        )

    def test_body_setter(self):

        self.test_comment.body = 'This is a value given by a setter!'

        self. assertEqual(
            self.test_comment.body,
            'This is a value given by a setter!'
        )
