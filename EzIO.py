import re

def FindAnswer(response, answers):
	for answer, regex in answers.items():
		if not(re.findall(regex, response)):
			continue
		return answer
	raise Exception('Invalid response')

def Get(answers):
	while True:
		try:
			ans = FindAnswer(input().lower(), answers)
			print()
			return ans
		except:
			continue

def Ask(question, answers={}):
	print(question)
	
	if answers:
		return Get(answers)
	
	val = input()
	print()
	return val

def AskBool(question):
	return Ask(question,{
		True:  r'^(1|y(es)?|t(rue)?)$',
		False: r'^([0x]|no?|f(alse)?)$'
	})

def AskAB(question, a, b):
	return Ask(question,{
		 1: rf'^([al1>]|left|{a.lower()})$',
		-1: rf'^([br2<]|right|{b.lower()})$',
		 0: r'^(?![\s\S])|^( |==?|\?)$'
	})

def ColLen(table, n):
	return max(map(lambda x: len(str(x[n])), table))