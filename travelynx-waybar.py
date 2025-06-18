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
import argparse

parser = argparse.ArgumentParser(description='Travelynx Integration for waybar')
parser.add_argument("token", help="travelynx status API token")
parser.add_argument("-l", "--last-checkin", metavar="MINUTES", help="keep showing last checkin for a given amount of minutes, 0 for indefinitely", type=int,)
parser.add_argument("-d", "--ds-100", action="store_true", help="Prefer DS100 codes for stations", default=False)
args = parser.parse_args()

token = args.token

contents = urllib.request.urlopen("https://travelynx.de/api/v1/status/"+token, timeout=60).read()

response = json.loads(contents)

st = ""

def humantime(t) :
    return time.strftime("%H:%M", time.localtime(int(t)))

def delay(s,i) :
    if s["real"+i] is not None :
        return (int(s["real"+i]) - int(s["scheduled"+i])) // 60
    else :
        return 0

def timestring(s,i):
    if not "real"+i in s or s["real"+i] is None :
        return humantime(s["scheduled"+i])
    dl = delay(s,i)
    ht = humantime(s["real"+i])
    if dl > 0 :
        return ht + " (+%d)" % dl
    if dl < 0 :
        return ht + " (%d)" % dl
    return ht

def get_destination(response) :
    if "toStation" in response :
        s = response["toStation"]
        if "ds100" in s and s["ds100"] and args.ds_100 :
            s["prefname"] = s["ds100"]
        else :
            s["prefname"] = s["name"]
        return s
    else:
        return None
tooltip = ""
checked_in = response["checkedIn"]
if checked_in or args.last_checkin is not None :    
    s = get_destination(response)
    elapsed = int(time.time()) - int(s["realTime"])
    if checked_in or args.last_checkin == 0 or args.last_checkin * 60 > elapsed :
        tstr = timestring(s,"Time")
        st = f'{s["prefname"]} {tstr}'
    if "train" in response :
        train = response["train"]
        if train["line"] is not None :
            tooltip = f'<b>{train["type"]} {train["line"]} ({train["no"]})</b> to {s["name"]}'
        else :
            tooltip = f'<b>{train["type"]} {train["no"]}</b> to {s["name"]}'
            
    if "intermediateStops" in response :
        stops = response["intermediateStops"]
        now = time.time()
        for stop in stops:
            if stop["scheduledDeparture"] is None and stop["scheduledArrival"] is None :
                continue
            if stop["realDeparture"] is not None and int(stop["realDeparture"]) > now :
                dep = timestring(stop, "Departure")
                arr = timestring(stop, "Arrival")
                tooltip = tooltip + f'\n{arr}–{dep} <b>{stop["name"]}</b>'
            elif stop["scheduledDeparture"] is not None and  int(stop["scheduledDeparture"]) > now :
                dep = humantime(stop["scheduledDeparture"])
                arr = humantime(stop["scheduledArrival"])
                tooltip = tooltip + f'\n<i>{arr}–{dep}</i>  <b>{stop["name"]}</b>'
            elif stop["scheduledDeparture"] is None and  int(stop["scheduledArrival"]) > now :
                arr = humantime(stop["scheduledArrival"])
                tooltip = tooltip + f'\n<i>arrival {arr}</i>  <b>{stop["name"]}</b>'                

        
print(json.dumps({"text": st, "tooltip": tooltip, "class": "active", "percentage": ""}))
