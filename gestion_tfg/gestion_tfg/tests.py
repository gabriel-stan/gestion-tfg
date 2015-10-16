
from django.test import TestCase

class QuestionMethodTests(TestCase):
	def dummy_test(self):
		this_is_true = True
		self.assertEqual(this_is_true, True)
