import query_repo as repo
import SnipSuggest as ss
import evaluation as ev
import matplotlib.pyplot as plt

# SELECT
path = .../with_select.csv"

# Test 1
# We compare SS, Random & Pop_based for empty query and ask for the top 3 suggestions for the SELECT clause

allSS_avgs, allR_avgs, allPb_avgs = [], [], []

for full_query in open(path, "r"):
	avgSS, avgR, avgPb = [], [], []
	for k in range(1,4):
		clause_to_remove = "select"
		all_features = repo.ClausesTokenizer(0, full_query)
		removed_features = ev.remove_features(all_features, clause_to_remove, 3)
		fids = [] # no knowledge

		# SnipSuggest
		SS_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "ssaccuracy")
		SS_snippets = ss.snippets(SS_suggestions)
		SS_ksnippets = SS_snippets[:k]

		# Random
		R_suggestions = ev.Random(fids, clause_to_remove, k)
		R_ksnippets = ss.snippets(R_suggestions)

		# Popularity_based
		Pb_suggestions = ev.popularity_based(fids, clause_to_remove, k)
		Pb_ksnippets = ss.snippets(Pb_suggestions)

		avgSS.append(ev.average_precision(removed_features, SS_ksnippets, k))
		avgR.append(ev.average_precision(removed_features, R_ksnippets, k))
		avgPb.append(ev.average_precision(removed_features, Pb_ksnippets, k))

	allSS_avgs.append(avgSS)
	allR_avgs.append(avgR)
	allPb_avgs.append(avgPb)

mean_allSS_avgs = [float(sum(col))/len(col) for col in zip(*allSS_avgs)]
mean_allR_avgs = [float(sum(col))/len(col) for col in zip(*allR_avgs)]
mean_allPb_avgs = [float(sum(col))/len(col) for col in zip(*allPb_avgs)]

# plot
plt.plot([1, 2, 3], mean_allSS_avgs, linestyle="--", marker=">", color="palevioletred")
plt.plot([1, 2, 3], mean_allR_avgs, linestyle="--", marker="s", color="seagreen")
plt.plot([1, 2, 3], mean_allPb_avgs, linestyle="--", marker="p", color="darkorange")

plt.legend(["SnipSuggest", "Random", "Popularity_based"], loc="upper left")
plt.xticks([1, 2, 3])
plt.ylabel("average precision", fontsize=13)
plt.xlabel("top k", fontsize=13)

plt.savefig("images/SELECT_empty.jpg")
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Test 2
# We compare SS, Random & Pop_based for partial query (3 atrr missing) and ask for the top 3 suggestions for the SELECT clause

allSS_avgs, allR_avgs, allPb_avgs = [], [], []

for full_query in open(path, "r"):
	avgSS, avgR, avgPb = [], [], []
	for k in range(1,4):
		clause_to_remove = "select"
		all_features = repo.ClausesTokenizer(0, full_query)
		removed_features = ev.remove_features(all_features, clause_to_remove, 3)
		fk = ev.features_knowledge(all_features, removed_features)
		fids = ss.find_feature_ids(fk)

		# SnipSuggest
		SS_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "ssaccuracy")
		SS_snippets = ss.snippets(SS_suggestions)
		SS_ksnippets = SS_snippets[:k]

		# Random
		R_suggestions = ev.Random(fids, clause_to_remove, k)
		R_ksnippets = ss.snippets(R_suggestions)

		# Popularity_based
		Pb_suggestions = ev.popularity_based(fids, clause_to_remove, k)
		Pb_ksnippets = ss.snippets(Pb_suggestions)

		avgSS.append(ev.average_precision(removed_features, SS_ksnippets, k))
		avgR.append(ev.average_precision(removed_features, R_ksnippets, k))
		avgPb.append(ev.average_precision(removed_features, Pb_ksnippets, k))

	allSS_avgs.append(avgSS)
	allR_avgs.append(avgR)
	allPb_avgs.append(avgPb)

mean_allSS_avgs = [float(sum(col))/len(col) for col in zip(*allSS_avgs)]
mean_allR_avgs = [float(sum(col))/len(col) for col in zip(*allR_avgs)]
mean_allPb_avgs = [float(sum(col))/len(col) for col in zip(*allPb_avgs)]

# plot
plt.plot([1, 2, 3], mean_allSS_avgs, linestyle="--", marker=">", color="palevioletred")
plt.plot([1, 2, 3], mean_allR_avgs, linestyle="--", marker="s", color="seagreen")
plt.plot([1, 2, 3], mean_allPb_avgs, linestyle="--", marker="p", color="darkorange")

