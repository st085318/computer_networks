import json
class Node:
    def __init__(self, ip, neighbours, inf = 16):
        self._ip = ip
        self._neighbours = neighbours
        self.inf = inf
        self._routing_table = {n: {'dist': 1, 'next': n} for n in neighbours}
        self._routing_table[ip] = {'dist': 0, 'next': ip}

    def update_destination(self, node, neighbour, dist):
        if node not in self._routing_table or self.get_dist_to_node(node) > dist:
            self._routing_table[node] = {'dist': dist, 'next': neighbour}
            return True
        return False

    @property
    def ip(self):
        return self._ip
    
    @property
    def neighbours(self):
        return self._neighbours
    
    @property
    def destination(self):
        return list(self._routing_table.keys())
    
    def get_dist_to_node(self, node):
        if node in self._routing_table:
            return self._routing_table[node]['dist']
        else:
            return self.inf
    
    def print_routing_table(self):
        msg = f'[Source IP]        [Destination IP]   [Next Hop]         [Metric]\n'
        indent = 3 * 4 + 3 + 4
        for (router, info) in self._routing_table.items():
            if router == self.ip:
                continue
            msg += f'{self._ip}{" " * (indent - len(self._ip))}'
            msg += f'{router}{" " * (indent - len(router))}'
            next_hop = info['next']
            msg += f'{next_hop}{" " * (indent - len(next_hop))}'
            metric = info['dist']
            msg += f'{metric}\n'
        msg += '\n'
        print(msg)


class Network:
    def __init__(self, networks, inf = 16):
        self.networks = networks
        self.ip2router = {}
        for ip in networks:
            router = Node(str(ip), networks[str(ip)])
            self.ip2router[ip] = router
        self.inf = 16
        
    def update_node_destinations(self, node):
        is_update = False
        for neighbour_ip in node.neighbours:
            neighbour = self.ip2router[neighbour_ip]
            for router in neighbour.destination:
                dist = neighbour.get_dist_to_node(router) + 1
                if dist >= self.inf:
                    continue
                is_update |= node.update_destination(router, neighbour_ip, dist)
        return is_update

    def rip(self):
        is_update = True
        step = 0
        print(f'{"#" * 65}\n')
        while is_update:
            step += 1
            is_update = False
            for (ip, node) in self.ip2router.items():
                is_update_now = self.update_node_destinations(node)
                is_update |= is_update_now
                if is_update_now:
                    print(f'Simulation step {step} of router {ip}')
                    node.print_routing_table()

    def print_final(self):
        print(f'{"#" * 65}\n')
        for ip, router in self.ip2router.items():
            print(f'Final state of router {ip} table:\n')
            router.print_routing_table()

    def print_network(self):
        indent = 3 * 4 + 3 + 4
        print(f'[IP]{" " * (indent - 4)}[Neighbours]\n')
        for (ip, conn) in self.networks.items():
            print(f'{ip}{" " * (indent - len(ip))}{conn}\n')
        print('\n')

if __name__ == '__main__':
    networks = json.load(open('network.json'))
    net = Network(networks)
    net.print_network()
    net.rip()
    net.print_final()



