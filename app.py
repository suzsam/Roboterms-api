import os
from flask import (
  Flask,
  request,
  abort,
  jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_migrate import Migrate

# Stuff to render my README.md on the home page
import markdown
import markdown.extensions.fenced_code  # Supports GitHub's backtick (```code```) blocks
import markdown.extensions.codehilite   # Code highlighting: Python, JSON
import markdown.extensions.tables       # Format tables better in HTML
import markdown.extensions.sane_lists   # Make bulleted list formatting in HTML better
from pygments.formatters import HtmlFormatter

# My modules
from models import setup_db, Company, Policy
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)   # Allow all origins

    # Set up the database first
    setup_db(app)

    @app.route('/', methods=['GET'])
    def index():
        # https://dev.to/mrprofessor/rendering-markdown-from-flask-1l41
        with open("README.md", "r") as readme:
            md_template_string = markdown.markdown(
                readme.read(), extensions=["fenced_code", "codehilite", "tables", "sane_lists"]
            )

        # Generate css for syntax highlighting
        formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
        css_string = formatter.get_style_defs()

        # Builds embedded CSS styling without a static file
        md_css_string = "<style>" + css_string + "</style>"

        md_template = md_css_string + md_template_string
        return md_template


    @app.route('/companies', methods=['GET'])
    def get_companies():
        company_list = []
        companies = Company.query.all()
        for co in companies:
            company_list.append({
                "id": co.id,
                "name": co.name,
                "website": co.website
            })

        # Build overall response
        data = {
            "companies": company_list,
            "success": True
        }
        return jsonify(data)

    
    @app.route('/policies', methods=['GET'])
    def get_policies():
        pol_list = []
        policies = Policy.query.all()
        for pol in policies:
            pol_list.append({
                "id": pol.id,
                "name": pol.name,
                "body": pol.body
            })
        
        data = {
            "policies": pol_list,
            "success": True
        }
        return jsonify(data)
    

    @app.route('/rendered_policy/<int:company_id>/<int:policy_id>', methods=['GET'])
    def get_rendered_policy(company_id, policy_id):
        company = Company.query.get(company_id)
        if not company:
            abort(404)
            
        policy = Policy.query.get(policy_id)
        if not policy:
            abort(404)
            
        # Fill in the placeholders {COMPANY} and {WEBSITE} with real data
        rendered_policy = policy.body.format(COMPANY=company.name, WEBSITE=company.website)

        data = {
            "policy": rendered_policy,
            "success": True
        }
        return jsonify(data)

    
    @app.route('/company', methods=['POST'])
    @requires_auth(permission='post:company')
    def add_company(payload):
        body = request.json

        # Need to have name and website keys in body
        if not all([ x in body for x in ['name', 'website'] ]):
            abort(422)

        # Here we want this to return None otherwise another company has that name
        # If you don't handle this way, function works, but unittests catches the 
        # print statement below in the 'except Exception as e' block and clutters
        # up the unittests output.
        duplicate_name = Company.query.filter_by(name=body['name'].strip()).one_or_none()
        if duplicate_name:
            abort(422)
        duplicate_website = Company.query.filter_by(website=body['website'].strip()).one_or_none()
        if duplicate_website:
            abort(422)

        try:
            new_co = Company(name=body['name'].strip(), website=body['website'].strip())
            new_co.insert()
        except Exception as e:
            print(f'Exception in add_company(): {e}')
            abort(422)  # Syntax is good, can't process for semantic reasons

        return jsonify({
            "id": new_co.id,
            "success": True
        })

    
    @app.route('/company/<int:company_id>', methods=['DELETE'])
    @requires_auth(permission='delete:company')
    def delete_company(payload, company_id):
        # Get the company to delete
        goner_co = Company.query.get(company_id)
        if not goner_co:
            abort(404)
        
        id = goner_co.id    # Will lose this after delete

        try:
            goner_co.delete()
        except Exception as e:
            print(f'Exception in delete_company(): {e}')
            abort(422)

        return jsonify({
            "id": id,
            "success": True
        })
        
    
    @app.route('/policy/<int:policy_id>', methods=['PATCH'])
    @requires_auth(permission='edit:policy')
    def edit_policy(payload, policy_id):
        # Get the policy to edit
        policy = Policy.query.get(policy_id)
        if not policy:
            abort(404)
        
        body = request.json

        # Check for name and body keys in the request payload
        # Here it's allowable to only update one, or both, entries
        if not any([ x in body for x in ['name', 'body'] ]):
            abort(422)

        if 'name' in body:
            policy.name = body['name']
        if 'body' in body:
            policy.body = body['body']  # whoah
        
        try:
            policy.update()
        except Exception as e:
            print(f'Exception in edit_policy(): {e}')
            abort(422)
        
        return jsonify({
            "success": True
        })

    
    ## Error Handling.  Returns tuple of JSON data and integer status code

    '''
        error handler should conform to general task above 
    '''
    @app.errorhandler(AuthError)
    def auth_error(excpt):
        # This decorator is called when an exception is thrown of AuthError type
        # (unlike standard aborts which accept integer status error codes)
        # This is for authentication errors only (our decorator)
        response = jsonify(excpt.error)
        response.status_code = excpt.status_code
        return response


    @app.errorhandler(400)
    def bad_request(error):
        '''Server cannot process request due to client error, such as malformed request'''
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        '''Authentication has not yet been provided'''
        return jsonify({
            "success": False, 
            "error": 401,
            "message": "unauthorized"
            }), 401

    @app.errorhandler(403)
    def forbidden(error):
        '''Server is refusing action, often because user does not have permissions for request'''
        return jsonify({
            "success": False, 
            "error": 403,
            "message": "forbidden"
            }), 403

    @app.errorhandler(404)
    def not_found(error):
        '''Requested resource could not be found on the server'''
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "not found"
            }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        '''Request method (i.e. GET or POST) is not allowed for this resource'''
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        '''The request was well-formed but unable to be followed due to semantic errors'''
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(500)
    def server_error(error):
        '''Catch-all for server error on our end'''
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "internal server error"
            }), 500


    return app

app = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=8080, debug=True)
    app.run()