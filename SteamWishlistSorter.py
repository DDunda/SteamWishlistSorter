import re
import json
import requests
import math

from EzIO import *
from random import shuffle
from functools import cmp_to_key

# Solution taken from here:
# https://stackoverflow.com/a/59439726
def GetWishlistUrl(username):
	url = f'https://store.steampowered.com/wishlist/id/{username}'
	return json.loads(re.findall(r'g_strWishlistBaseURL = (".*?");', requests.get(url).text)[0])

def TryGetUrl(username):
	while True:
		try:
			return GetWishlistUrl(username)

		except:
			print("Sorry, I couldn't find your wishlist.")
			username = input()
			print()

			if username in ['','exit','quit']:
				print('See ya.')
				quit()

url = TryGetUrl(Ask('What is your steam username?'))
sorting  = Ask(
	'Start by sorting randomly, by player score, or by your ranking? (This affects the order questions are asked)',
	{
		'order': r'^(m(y|ine)?|personal|rank(ing)?|order)$',
		'reviewscore': r'^(p(layers?)?|global|public|steam|reviews|(review ?)?score)$',
		'random': r'^(r(and(om(ly)?)?)?|shuffled?)$'
	}
)
exc_soon = AskBool('Exclude unreleased games?')

p = 0
data = {}
while True:
	new_data = requests.get(url + 'wishlistdata/?p={p}}').json()
	
	keys = list(new_data.keys())
	for n in keys:
		if n in data:
			new_data.pop(n)

	if not new_data:
		break

	data = data | new_data
	p += 1

if len(data.keys() < 2):
	if len(data.keys()) == 0:
		print("You don't have any games to sort.")
	else:
		print("You can't sort one game.")
	exit()

# Always sort by ranking initially, so that the proper order is implied if unreleased games are filtered out
games = sorted(data.values(), key = lambda x: x['priority'])

if exc_soon:
	games = list(filter(lambda x: not ('prerelease' in x), games))
	for i in range(len(games)):
		games[i]['priority'] = i + 1

if sorting == 'random':
	shuffle(games)
elif sorting == 'reviewscore':
	games = sorted(games, key = lambda x: x['reviews_percent'], reverse = True)

# These magic numbers were found through experimentation. TimSort is usually known as O(n*log(n)) at worst
print(f'Number of questions: {len(games) - 1} (best) ~{round(0.82110185153 * (len(games)-1) * math.log(3.38 * (len(games)-1)))} (worst)\r\n')

q = 1
questions = dict((game['name'],[]) for game in games)
n_games = len(games)
la = ""
gt = 0

def Compare(A, B):
	global q, la, gt

	a = A['name']
	b = B['name']

	if a != la:
		la = a
		gt += 1
	
	if b in questions[a]:
		return 1
	
	if a in questions[b]:
		return -1
	
	AB = AskAB(f'Question {q} ({gt}/{n_games}):\r\n{a} or {b}?', a, b)
	q += 1
	
	if AB == 0:
		return AB
	
	if AB == -1:
		b = A['name']
		a = B['name']
	
	questions[a].append(b)
	
	if len(questions[b]) == 0:
		return AB

	for n in questions[b]:
		if not (n in questions[a]):
			questions[a].append(n)

	return AB

games.sort(key = cmp_to_key(Compare), reverse = True)

out = []
i = 1
for game in games:
	osc = game["priority"]
	out.append([i, game["name"], "▲" if osc > i else ("▼" if osc < i else "•"), abs(osc - i)])
	i += 1

row_f  = '{:>' + str(ColLen(out, 0)) + '}: '
row_f += '{:<' + str(ColLen(out, 1)) + '} '
row_f += '({} {:>' + str(ColLen(out, 3)) + '})'

for row in out:
	print(row_f.format(*row))

print()

if len(games) == 2:
	print('(Did you really need this program for two games?)')
	print()

Ask("\r\nPress any key to exit")