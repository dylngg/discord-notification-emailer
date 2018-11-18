import threading
import time


class ClusterManager():

    def __init__(self, callback, clustering_period=10):
        """Defines a cluster manager that allows for the clustering of objects
        in a period of time. After that period of time, a callback is called
        and the cluster is reset.

        :param callback: A function to call when the clustering period is
        over. The objects in the cluster are passed into that callback as the
        sole argument.
        :param clustering_period: The period of time in seconds in which all
        objects added are clustered together.
        """
        self.callback = callback
        self.clustering_period = clustering_period
        self._clustering = False
        self._cluster = []

    def append(self, obj):
        """Appends a obj and clusters it accordingly.

        :param obj: An object that is added to the cluster
        """
        if not self._clustering:
            self._start_clustering()

        self._cluster.append(obj)

    def _start_clustering(self):
        """Starts a clustering timer that does a callback with all the obj in
        the cluster after a period of time.
        """
        self._clustering = True
        thread = threading.Thread(target=self.end_cluster)
        thread.start()

    def end_cluster(self):
        """Waits a specified period of time and calls the callback"""
        time.sleep(self.clustering_period)
        self.callback(self._cluster)
        self._cluster = []
        self._clustering = False
