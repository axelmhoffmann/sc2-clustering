import os
import ast
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, \
    TimeSeriesResampler
import numpy
import matplotlib.pyplot as plt

n = 100
troops = ["drones", "zerglings", "roaches", "hydralisks", "mutalisks", "banelings"]
dmetric = "softdtw"
clustercount = 3
ylimit = 50

path = os.getcwd()

vectors = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) & f.endswith('.txt'))]
print('Reading {0} vectors...'.format(len(vectors)))

data = list()

useAllFeatures = True;

for r in vectors:
    rPath = path + "/" + r
    name = r.split('.', 1)[0]

    saveFile = open(name + '.txt', 'r')
    line = saveFile.read()
    saveFile.close()
    
    if useAllFeatures:
        multivec = ast.literal_eval(line)
        # concatenating the vectors for different features into one long vector. As each feature has the same length within a single point, they should all be scaled equally
        vec =[*multivec[0], *multivec[1], *multivec[2], *multivec[3], *multivec[4], *multivec[5]];
        data.append(vec);
    else:
        data.append(ast.literal_eval(line)[0]);



print('Resampling all time-series to length {0}'.format(n))
resampled_data = TimeSeriesResampler(sz=n).fit_transform(data)
sz = resampled_data.shape[1]

print("Clustering with: " + dmetric + " K-means")
kmeans = TimeSeriesKMeans(n_clusters=clustercount,
                           metric=dmetric,
                           # metric_params={"gamma": .01},
                           verbose=False,
                           random_state=seed,
                           n_jobs=-1)
y_pred = kmeans.fit_predict(resampled_data)

plt.figure(dpi=1200)

# Render a graph for each cluster
for yi in range(clustercount):
    
    # Graph layout
    plt.subplot(int(clustercount / 3) + 1, 3, 1 + yi)
    # Select the cluster from the data
    for xx in resampled_data[y_pred == yi]:
        plt.plot(xx.ravel(), "k-", alpha=.2)
    # Plot the mean
    plt.plot(kmeans.cluster_centers_[yi].ravel(), "r-")
    
    plt.xlim(0, sz)
    plt.xticks(numpy.arange(0, sz, sz / 6), [])
    plt.ylim(0, ylimit)
    plt.text(0.55, 0.85,'Cluster %d' % (yi + 1),
             transform=plt.gca().transAxes)
    if yi == 1:
        plt.title("Troops over game time(" + ", ".join(troops) + ")")

plt.tight_layout()
plt.savefig('cluster.png')
plt.show()