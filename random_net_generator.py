# -*-coding:utf-8-*-
import time
import copy
import numpy as np
import random
import argparse
import sys
import textwrap

class ConditionEventNetGenerator:
    def __init__(self, A=2, U=2, H=4):
        self._event_id = 0
        self._max_multi_net_size = A
        self._max_multi_time = U
        self._max_condition_event_num = H
        self._connected_edges = []
        self._event_list = []
        self._condition_list = []

    def generate_net(self, event_list, condition_list):
        i = 1
        self._event_id = len(event_list) + 1
        while i <= self._max_multi_time:
            event_list, condition_list = self.new_multi_net(event_list, condition_list, i)
            i = i + 1

        self._event_list.extend(event_list)
        self._condition_list.extend(condition_list)

    def new_multi_net(self, event_list, condition_list, i):
        event_i = []
        condition_i = []
        j = random.randint(1, self._max_multi_net_size)
        n = 1
        while n <= j:
            event_i, condition_i = self.new_single_net(event_i, condition_i)
            n = n + 1

        return self.connect(event_list, condition_list, event_i, condition_i)

    def new_single_net(self, E, C):
        new_envent_list = []
        new_condition_list = []

        j = random.randint(1, self._max_condition_event_num)
        k = random.randint(1, self._max_condition_event_num)

        #构造事件
        e = 'e%d(%d,%d)' % (self._event_id, -j, k)
        new_envent_list.append(e)

        i = -j
        while i >= -j and i <= k:
            if i != 0:
                c = 'e%d(%d)'%(self._event_id, i)
                new_condition_list.append(c)
                if i > 0:
                    self._connected_edges.append((e, c))
                else:
                    self._connected_edges.append((c, e))

            i = i+1

        E, C = self.connect(E, C, new_envent_list, new_condition_list)
        self._event_id += 1
        return E, C

    def connect(self, E, C, E1, C1):
        if len(E) == 0:
            return E1, C1

        condition_size = len(C)
        to_be_connected = []
        while len(to_be_connected) < condition_size:
            l = random.randint(0, condition_size - 1)
            if l not in to_be_connected:
                to_be_connected.append(l)

        condition_size_1 = len(C1)
        condition_size_2 = len(C)
        condition_time = random.randint(1, condition_size_1)
        wait_connected_edges = []
        connected_conditions_1 = []
        connected_conditions_2 = []
        while len(connected_conditions_1) < condition_time:
            r = random.randint(0, condition_size_1 - 1)
            if r not in connected_conditions_1:
                connected_conditions_1.append(r)
                u = 0
                if r >= len(to_be_connected):
                    u = r % condition_size_2
                    u = to_be_connected[u]
                else:
                    u = to_be_connected[r]

                if u not in connected_conditions_2:
                    connected_conditions_2.append(u)
                else:
                    continue

                wait_connected_edges.append((C[u], C1[r]))

        for edge in wait_connected_edges:
            if edge[1] in C1:
                C1.remove(edge[1])

            edge_i = 0
            while edge_i < len(self._connected_edges):
                (lnode, rnode) = self._connected_edges[edge_i]
                needs_remove = 0
                if lnode == edge[1]:
                    lnode = edge[0]
                    needs_remove = 1

                if rnode == edge[1]:
                    rnode = edge[0]
                    needs_remove = 1

                if needs_remove == 1:
                    self._connected_edges.pop(edge_i)
                    self._connected_edges.insert(edge_i, (lnode, rnode))

                edge_i += 1

        C.extend(C1)
        E.extend(E1)

        return E, C

    def dump(self, output):
        f = open(output, "w")
        f.write('event\n')
        for event in self._event_list:
            f.write(event + '\n')

        f.write('condition\n')
        for condition in self._condition_list:
            f.write(condition + '\n')

        f.write('edge\n')
        for edge in self._connected_edges:
            f.write(edge[0] + ', ' + edge[1] + '\n')

        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="random generate c/e net.      ",
    usage='use "python %(prog)s --help" for more information.',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="Typical usage:\n"
        "\tpython %(prog)s --s 2 --t 4 --c 4 --o output.txt")

    parser.add_argument('-s', '--multinetsize',required=False, help=textwrap.dedent('''The max multi-net size'''))
    parser.add_argument('-t', '--multitime',required=False, help=textwrap.dedent('''The max multi-time'''))
    parser.add_argument('-c', '--conditioneventnum',required=False, help=textwrap.dedent('''The max condition/event num'''))
    parser.add_argument('-o', '--output', required=True, help=textwrap.dedent('''The output file'''))

    args = sys.argv[1:]
    output_file = None
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    else:
        parsed_args = parser.parse_args(args)
        output_file = parsed_args.output

        if output_file == None:
            parser.print_help()
            sys.exit(0)

        print parsed_args.multinetsize, parsed_args.multitime, parsed_args.conditioneventnum, output_file
        generator = ConditionEventNetGenerator(int(parsed_args.multinetsize), int(parsed_args.multitime), int(parsed_args.conditioneventnum))
        generator.generate_net([], [])
        generator.dump(output_file)
