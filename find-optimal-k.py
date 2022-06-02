from tslearn.metrics import cdist_dtw
import tslearn.clustering

##############################################################
# Computes the silhouette score of each value of k in krange #
##############################################################

krange = range(2, 9)

scores = list()
dmetric = "softdtw"

def kmeans(clustercount):
    global scores
    km = TimeSeriesKMeans(n_clusters=clustercount,
                           metric=dmetric,
                           # metric_params={"gamma": .01},
                           verbose=False,
                           random_state=seed,
                           n_jobs=-1)
    clstrs = km.fit_predict(X_train)

    sil = tslearn.clustering.silhouette_score(X_train, clstrs, metric="softdtw", n_jobs=-1)
    print("(k, sil) = ({0}, {1:.4f})".format(clustercount,sil))
    scores.append(sil)



for k in krange:
    kmeans(k)