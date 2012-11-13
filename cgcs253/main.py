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
import cgi

form = """
    <form method="post">
    Enter some text to ROT13.
    <br>
    <textarea name="text" rows="10" cols="80">%(user_text)s</textarea>
    <br>
    <br>
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

class MainHandler(webapp2.RequestHandler):
    def write_form(self,text=""):
        self.response.write(form % {"user_text": text})
    
    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get('text')

        text = rot13(text)
        self.write_form(text=text)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
