#!/usr/bin/python3


# Copyright (c) 2024 Antonia <antonia@antonia.is>

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import json
import urllib.request
import time

token = sys.argv[1]

contents = urllib.request.urlopen("https://travelynx.de/api/v1/status/"+token).read()

response = json.loads(contents)
#print(response)

s = ""

if response["checkedIn"] :
    if "toStation" in response :
        s = response["toStation"]
        if "ds100" in s and s["ds100"] :
            name = s["ds100"]
        else :
            name = s["name"]
        arrtime = time.strftime("%H:%m", time.localtime(int(s["realTime"])))
        delay = (int(s["realTime"]) - int(s["scheduledTime"])) // 60
        s = f'{name} {arrtime}'
        if delay > 0 :
            s = s + " (+%d)" % delay
        
print(json.dumps({"text": s, "tooltip": "", "class": "active", "percentage": ""}))
