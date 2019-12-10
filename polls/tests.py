import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse
# Create your tests here.


class QuestionModelTest(TestCase):
    def test_was_published_rencently_with_future_question(self):
        time = timezone.now()+datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        """
        将问卷的发布日期是未来的某一天时，was_published_recently()方法将返回False
        """
        self.assertIs(future_question.was_publiced_recently(), False)

    def test_was_published_rencently_with_old_question(self):
        """
        当问卷的发布日期比前一天还早一秒钟时，was_published_recently()返回False
        """
        time = timezone.now()-datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_publiced_recently(), False)

    def test_was_published_rencently_with_recent_question(self):
        """
        当问卷的发布日期比前一天还晚一秒钟时，was_published_recently()返回False
        """
        time = timezone.now()-datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_publiced_recently(), True)


def create_question(question_text, days):
    """
    使用指定的文本和日期数量创建问卷
    如果日期数量是负数表示发布日期早于当前时间，如果日期为正数则表示发布日期晚于当前时间
    """
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        如果当前系统没有符合条件的问卷则返回提示信息
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, u"还没有调查问卷!")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        早于当前时间发表的问卷将会被显示在index页面中
        """
        create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: Past Question>'])

    def test_feature_question(self):
        """
        晚于当前时间发表的问卷将不会显示在index页面
        """
        create_question(question_text="Feature Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, u"还没有调查问卷!")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_feature_question_and_past_question(self):
        """
        晚于当前时间发表的问卷将不会显示在index页面
        """
        create_question(question_text="Past Question", days=-30)
        create_question(question_text="Feature Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: Past Question>'])

    def test_two_past_question(self):
        """
        显示多个问卷
        """
        create_question(question_text="Past Question1", days=-30)
        create_question(question_text="Past Question2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: Past Question2>', '<Question: Past Question1>'])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        如果被查询的问卷还没有发表则返回404错误
        """
        future_question=create_question(question_text="Future Question",days= 5)
        url=reverse("polls:detail",args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    def test_past_question(self):
        """
        如果被查询的问卷已经发表了则返回问卷内容
        """
        past_question =create_question(question_text="Past Question",days=-5)
        url=reverse("polls:detail",args=(past_question.id,))
        response=self.client.get(url)
        self.assertContains(response,past_question.question_text)

