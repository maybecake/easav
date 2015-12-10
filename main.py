#!/usr/bin/env python

import os, urllib, json, cgi, random, jinja2, webapp2, datetime
# from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENV = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions = ['jinja2.ext.autoescape'],
  autoescape = True)
  
ALL_ROLES = [
  'Merlin',
  'Assassin',
  'Percival',
  'Morgana',
  'G1',               # 5 player game,  3 good, 2 bad
  'G2',               # 6 player game,  4 good, 2 bad
  'Mordred',          # 7 player game,  4 good, 3 bad
  'G3',               # 8 player game,  5 good, 3 bad
  'G4',               # 9 player game,  6 good, 3 bad
  'Oberon',           # 10 player game, 6 good, 4 bad
  'B1',
  'B2',
  'B3',
  'B4',
  'G5',
  'G6',
  ]
  
ROLE_INFO = {
  'Merlin':   {
    'align': 'good',
    'name': 'Merlin',
    'desc': 'Knows evil except Mordred',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Morgana', 'Oberon', 'B1', 'B2', 'B3', 'B4']
  },
  'Assassin': {
    'align': 'evil',
    'name': 'Assassin',
    'desc': 'Tries to kill Merlin if 3 missions pass. Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Morgana', 'Mordred', 'B1', 'B2', 'B3', 'B4']
  },
  'Morgana':  {
    'align': 'evil',
    'name': 'Morgana',
    'desc': 'Appears as Merlin to Percival. Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Mordred', 'B1', 'B2', 'B3', 'B4']
  },
  'Mordred':  {
    'align': 'evil',
    'name': 'Mordred',
    'desc': 'Unknown to Merlin. Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Morgana', 'B1', 'B2', 'B3', 'B4']},
  'Percival': {
    'align': 'good',
    'name': 'Percival',
    'desc': 'Knows Merlin (or Morgana)',
    'seetext': 'Knows is Merlin (or Morgana)',
    'sees': ['Merlin', 'Morgana']},
  'Oberon': {
    'align': 'evil',
    'name': 'Oberon',
    'desc': 'Knows nothing.',
    'sees': []},
  'B1': {
    'align': 'evil',
    'name': 'Minion of Mordred',
    'desc': 'Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Morgana', 'Mordred', 'B2', 'B3', 'B4']},
  'B2': {
    'align': 'evil', 
    'name': 'Minion of Mordred',
    'desc': 'Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Morgana', 'Mordred', 'B1', 'B3', 'B4']},
  'B3': {
    'align': 'evil', 
    'name': 'Minion of Mordred',
    'desc': 'Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Morgana', 'Mordred', 'B1', 'B2', 'B4']},
  'B4': {
    'align': 'evil', 
    'name': 'Minion of Mordred',
    'desc': 'Knows other evil except Oberon.',
    'seetext': 'Knows are evil',
    'sees': ['Assassin', 'Morgana', 'Mordred', 'B1', 'B2', 'B3']},
  'G1': {
    'align': 'good',
    'name': 'Servent of Arthur',
    'desc': 'Knows nothing.',
    'seetext': 'Knows nothing',
    'sees': []},
  'G2': {
    'align': 'good',
    'name': 'Servent of Arthur',
    'desc': 'Knows nothing.',
    'seetext': 'Knows nothing',
    'sees': []},
  'G3': {
    'align': 'good',
    'name': 'Servent of Arthur',
    'desc': 'Knows nothing.',
    'seetext': 'Knows nothing',
    'sees': []},
  'G4': {
    'align': 'good',
    'name': 'Servent of Arthur',
    'desc': 'Knows nothing.',
    'seetext': 'Knows nothing',
    'sees': []},
  'G5': {
    'align': 'good',
    'name': 'Servent of Arthur',
    'desc': 'Knows nothing.',
    'seetext': 'Knows nothing',
    'sees': []},
  'G6': {
    'align': 'good',
    'name': 'Servent of Arthur',
    'desc': 'Knows nothing.',
    'seetext': 'Knows nothing',
    'sees': []}
}

# Storage data structures
class Person(ndb.Model):
  id = ndb.IntegerProperty()
  name = ndb.StringProperty()
  role = ndb.StringProperty()
  
class Role(ndb.Model):
  id = ndb.IntegerProperty()
  role = ndb.StringProperty()
  
class Game(ndb.Model):
  date = ndb.DateTimeProperty(auto_now_add=True)
  gamekey = ndb.StringProperty()