plt.legend(["SnipSuggest", "Random", "Popularity_based"], loc="upper left")
plt.xticks([1, 2, 3])
plt.ylabel("average precision", fontsize=13)
plt.xlabel("top k", fontsize=13)

plt.savefig("images/SELECT_3attr.jpg")
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Test 3
# We compare SS, Random & Pop_based for partial query (4 atrr missing) and ask for the top 3 suggestions for the SELECT clause

allSS_avgs, allR_avgs, allPb_avgs = [], [], []

for full_query in open(path, "r"):
	avgSS, avgR, avgPb = [], [], []
	for k in range(1,4):
		clause_to_remove = "select"
		all_features = repo.ClausesTokenizer(0, full_query)
		removed_features = ev.remove_features(all_features, clause_to_remove, 4)
		fk = ev.features_knowledge(all_features, removed_features)
		fids = ss.find_feature_ids(fk)

		# SnipSuggest
		SS_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "ssaccuracy")
		SS_snippets = ss.snippets(SS_suggestions)
		SS_ksnippets = SS_snippets[:k]

		# Random
		R_suggestions = ev.Random(fids, clause_to_remove, k)
		R_ksnippets = ss.snippets(R_suggestions)

		# Popularity_based
		Pb_suggestions = ev.popularity_based(fids, clause_to_remove, k)
		Pb_ksnippets = ss.snippets(Pb_suggestions)

		avgSS.append(ev.average_precision(removed_features, SS_ksnippets, k))
		avgR.append(ev.average_precision(removed_features, R_ksnippets, k))
		avgPb.append(ev.average_precision(removed_features, Pb_ksnippets, k))

	allSS_avgs.append(avgSS)
	allR_avgs.append(avgR)
	allPb_avgs.append(avgPb)

mean_allSS_avgs = [float(sum(col))/len(col) for col in zip(*allSS_avgs)]
mean_allR_avgs = [float(sum(col))/len(col) for col in zip(*allR_avgs)]
mean_allPb_avgs = [float(sum(col))/len(col) for col in zip(*allPb_avgs)]

# plot
plt.plot([1, 2, 3], mean_allSS_avgs, linestyle="--", marker=">", color="palevioletred")
plt.plot([1, 2, 3], mean_allR_avgs, linestyle="--", marker="s", color="seagreen")
plt.plot([1, 2, 3], mean_allPb_avgs, linestyle="--", marker="p", color="darkorange")

plt.legend(["SnipSuggest", "Random", "Popularity_based"], loc="upper left")
plt.xticks([1, 2, 3])
plt.ylabel("average precision", fontsize=13)
plt.xlabel("top k", fontsize=13)

plt.savefig("images/SELECT_4attr.jpg")
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# FROM
path = ".../with_from.csv"

# Test 1
# We compare SS, Random & Pop_based for partial query (2 real missing) and ask for the top 3 suggestions for the FROM clause

allSS_avgs, allR_avgs, allPb_avgs = [], [], []

for full_query in open(path, "r"):
	avgSS, avgR, avgPb = [], [], []
	for k in range(1,4):
		clause_to_remove = "from"
		all_features = repo.ClausesTokenizer(0, full_query)
		removed_features = ev.remove_features(all_features, clause_to_remove, 2)
		fk = ev.features_knowledge(all_features, removed_features)
		fids = ss.find_feature_ids(fk)

		# SnipSuggest
		SS_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "ssaccuracy")
		SS_snippets = ss.snippets(SS_suggestions)
		SS_ksnippets = SS_snippets[:k]

		# Random
		R_suggestions = ev.Random(fids, clause_to_remove, k)
		R_ksnippets = ss.snippets(R_suggestions)

		# Popularity_based
		Pb_suggestions = ev.popularity_based(fids, clause_to_remove, k)
		Pb_ksnippets = ss.snippets(Pb_suggestions)

		avgSS.append(ev.average_precision(removed_features, SS_ksnippets, k))
		avgR.append(ev.average_precision(removed_features, R_ksnippets, k))
		avgPb.append(ev.average_precision(removed_features, Pb_ksnippets, k))

	allSS_avgs.append(avgSS)
	allR_avgs.append(avgR)
	allPb_avgs.append(avgPb)

mean_allSS_avgs = [float(sum(col))/len(col) for col in zip(*allSS_avgs)]
mean_allR_avgs = [float(sum(col))/len(col) for col in zip(*allR_avgs)]
mean_allPb_avgs = [float(sum(col))/len(col) for col in zip(*allPb_avgs)]

