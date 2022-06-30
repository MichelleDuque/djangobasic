import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question



# py manage.py test polls


#Models
class QuestionModelTests(TestCase):

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
        present_question_published = Question(question_text="¿Cúal ha sido el mejor jugador en la Premier League?",pub_date=time)
        self.assertIs(present_question_published.was_published_recently(), True)

#vistas

def create_question(question_text, days):
    """
    Create a question with the given "question_text", and publish the given number of days offset to now
    (negative for question published in the past, positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """ If no question exits, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are avariable.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_questions_in_the_future(self):
        """Question created in the future has not been included in latest_question_list"""
        create_question("¿Future Question?", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No Polls are avariable.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_questions_in_the_past(self):
        """Question created in the future has been included in latest_question_list"""
        question = create_question("¿Past Question?", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed.
        """
        past_question = create_question("Past question?", days=-30)
        future_question = create_question("Future question?", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_question1 = create_question("Past question 1?", days=-30)
        past_question2 = create_question("Past question 2?", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])

    def test_two_future_questions(self):
        """
        The questions index do not display questions.
        """
        future_question1 = create_question("Future question 1?", days=30)
        future_question2 = create_question("Future question 2?", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    