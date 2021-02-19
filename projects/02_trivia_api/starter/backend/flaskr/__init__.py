import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.sql.expression import join, true

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_items(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [ question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
 
  
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route("/")
  def hello():
    return "hello"
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_all_categories():
   
    categories = Category.query.order_by(Category.id).all()
    current_categories = paginate_items(request, categories)
    cirrent_size = len(current_categories) if current_categories else 0
    print(current_categories)
    return jsonify({
      'success': True,
      'categories': current_categories,
      'total': cirrent_size
    })


  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # '''
  @app.route('/questions')
  def get_questions():
    join_result = db.session.query(Question.category.distinct(), Category).filter(Question.category == Category.id).all()
    categories = [category.type  for categoryid, category in join_result]
    question_query = Question.query.join(Category, Question.category == Category.id).order_by(Question.id)
    questions = question_query.all()
    current_questions = paginate_items(request, questions)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      "categories" : categories,
      'current_category': ""
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def createQuestion():
    body = request.get_json()
    print(body)
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    search = body.get('searchTerm', None)
    print(search)

    if search:
      
      questions = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
      current_questions = paginate_items(request, questions)
      return jsonify({
        'success': True,
        'questions':current_questions
      })
    elif search == '':
      
      if search == '':
        print('empty')
        return jsonify({
        'success': True,
        'questions':[]
      })
    elif question and answer and difficulty and category:
      print('create')
      new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      Question.insert(new_question)

      return jsonify({
          'success': True,
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  

    


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_category(id):
    
    questions = Question.query.filter(Question.category == id).all()
    current_questions = paginate_items(request, questions)

    print(id)
    return jsonify({
      'success':True,
      'questions': current_questions,
    })



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    