# plot
plt.plot([1, 2, 3], mean_allSS_avgs, linestyle="--", marker=">", color="palevioletred")
plt.plot([1, 2, 3], mean_allR_avgs, linestyle="--", marker="s", color="seagreen")
plt.plot([1, 2, 3], mean_allPb_avgs, linestyle="--", marker="p", color="darkorange")

plt.legend(["SnipSuggest", "Random", "Popularity_based"], loc="upper left")
plt.xticks([1, 2, 3])
plt.ylabel("average precision", fontsize=13)
plt.xlabel("top k", fontsize=13)

plt.savefig("images/FROM_2real.jpg")
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Test 2
# We compare SS, Random & Pop_based for partial query (3 real missing) and ask for the top 3 suggestions for the FROM clause

allSS_avgs, allR_avgs, allPb_avgs = [], [], []

for full_query in open(path, "r"):
	avgSS, avgR, avgPb = [], [], []
	for k in range(1,4):
		clause_to_remove = "from"
		all_features = repo.ClausesTokenizer(0, full_query)
		removed_features = ev.remove_features(all_features, clause_to_remove, 3)
		fk = ev.features_knowledge(all_features, removed_features)
		fids = ss.find_feature_ids(fk)

		# SnipSuggest
		SS_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "ssaccuracy")
		SS_snippets = ss.snippets(SS_suggestions)
		SS_ksnippets = SS_snippets[:k]

		# Random
		R_suggestions = ev.Random(fids, clause_to_remove, k)
		R_ksnippets = ss.snippets(R_suggestions)

		# Popularity_based
		Pb_suggestions = ev.popularity_based(fids, clause_to_remove, k)
		Pb_ksnippets = ss.snippets(Pb_suggestions)

		avgSS.append(ev.average_precision(removed_features, SS_ksnippets, k))
		avgR.append(ev.average_precision(removed_features, R_ksnippets, k))
		avgPb.append(ev.average_precision(removed_features, Pb_ksnippets, k))

	allSS_avgs.append(avgSS)
	allR_avgs.append(avgR)
	allPb_avgs.append(avgPb)

mean_allSS_avgs = [float(sum(col))/len(col) for col in zip(*allSS_avgs)]
mean_allR_avgs = [float(sum(col))/len(col) for col in zip(*allR_avgs)]
mean_allPb_avgs = [float(sum(col))/len(col) for col in zip(*allPb_avgs)]

# plot
plt.plot([1, 2, 3], mean_allSS_avgs, linestyle="--", marker=">", color="palevioletred")
plt.plot([1, 2, 3], mean_allR_avgs, linestyle="--", marker="s", color="seagreen")
plt.plot([1, 2, 3], mean_allPb_avgs, linestyle="--", marker="p", color="darkorange")

plt.legend(["SnipSuggest", "Random", "Popularity_based"], loc="upper left")
plt.xticks([1, 2, 3])
plt.ylabel("average precision", fontsize=13)
plt.xlabel("top k", fontsize=13)

plt.savefig("images/FROM_3real.jpg")
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SSA vs SSC

path = ".../with_select.csv"

allSSA, allSSC = [], []
for full_query in open(path, "r"):
	flag = True
	SSA, SSC = [], []

	for k in range(1,11):
		clause_to_remove = "select"
		all_features = repo.ClausesTokenizer(0, full_query)
		tokens = ev.remove_features(all_features, clause_to_remove, "all")
		fk = ev.features_knowledge(all_features, tokens)
		fids = ss.find_feature_ids(fk)

		# SnipSuggest
		SSA_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "ssaccuracy")
		SSA_snippets = ss.snippets(SSA_suggestions)
		SSA_ksnippets = SSA_snippets[:k]

		SSC_suggestions = ss.get_suggestions(fids, clause_to_remove, k, "sscoverage")
		SSC_snippets = ss.snippets(SSC_suggestions)
		SSC_ksnippets = SSC_snippets[:k]

		SSA.append(ev.utility(tokens, SSA_ksnippets))
		SSC.append(ev.utility(tokens, SSC_ksnippets))

		allSSA.append(SSA)
		allSSC.append(SSC)

mean_allSSA = [float(sum(col))/len(col) for col in zip(*allSSA)]
mean_allSSC = [float(sum(col))/len(col) for col in zip(*allSSC)]

# plot
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], mean_allSSA, linestyle="--", marker=">", color="palevioletred")
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], mean_allSSC, linestyle="--", marker=">", color="mediumaquamarine")

plt.legend(["SSaccuracy", "SScoverage"], loc="upper left")
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.ylabel("queries - any correct", fontsize=13)
plt.xlabel("top k", fontsize=13)

plt.savefig("images/SSAvsSSC.jpg")
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
