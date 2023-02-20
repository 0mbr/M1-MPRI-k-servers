class Server:
    def __init__(self, id_server):
        self.id = id_server
        self.pos_x = 0
        self.pos_y = 0
        self.moves = [(0,0)]

    def __repr__(self):
        return "server: x: " + str(self.pos_x) + ", y: " + str(self.pos_y)

    def never_move(self):
        return self.pos_x == 0 and self.pos_y == 0

    def distance_with(self, position: tuple):
        """
        :param position: 2 size of tuple, e.g. (13, 36)
        Using Manhattan distance, get distance between this server and the site position
        """
        return abs(self.pos_x - position[0]) + abs(self.pos_y - position[1])

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.moves.append((x, y))


class RunState:
    def __init__(self, k_instance):
        """
        param k_instance:
        servers: array of class Server.
        num_request: the number (position) of request (sequence), it starts from 0 to N.
        sum_distance: sum of the distances traveled by all k servers (technicians).
        """
        self.k_instance = k_instance
        self.servers = []
        self.num_request = 0
        self.sum_distance = 0
        self.turns = [] # turns[i] = what server moved for request i

        # initiation of k servers
        for index in range(self.k_instance.k):
            self.servers.append(Server(index))

    def get_customer_site(self):
        """
        :return: the current site position (location of the customer that need maintenance service),
        return type: a tuple, e.g. (12, 36).
        """
        x = self.k_instance.sites[self.k_instance.requests[self.num_request]][0]
        y = self.k_instance.sites[self.k_instance.requests[self.num_request]][1]
        # print("num_request: " + str(self.num_request))
        # print("(x, y): " + str(x) + "," + str(y))
        return x, y

    @property
    def distances(self):
        """
        :return: k size array of distances between customer site and i-th servers
        """
        distances = []
        for server in self.servers:
            distance = server.distance_with(self.get_customer_site())
            distances.append(distance)
        return distances

    def update(self, selected_server: int):
        """
        :param selected_server: number of server that treat request
        """
        if self.num_request == len(self.k_instance.requests):
            print("It is over!")
            return
        
        distance = self.distances[selected_server]
        self.sum_distance = self.sum_distance + distance

        self.servers[selected_server].move(*self.get_customer_site())
        
        self.num_request += 1
        self.turns.append(selected_server)

        # print("num_request: " + str(self.num_request))
        # print("selected server number: " + str(selected_server) + ", " + str(self.servers[selected_server]))
        # print("distances: " + str(self.distances))
        # print("Updated, sum distance: " + str(self.sum_distance))
        # print("---------------------------------------")

    @property
    def moves(self):
        '''
        Iterator on the sequence of moves done by the servers during the run. 
        Ignores the first move, registered at pos (0, 0).
        At each step, yields i_server, (x, y).
        '''
        indices = [1]*len(self.k_instance.requests)
        for s in self.turns:
            yield s, self.servers[s].moves[indices[s]]
            indices[s] += 1
