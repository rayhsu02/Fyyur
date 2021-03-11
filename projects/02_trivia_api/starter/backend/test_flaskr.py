import os
import unittest
# import json
from flask import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'new question',
            'answer': 'Neil Gaiman',
            'difficulty': 1,
            'category': 1,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(len(data['categories']), 6)

    def test_404_get_paginated_categories_faild(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))

    # def test_404_get_paginated_questions_faild(self):
    #     res = self.client().get('/questions/1')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    def test_get_paginated_page1_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_4040_get_paginated_page_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=3000')
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 422)

    def test_delete_question_by_id(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_faild(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)

    def test_create_new_question_faild(self):
        res = self.client().post('/questions', json="")
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_question_with_result(self):
        res = self.client().post('/questions', json={'searchTerm': 'lifetime'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_search_question_with_no_result(self):
        res = self.client().post('/questions', json={'searchTerm': 'test'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_blank_search_term_question_with_no_result(self):
        res = self.client().post('/questions', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEquals(data['success'], True)
        self.assertGreater(data['total_questions'], 0)

    def test_422_questions_by_category_faild(self):
        res = self.client().get('/categories/12/questions')
        data = json.loads(res.data)

        self.assertEquals(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    def test_play_quiz(self):
        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': {
                        'id': 1,
                        'type': 'Science'},
                    'id': '0'},
                'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['question']), 0)

    def test_422_play_quiz_faild(self):
        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': {
                        'id': -1,
                        'type': 'Science'},
                    'id': '-1'},
                'previous_questions': []})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
