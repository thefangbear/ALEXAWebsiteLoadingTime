import json
from sys import argv
from scipy import stats
import numpy 
import math

class Website(object):
  url=None
  rank=None
  has_http=False
  has_https=False
  t_http=[]
  t_https=[]
  def __init__(self, url, rank):
    self.url = url
    self.rank = rank
    self.t_http = []
    self.t_https = []


  def __str__(self):
    _s = "Website(" + self.url + "," +  self.rank + "):"
    if self.has_http: 
      _s += "http:"
      _s += str(len(self.t_http))
    if self.has_https:
      _s += ",https:"
      _s += str(len(self.t_https))
    return _s

def get_time(l):
  try: 
    j = json.loads(l)
    t = j['result']['value']
    print(j) 
    print(t)
    return (True, t)
  except:
    print("get_time: here")
    return (False, -1.0)

def parse_lines(ls):
  d1={}
  for line in ls:
    print("---------")
    try:
      trials = line.split("|")  
      print(trials)
      chunks_http = []
      chunks_https = []
      chunks_http = trials[0].split(">>>")
      chunks_https = trials[1].split(">>>")
      website = chunks_http[0].split(' ')[1]
      rank = chunks_http[0].split(' ')[0]
      jsonstr_http = ""
      jsonstr_https = ""
      if len(chunks_http) >= 2:
        jsonstr_http = chunks_http[1]
      if len(chunks_https) >= 2:
        jsonstr_https = chunks_https[1]
      try:
        print("website data:", d1[website])
        has_http, t_http = get_time(jsonstr_http)
        has_https, t_https = get_time(jsonstr_https)
        if has_http:
          d1[website].has_http = True
          d1[website].t_http.append(t_http)
        if has_https:
          d1[website].has_https = True
          d1[website].t_https.append(t_https)
      except KeyError:
        print("adding ", website, "to dict")
        d1[website] = Website(website, rank)
#        print("here after ")
        has_http, t_http = get_time(jsonstr_http)
        has_https, t_https = get_time(jsonstr_https)
#        print("here: ", has_http, has_https, t_http, t_https)
        if has_http:
          d1[website].has_http = True
          d1[website].t_http.append(t_http)
        if has_https:
          d1[website].has_https = True
          d1[website].t_https.append(t_https)
    except:
      print("!!! Woops: ", line)
  return d1

def print_dict(d):
  for k, v in d:
    print("website: ", k)
    print(d)

top_file = argv[1]
btm_file = argv[2]
top_dict = {}

with open(top_file) as fd:
  top_all = fd.readlines()
with open(btm_file) as fd:
  btm_all = fd.readlines()

top_dict = parse_lines(top_all)
btm_dict = parse_lines(btm_all)

print("---")

top_vect = []
btm_vect  = []
top_avg = 0.0
btm_avg = 0.0
top_stdev= 0.0
btm_stdev = 0.0

def print_data(d, v):
  cnt=1
  for key, value in d.items():
    avg_http = 0
    avg_https = 0
    avg_t=0
    if value.has_http:
      avg_http = sum(value.t_http) / len(value.t_http)
    if value.has_https:
      avg_https = sum(value.t_https) / len(value.t_https)
    t = min(avg_http, avg_https)
    if t <= 0:
      t = max(avg_http, avg_https)
    if t <= 0:
      continue
    print(cnt, " ", t)
    v.append(t)
    cnt+=1

print_data(top_dict, top_vect)
print("...................")
print_data(btm_dict, btm_vect)
print("...................")
for x in range(0, 138):
  s = str(x) + " "
  if x < len(btm_vect):
    s += str(btm_vect[x])
    s += " "
  if x < len(top_vect):
    s += str(top_vect[x])
    s += " "
  print(s)
#print(top_vect)
#print(btm_vect)
top_avg = sum(top_vect) / len(top_vect)
btm_avg = sum(btm_vect) / len(btm_vect)
top_stdev = numpy.std(top_vect)
btm_stdev = numpy.std(btm_vect)
t = (top_avg - btm_avg) / math.sqrt(top_stdev*top_stdev / len(top_vect) + btm_stdev*btm_stdev / len(btm_vect))
half_p = stats.t.cdf(t, df=min(len(top_vect), len(btm_vect))-1)
print("top_avg=", top_avg, ",btm_avg=", btm_avg, ",top_stdev=",top_stdev,",btm_stdev=",btm_stdev,",t=",t,",p=",1-half_p)
