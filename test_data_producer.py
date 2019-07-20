import query_eliminator as el
import query_repo as repo

path = ".../test_queries.csv"

Queries = el.cleaner1(path)
Queries["statement"] = el.cleaner2(Queries["statement"],800)
Queries = el.cleaner3(Queries, Queries["statement"])
Queries = repo.DeleteDuplicates(Queries)

# f1 = open("test/with_from.csv", "w")
f2 = open("test/with_select.csv", "w")

for i,s in Queries["statement"].iteritems():
	count = 0
	if "'" in s: continue # avoids bug in MySQL query execution
	try:
		statement = repo.ClausesTokenizer(i,s)
	except AttributeError:
		continue
	for st in statement:
		if st[2] == "select": count+=1 # changes depended on file ("select", "from")
	if count >= 3:
		f2.write(Queries["statement"][i]) # changes depended on file (f1, f2)
		f2.write("\n") # changes depended on file (f1, f2)

# f1.close()
f2.close()