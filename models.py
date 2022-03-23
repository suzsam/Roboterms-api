import os
# from sqlalchemy import Column, String, Integer, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy

# Ensure that setup.sh has been sourced. Fail if variables not set
if not os.getenv('DATABASE_URL'):
    raise RuntimeError("Environment variables are not set, did you source setup.sh?")

database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
    binds a flask application and a SQLAlchemy service
    '''
    # print(f"Using database_path={database_path}")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    # Turn this off after initial run or will keep overwriting database!
    if 0:
        db.drop_all()
        db.create_all()
        pop_policies()          # See below for initial policy population
    if 0:
        pop_mock_companies()    # See below.  Used only during development.


class Company(db.Model):
    __tablename__ = 'Company'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80), unique=True, nullable=False)
    website = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Company object with name: {self.name} and site: {self.website}"

    '''
    insert() method
    Creates a new company
    EXAMPLE
        new_co = Company(name="Green Cola, Inc.", website="gcola.com")
        new_co.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update() method
    Updates a row already in the database
    EXAMPLE
        co = Company.query.filter(name="Green Cola, Inc.")
        co.website = "gcola.biz.info.site"
        co.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete() method
    Deletes a row from the database
    EXAMPLE
        co = Company.query.get(co_id)
        co.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
class Policy(db.Model):
    __tablename__ = 'Policy'

    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80), unique=True, nullable=False)
    body =  db.Column(db.String(3000), nullable=False)

    def __repr__(self):
        return f"Policy object with name: {self.name} and begins: {self.data[0:10]}"

    '''
    insert() method
    Creates a new policy
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update() method
    Updates a row already in the database
    '''
    def update(self):
        db.session.commit()

    '''
    delete() method
    Deletes a row from the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()


def pop_policies():
    # Add the policy boilerplate
    # 1. Terms of Service
    # 2. Cookie policy
    # 3. Disclaimer
    # 4. Privacy policy

    # Use placeholders {WEBSITE} and {COMPANY} which will fill in later

    # NOTE: These policies are extremely abbreviated and just for a homework assignment.
    # DO NOT USE THEM FOR ANY COMMERCIAL PRODUCTS!  Also, I am not a lawyer.

    tos = Policy(name="Terms of Service", body='''
        TERMS OF SERVICE

        These Terms of Service ("Terms") govern your access to and use of the website "{WEBSITE}" and all its services.  Your access to and use of the Services are conditioned on your acceptance of and compliance with these Terms. By accessing or using the Services you agree to be bound by these Terms.

        All Content, whether publicly posted or privately transmitted, is the sole responsibility of the person who originated such Content. You retain your rights to any Content you submit, post or display on or through the Services.

        You are responsible for your use of the Services, for any Content you post to the Services, and for any consequences thereof.  {COMPANY} respects the intellectual property rights of others and expects users of the Services to do the same.

        Your access to and use of the Services or any Content are at your own risk. You understand and agree that the Services are provided to you on an "AS IS" and "AS AVAILABLE" basis.

        TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE ENTITIES SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS OR REVENUES, WHETHER INCURRED DIRECTLY OR INDIRECTLY, OR ANY LOSS OF DATA, USE, GOOD-WILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM (i) YOUR ACCESS TO OR USE OF OR INABILITY TO ACCESS OR USE THE SERVICES; (ii) ANY CONDUCT OR CONTENT OF ANY THIRD PARTY ON THE SERVICES, INCLUDING WITHOUT LIMITATION, ANY DEFAMATORY, OFFENSIVE OR ILLEGAL CONDUCT OF OTHER USERS OR THIRD PARTIES; (iii) ANY CONTENT OBTAINED FROM THE SERVICES; OR (iv) UNAUTHORIZED ACCESS, USE OR ALTERATION OF YOUR TRANSMISSIONS OR CONTENT.
        '''        
    )
    tos.insert()

    cookies = Policy(name="Cookies Policy", body='''
        COOKIES POLICY

        {COMPANY} ("us", "we", or "our") uses cookies on "{WEBSITE}" (the "Service"). By using the Service, you consent to the use of cookies.

        Our Cookies Policy explains what cookies are, how we use cookies, how third-parties we may partner with may use cookies on the Service, your choices regarding cookies and further information about cookies.

        What are cookies

        Cookies are small pieces of text sent by your web browser by a website you visit. A cookie file is stored in your web browser and allows the Service or a third-party to recognize you and make your next visit easier and the Service more useful to you.

        Cookies can be "persistent" or "session" cookies.

        How {COMPANY} uses cookies

        When you use and access the Service, we may place a number of cookies files in your web browser.

        We use cookies for the following purposes: to enable certain functions of the Service, to provide analytics, to store your preferences, to enable advertisements delivery, including behavioral advertising.

        If you'd like to delete cookies or instruct your web browser to delete or refuse cookies, please visit the help pages of your web browser.

        Please note, however, that if you delete cookies or refuse to accept them, you might not be able to use all of the features we offer, you may not be able to store your preferences, and some of our pages might not display properly.
        '''
    )
    cookies.insert()

    disclaimer = Policy(name="Disclaimer", body='''
        DISCLAIMER

        This website {WEBSITE} owned and operated by {COMPANY} makes no representations as to accuracy, completeness, correctness, suitability, or validity of any information on this site and will not be liable for any errors, omissions, or delays in this information or any losses injuries, or damages arising from its display or use. All information is provided on an as-is basis.

        The views and opinions expressed herein are those of the authors and do not necessarily reflect the official policy or position of any other agency, organization, employer or company.
        '''        
    )
    disclaimer.insert()

    privacy = Policy(name="Privacy Policy", body='''
        PRIVACY POLICY

        This statement ("Privacy Policy") covers the website {WEBSITE} owned and operated by {COMPANY} ("we", "us", "our") and all associated services.

        We use information you share with us for our internal business purposes. We do not sell your information. This notice tells you what information we collect, how we use it, and steps we take to protect and secure it.

        Information we automatically collect
        Non-personally-identifying

        Like most website operators, we collect non-personally-identifying information such as browser type, language preference, referring site, and the date and time of each visitor request.  We collect this to understand how our visitors use our service, and use it to make decisions about how to change and adapt the service.

        From time to time, we may release non-personally-identifying information in aggregate form (for instance, by publishing trends in site usage) to explain our reasoning in making decisions. We will not release individual information, only aggregate information.

        Personally-identifying

        We automatically collect personally-identifying information, such as IP address, provided by your browser and your computer.

        You can change or delete any optional information that you've provided us at any time. If you change or delete any optional information you've provided, the change will take place immediately.

        You can also choose to delete your account entirely. If you choose to delete your account entirely, we will retain any personally-identifying information for a limited amount of time before removing it entirely. This is to allow you to undelete your account and continue using the service if you so choose. After this time, all your personally-identifying information will be removed entirely from our service, with the exception of any records we must retain to document compliance with regulatory requirements.
        '''        
    )
    privacy.insert()


def pop_mock_companies():
    # Add new companies
    new_co = Company(name="Green Cola, Inc.", website="gcola.com")
    new_co.insert()

    new_co = Company(name="Googolplex AtoZ Data", \
        website="stopdoingevilwheneverconvenient.com")
    new_co.insert()

    new_co = Company(name="Spy App Inc.", website="spyonyourlovedones--butlovingly.com")
    new_co.insert()