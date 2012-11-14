#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

main_page = """
    Problem Set 2:<br>
    <ul>
    <li><a href="/rot13">ROT13 assignment</a></li>
    <li><a href="/signup">Signup Form</a></li>
    </ul>
    """

rot13_page = """
    <form method="post">
    Enter some text to ROT13.
    <br>
    <textarea name="text" rows="10" cols="80">%(user_text)s</textarea>
    <br>
    <br>
    <input type="submit">
    </form>
    """

signup_page = """
    <h2>Signup!</h2><br>
    <form method="post">
    <label>Username: 
        <input type="text" name="username" value="%(username)s">
    </label> <div style="color: red">%(user_error)s </div><br>
    <label>Password: 
        <input type="password" name="password">
    </label> <div style="color: red">%(pw_error)s </div><br>
    <label>Verify Password: 
        <input type="password" name="verify">
    </label> <div style="color:red">%(verify_error)s </div><br>
    <label>E-mail (optional):
        <input type="text" name="email" value="%(email)s">
    </label> <div style="color: red">%(email_error)s </div><br>
    <input type="submit">
    </form>
    """

from_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
to_characters = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
trans_table = dict(zip(from_characters,to_characters))

def rot13(s):
    s2 = ''
    
    for letter in s:
        if letter in from_characters:
            s2 += trans_table[letter]
        else:
            s2 += letter

    return escape_html(s2)


def escape_html(s):
    return cgi.escape(s,quote=True)

user_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")
pass_re = re.compile("^.{3,20}$")
email_re = re.compile("^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return user_re.match(username)

def valid_password(password):
    return pass_re.match(password)

def valid_email(email):
    return email_re.match(email)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(main_page)
        

class Rot13Handler(webapp2.RequestHandler):
    def write_form(self,text=""):
        self.response.write(rot13_page % {"user_text": text})
    
    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get('text')

        text = rot13(text)
        self.write_form(text=text)


class SignupHandler(webapp2.RequestHandler):
    def write_form(self,
                   username="",
                   email="",
                   user_error="",
                   pw_error="",
                   verify_error="",
                   email_error=""):
    
        self.response.write(signup_page % {"username": escape_html(username),
                                        "email": escape_html(email),
                                        "user_error": user_error,
                                        "pw_error": pw_error,
                                        "verify_error": verify_error,
                                        "email_error": email_error   })
    
    
    def get(self):
        self.write_form()
    

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")
        
        if ( valid_username(user_username)
             and valid_password(user_password)
             and user_password == user_verify
             and ( valid_email(user_email) if len(user_email) else True ) ):

            self.redirect('/welcome?username=%s' % user_username)
    
        else:
            user_error = "That's not a valid username." if not valid_username(user_username) else ""
            
            pw_error = "That's not a valid password." if not valid_password(user_password) else ""
            
            verify_error = "Your passwords didn't match." if not (user_password == user_verify) else ""

            
            email_error = "That's not a valid email." if ( len(user_email) and not valid_email(user_email) ) else ""

            self.write_form(user_username,
                            user_email,
                            user_error,
                            pw_error,
                            verify_error,
                            email_error)



class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write('<h2>Welcome, %s!</h2>' % escape_html(username))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/rot13', Rot13Handler),
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