class Mission(ndb.Model):
  completed = ndb.BooleanProperty()
  failsRequred = ndb.IntegerProperty()
  fails = ndb.IntegerProperty()
  who = ndb.StructuredProperty(Role, repeated=True)

def master_key(key = 'default'):
  return ndb.Key('Master', key)

def game_key(key = 'default_game'):
  return ndb.Key('Game', key)
  
def get_ppl(key = 'default_game'):
  return Person.query(ancestor = game_key(key)).order(Person.id).fetch(10)
  
def num_ppl(key = 'default_game'):
  return Person.query(ancestor = game_key(key)).count()
  
def get_roles(key = 'default_game'):
  return Role.query(ancestor = game_key(key)).order(Role.id).fetch(20)
  
def get_games():
  return Game.query().order(-Game.date)
  
def clear_data(key = 'default_game'):
  for p in get_ppl(key):
    p.key.delete()
  for r in get_roles(key):
    r.key.delete()  
  for g in get_games():
    g.key.delete()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENV.get_template('index.html')
    self.response.write(template.render(''))


class UtcTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(0)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'UTC'
  def olsen_name(self): return 'UTC'


class PstTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(hours=-8)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'PST+08PDT'
  def olsen_name(self): return 'US/Pacific'

class GameHandler(webapp2.RequestHandler):
  def get(self):
    res = {}
    games = get_games()

    res['games'] = [{'key': g.gamekey,
       'time': g.date.strftime('%y-%m-%d')} for g in games]

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(res))

  def post(self):
    self.response.headers['Content-Type'] = 'application/json'
    gamekey = self.request.get('gamekey')
    masterkey = master_key()

    exists = Game.query(Game.gamekey == gamekey, ancestor = masterkey).count()
    if exists == 0 :
      game = Game(parent = masterkey)
      game.gamekey = gamekey
      game.put()
      self.response.write(json.dumps({'added': 'ok'}))
    else:
      self.response.write(json.dumps({'error': 'duplicate'}))


class PeopleHandler(webapp2.RequestHandler):
  def get(self):
    res = {}
    people = get_ppl()
    res['people'] = [ p.name for p in people ]
    player = self.request.get('player')    
    
    if player:
      prole = None
      res['sees'] = []
      
      # Find current role
      for p in people:
        if player == p.name :
          prole = p.role
          break
          
      # Find people you can see.
      res['role'] = prole
      if prole and prole in ROLE_INFO :
        for p in people:
          if p.role in ROLE_INFO[prole]['sees']:
            res['sees'].append(p.name)
      else :
        res['error'] = "No role"
        
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(res))
    
  def post(self):
    self.response.headers['Content-Type'] = 'application/json'
    name = self.request.get('name')
    if not name:
      self.response.write(json.dumps('error', 'noname'));
      return
      
    gamekey = game_key()
    exists = Person.query(Person.name == name, ancestor = gamekey).count()
    if exists == 0 :
      person = Person(parent = gamekey)
      person.id = num_ppl()
      person.name = name
      person.put()
      self.response.write(json.dumps({'added': 'ok'}))
    else:
      self.response.write(json.dumps({'error': 'duplicate'}))
    

class RoleHandler(webapp2.RequestHandler):
  def get(self):
    roles = get_roles()
    if len(roles) == 0:
      for idx, r in enumerate(ALL_ROLES) :
        role = Role(parent=game_key())
        role.id = idx
        role.role = r
        role.put()
        roles.append(role)
        
    res = {}
    res['roles'] = [ {'role':r.role, 'info':ROLE_INFO[r.role]} for r in roles ]
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(res))
    
  def post(self):
    if self.request.get('assign'):
      people = get_ppl()
      # only get enough roles to match the number of players
      roles = [ r.role for r in get_roles()][:len(people)]
      random.shuffle(roles)
      for person in people:
        person.role = roles.pop()
        person.put()
      self.redirect('/role')


class AdminHandler(webapp2.RequestHandler):
  def get(self):
    templateValues = {
      'people': get_ppl(),
      'roles': [ROLE_INFO[r.role] for r in get_roles()]
    }
    template = JINJA_ENV.get_template('admin.html')
    self.response.write(template.render(templateValues))
    
  def post(self):
    if self.request.get('del'):
      clear_data()
      self.redirect('/admin')

      
app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/ppl', PeopleHandler),
  ('/role', RoleHandler),
  ('/admin', AdminHandler),
  ('/game', GameHandler)
], debug=True)
