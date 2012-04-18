try:
    from collections import namedtuple
except:
    from newrelic.lib.namedtuple import namedtuple

import newrelic.core.metric
import newrelic.core.trace_node

_FunctionNode = namedtuple('_FunctionNode',
        ['group', 'name', 'children', 'start_time', 'end_time',
        'duration', 'exclusive'])

class FunctionNode(_FunctionNode):

    def time_metrics(self, stats, root, parent):
        """Return a generator yielding the timed metrics for this
        function node as well as all the child nodes.

        """

        name = '%s/%s' % (self.group, self.name)
        overflow = '%s/*' % self.group
        scope = root.path

        yield newrelic.core.metric.TimeMetric(name=name, scope=scope,
                overflow=overflow, forced=False, duration=self.duration,
                exclusive=self.exclusive)

        # Now for the children.

        for child in self.children:
            for metric in child.time_metrics(stats, root, self):
                yield metric

    def trace_node(self, stats, string_table, root):

        name = '%s/%s' % (self.group, self.name)

        name = string_table.cache(name)

        start_time = newrelic.core.trace_node.node_start_time(root, self)
        end_time = newrelic.core.trace_node.node_end_time(root, self)

        #children = [child.trace_node(stats, string_table, root) for
        #            child in self.children]

        root.trace_node_count += 1

        children = []

        for child in self.children:
            if root.trace_node_count > root.trace_node_limit:
                break
            children.append(child.trace_node(stats, string_table, root))

        params = None

        return newrelic.core.trace_node.TraceNode(start_time=start_time,
                end_time=end_time, name=name, params=params, children=children)
