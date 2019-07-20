import SnipSuggest as ss
import query_repo as repo
import evaluation as ev

recom = True

print("Hello friend! This is SnipSuggest. \n \nOur current implementation offers suggestions for the following clauses: select, from, where, group by and with the following techniques: SSaccuracy and SScoverage.\n\nRemember that if your\
  partial query is the empty query or if it consists of features that have never appeared in the workload before, the marginal\
  probabilities of the features in our repository will be used for suggestions.\n\nHowever, if a part of your query belongs to our workload, the conditional probabilities will be used instead.")

while recom == True:

	q = input("Pass me your partial query or 0 for exit: ")
	if q == "0": break
	if ("from" not in q.lower()) & ("select" in q.lower()):
		q = q + " from" # helps the tokenizer slice it

	features = repo.ClausesTokenizer(0,str(q).lower())

	c = input("For which clause you need suggestions?: ")
	if c.lower() not in ["select", "from", "where", "group by"]:
		print("\nOops! We offer suggestions only for the following clauses: select, from, where and group by.")
		continue

	n = input("How many suggestions you want?: ")
	try:
		k = int(n)
	except ValueError:
		print("\nSorry, suggestions must be an integer number.")
		continue

	t = input("What technique do you prefer?: ")
	if t.lower() not in ["ssaccuracy", "sscoverage"]:
		print("\nSorry, I did not understand.")
		continue

	# user has defined q, c, k
	fids = ss.find_feature_ids(features)

	# SnipSuggest
	SS_suggestions = ss.get_suggestions(fids, c.lower(), k, t.lower())
	SS_snippets = ss.snippets(SS_suggestions)
	SS_ksnippets = SS_snippets[:k]

	recom = False
