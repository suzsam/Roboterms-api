import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Company, Policy


class RoboTermsTestsCase(unittest.TestCase):
    """This class represents the test case for the RoboTerms app"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:a@localhost:5432/roboterms_test"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.db = SQLAlchemy()
        self.db.app = self.app
        self.db.init_app(self.app)

        if not os.getenv('CLIENT_TOKEN'):
            raise RuntimeError("Environment variables are not set, did you source setup.sh?")

        self.headers_client = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('CLIENT_TOKEN')
        }

        self.headers_admin = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('ADMIN_TOKEN')
        }

        # new Company for testing
        self.new_co = {
            "name": "Facesmash, LLC",
            "website": "geturfacesmashed.biz"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass


    # Unit Tests

    # At least two per endpoint

    # For the simple GET endpoints (/, /companies, /policies), test both as a public user 
    # (no 'Authorization' header), and as a member (with header).  
    # Header should not break the public access.
    def test_get_index_public(self):
        """Gets the / endpoint as public user and checks valid results"""
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual("This is my capstone project" in res.get_data(as_text=True), True)

    def test_get_index_member(self):
        """Gets the / endpoint as a member and checks valid results"""
        res = self.client().get('/', headers=self.headers_client)

        self.assertEqual(res.status_code, 200)
        self.assertEqual("This is my capstone project" in res.get_data(as_text=True), True)

    def test_get_all_companies_public(self):
        """Gets all companies as a public user and checks status and count."""
        res = self.client().get('/companies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['companies']), 3)

    def test_get_all_companies_member(self):
        """Gets all companies as a member and checks status and count."""
        res = self.client().get('/companies', headers=self.headers_client)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['companies']), 3)

    def test_get_all_policies_public(self):
        """Gets all policies as a public user and checks status and count."""
        res = self.client().get('/policies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['policies']), 4)

    def test_get_all_policies_member(self):
        """Gets all policies as a public user and checks status and count."""
        res = self.client().get('/policies', headers=self.headers_client)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['policies']), 4)

    def test_get_rendered_policy_valid(self):
        """Gets a valid rendered policy."""
        res = self.client().get('/rendered_policy/1/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual("TERMS OF SERVICE" in data['policy'], True)
        self.assertEqual("gcola.com" in data['policy'], True)

    def test_get_rendered_policy_invalid_company(self):
        """Attempts to get the rendered policy for an invalid company id."""
        res = self.client().get('/rendered_policy/1000/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_get_rendered_policy_invalid_policy(self):
        """Attempts to get the rendered policy for an invalid policy id."""
        res = self.client().get('/rendered_policy/1/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_new_company(self):
        """Attempts to create a new company as Client."""
        res = self.client().post('/company', headers=self.headers_client, json=self.new_co)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        # Delete the company we added directly through the DB session
        Company.query.get(data['id']).delete()

    def test_post_new_company_without_token(self):
        """Attempts to create a new company without a token."""
        res = self.client().post('/company', json=self.new_co)
        
        self.assertEqual(res.status_code, 401)  # Should return Unauthorized
        
    def test_post_existing_company(self):
        """Attempts to create a new company with same name as existing one."""
        existing_co = {
            "name": "Spy App Inc.",
            "website": "spyonyourlovedones--butlovingly.com"
        }
        res = self.client().post('/company', headers=self.headers_client, json=existing_co)
        
        self.assertEqual(res.status_code, 422)  # Unprocessable
    
    def test_post_company_missing_name(self):
        """Attempts to create a new company but missing a name."""
        new_co = {
            "website": "abcdefghijklmnopqrstuvwxyz.gov"
        }
        res = self.client().post('/company', headers=self.headers_client, json=new_co)
        
        self.assertEqual(res.status_code, 422)  # Unprocessable

    def test_post_company_as_admin(self):
        """Attempts to create a new company as Admin."""
        res = self.client().post('/company', headers=self.headers_admin, json=self.new_co)
        
        self.assertEqual(res.status_code, 403)  # Should return as Forbidden (invalid permissions)

    def test_delete_company(self):
        """Attempts to delete a company successfully as Client."""
        # Create a test company to delete
        new_co = Company(name="we're toast, LLC", website="dooooooooooommmmed.com")
        new_co.insert()
        new_co_id = new_co.id

        # Make sure it added successfully
        all_companies = Company.query.all()
        self.assertEqual(len(all_companies), 4)    # 3 originally in test DB

        # Delete it through route
        res = self.client().delete(f'/company/{new_co_id}', headers=self.headers_client)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], new_co_id)

    def test_delete_nonexistent_company(self):
        """Attempts to delete a company that doesn't exist."""
        res = self.client().delete(f'/company/1000', headers=self.headers_client)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Not Found
        self.assertEqual(data['success'], False)
        
    def test_delete_company_without_credentials(self):
        """Attempts to delete a company without any credentials."""
        res = self.client().delete(f'/company/1')
        data = json.loads(res.data)

        # AuthError throw different JSON format, no 'success' key
        self.assertEqual(res.status_code, 401)  # Unauthorized
        self.assertEqual(data['code'], "missing_auth_header")

    def test_delete_company_wrong_role(self):
        """Attempts to delete a company with a role that doesn't have correct permissions."""
        res = self.client().delete(f'/company/1', headers=self.headers_admin)
        data = json.loads(res.data)

        # AuthError throw different JSON format, no 'success' key
        self.assertEqual(res.status_code, 403)  # Forbidden
        self.assertEqual(data['code'], "forbidden")

    def test_update_policy(self):
        """Attempts to update a policy successfully as an Admin."""
        # Get current name of policy 1
        pol_1 = Policy.query.get(1)
        orig_name = pol_1.name

        # Change the policy name to FOOBAZ
        res = self.client().patch('/policy/1', headers=self.headers_admin, json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        # Check that it updated OK
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Fetch from the /policies endpoint to make sure the name changed
        res = self.client().get('/policies')
        data = json.loads(res.data)
        
        self.assertEqual(len(data['policies']), 4)  # Make sure length of /policies remains the same
        self.assertNotEqual(orig_name, data['policies'][0]['name'])

        # Now put the name back
        res = self.client().patch('/policy/1', headers=self.headers_admin, json={"name": "Terms of Service"})
        
        # And fetch new policies
        res = self.client().get('/policies')
        data = json.loads(res.data)

        # Check that it updated OK
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        for policy in data['policies']: # Can't count on ordering
            if policy['id'] == 1:
                updated_name = policy['name']
                break
        self.assertEqual(updated_name, "Terms of Service")

    def test_update_nonexistent_policy(self):
        """Attempts to update a policy that doesn't exist."""
        res = self.client().patch('/policy/1000', headers=self.headers_admin, json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Not Found
        self.assertEqual(data['success'], False)

    def test_update_policy_without_credentials(self):
        """Attempts to update a policy without credentials."""
        res = self.client().patch('/policy/1', json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)  # Unauthorized
        self.assertEqual(data['code'], "missing_auth_header")

    def test_update_policy_wrong_credentials(self):
        """Attempts to update a policy with incorrect credentials."""
        res = self.client().patch('/policy/1', headers=self.headers_client, json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)  # Forbidden
        self.assertEqual(data['code'], "forbidden")

    # Test error handlers
    def test_404(self):
        """Test 404 error handler is API'd"""
        res = self.client().get('/company/abcdefghijk')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['success'], False)

    def test_405(self):
        """Test 405 error handler is API'd"""
        # 405 means wrong method, here we use POST when should be GET
        res = self.client().post('/companies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertIn('error', data)
        self.assertEqual(data['success'], False)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()