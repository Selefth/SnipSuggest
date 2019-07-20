import SnipSuggest as ss
import mysql.connector

DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_NAME = "SDSS"
DATABASE_PASSWD = "***"

mydb = mysql.connector.connect(
	host=DATABASE_HOST,
	user=DATABASE_USER,
	passwd=DATABASE_PASSWD,
	database=DATABASE_NAME
)

mycursor = mydb.cursor()

def Random(fids, clause_requested, k):
	if len(fids) != 0:
		sql = "SELECT qf.feature FROM QueryFeatures qf, (SELECT query FROM QueryFeatures WHERE feature in ("+ ','.join(str(f) for f in fids) +") GROUP BY query) as sq WHERE qf.query = sq.query AND qf.feature NOT IN ("+ ','.join(str(f) for f in fids) +") GROUP BY qf.feature ORDER BY RAND()"
	else:
		sql = "SELECT qf.feature FROM QueryFeatures qf ORDER BY RAND()"
	candidates, suggestions = [], []
	mycursor.execute(sql)
	candidates = mycursor.fetchall()
	for f in candidates:
		if str(f[0]) not in suggestions and ss.clause(str(f[0])) == clause_requested: suggestions.append(str(f[0]))
	return suggestions[:k]

def popularity_based(fids, clause_requested, k):
	if len(fids) != 0:
		sql = "SELECT qf.feature FROM QueryFeatures qf, (SELECT * FROM MarginalProbs) as mp, (SELECT query FROM QueryFeatures WHERE feature in ("+ ','.join(str(f) for f in fids) +") GROUP BY query) as sq WHERE qf.query = sq.query AND qf.feature NOT IN ("+ ','.join(str(f) for f in fids) +") AND qf.feature = mp.featureID GROUP BY qf.feature ORDER BY mp.probability DESC"
	else:
		sql = "SELECT mp.featureID FROM MarginalProbs mp ORDER BY mp.probability DESC"
	candidates, suggestions = [], []
	mycursor.execute(sql)
	candidates = mycursor.fetchall()
	for f in candidates:
		if str(f[0]) not in suggestions and ss.clause(str(f[0])) == clause_requested: suggestions.append(str(f[0]))
	return suggestions[:k]

def remove_features(all_features, clause, num_to_remove="all"):
	removed_features = []
	for f in all_features:
		if f[2] == clause:
			removed_features.append(f)
		if num_to_remove == "all":
			continue
		else:
			if len(removed_features) == num_to_remove:
				break
			else:
				continue
	return [f[1] for f in removed_features]

def features_knowledge(all_features, removed_features):
	return [f for f in all_features if f[1] not in removed_features]

def rel(features_required, features_suggested, i):
	if str(features_suggested[i]) in features_required:
		return 1
	else:
		return 0

def precision(features_required, features_suggested, k):
	sum = 0.0
	for i in range(k+1):
		sum = sum + rel(features_required, features_suggested, i)
	return sum / (k+1)
  
def average_precision(features_required, features_suggested, k):
	sum= 0.0 
	for i in range(k):
		sum = sum + (precision(features_required, features_suggested, i) * rel(features_required, features_suggested, i))
	return sum / (len(features_required))

def utility(features_required, features_suggested):
	u = 0
	for f in features_suggested:
		if f in features_required: u = 1
	return u