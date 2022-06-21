import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# py manage.py test polls


#Models
class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns false for questions whose pub_date is in the future""" 
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Cúal ha sido el mejor jugador en Europa esta temporada?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_past_questions(self):
        """was_published_recently() must return False for questions whose pub_date is more than 1 day in the past"""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(question_text="¿Cúal ha sido el mejor jugador colombiano en Europa esta temporada?",pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_in_the_moment_with_present_questions(self):
        """was_published_recently() must return True for questions whose pub_date is actual"""
        time = timezone.now()
        present_question = Question(question_text="¿Cúal ha sido el mejor jugador colombiano en la liga local?",pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently() must return True for questions whose pub_date is less than a day"""
        time = timezone.now() - datetime.timedelta(days=1)
        present_question = Question(question_text="¿Cúal ha sido el mejor jugador en la Premier League?",pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

#vistas