import json


from autobricks import Cluster


clusters = Cluster.cluster_list()

print(json.dumps(clusters, indent=4))