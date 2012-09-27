#!/usr/bin/env python 
from utils.munin.base import MuninGraph

class NBMuninGraph(MuninGraph):

    @property
    def graph_config(self):
        graph = {
            'graph_category' : 'NewsBlur',
            'graph_title' : 'NewsBlur Task Server Times',
            'graph_vlabel' : 'Feed fetch time / server',
        }

        stats = self.stats
        graph['graph_order'] = ' '.join(sorted(s['_id'] for s in stats))
        graph.update(dict((("%s.label" % s['_id'], s['_id']) for s in stats)))
        graph.update(dict((("%s.draw" % s['_id'], 'LINE1') for s in stats)))

        return graph

    def calculate_metrics(self):
        servers = dict((("%s" % s['_id'], s['total']) for s in self.stats))

        return servers
    
    @property
    def stats(self):
        import datetime
        from django.conf import settings
        
        stats = settings.MONGOANALYTICSDB.nbanalytics.feed_fetches.aggregate([{
            "$match": {
                "date": {
                    "$gt": datetime.datetime.now() - datetime.timedelta(minutes=5),
                },
            },
        }, {
            "$group": {
                "_id"   : "$server",
                "total" : {"$avg": "$total"},
            },
        }])
        
        return stats['result']
        

if __name__ == '__main__':
    NBMuninGraph().run()
