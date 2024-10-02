import random
import copy


class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = [['.' for _ in range(width)] for _ in range(height)]
        self.players = []
        self.gold_mines = []
        self.peasants = []

    def place_gold_mine(self, x, y):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.background[ny][nx] = '.'
        self.gold_mines.append((x, y))
        self.background[y][x] = 'G'

    def place_player(self, player_id):
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.background[y][x] == '.':
                self.players.append((player_id, x, y))
                self.background[y][x] = 'P'
                break

    def place_peasant(self, peasant_id):
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.background[y][x] == '.':
                self.peasants.append((peasant_id, x, y))
                self.background[y][x] = 'p'
                break

    def evaluate_map(self):
        base_distance_score = self.evaluate_base_distance()
        resource_balance_score = self.evaluate_resource_balance()
        map_geometry_score = self.evaluate_map_geometry()
        total_score = base_distance_score + resource_balance_score + map_geometry_score
        return total_score

    def evaluate_base_distance(self):
        if len(self.players) < 2:
            return 0
        x1, y1 = self.players[0][1], self.players[0][2]
        x2, y2 = self.players[1][1], self.players[1][2]
        distance = abs(x1 - x2) + abs(y1 - y2)
        return distance

    def evaluate_resource_balance(self):
        if len(self.gold_mines) < 2:
            return 0
        x1, y1 = self.gold_mines[0][0], self.gold_mines[0][1]
        x2, y2 = self.gold_mines[1][0], self.gold_mines[1][1]
        distance = abs(x1 - x2) + abs(y1 - y2)
        return 100 - distance

    def evaluate_map_geometry(self):
        terrain_variety = len(set(item for row in self.background for item in row))
        return terrain_variety * 10

    def generate_random_map(self):
        for y in range(self.height):
            for x in range(self.width):
                self.background[y][x] = '.'

        for _ in range(3):
            lake_size = random.randint(5, 10)
            lx, ly = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            for _ in range(lake_size):
                nx, ny = lx + random.randint(-2, 2), ly + random.randint(-2, 2)
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.background[ny][nx] = 'w'

        for y in range(self.height):
            for x in range(self.width):
                if self.background[y][x] == '.' and random.random() < 0.1:
                    self.background[y][x] = 't'

        for _ in range(2):
            while True:
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
                if self.background[y][x] == '.':
                    self.place_gold_mine(x, y)
                    break

        for player_id in range(2):
            self.place_player(player_id)

        for peasant_id in range(2):
            self.place_peasant(peasant_id)

    def hill_climb(self, iterations=100):
        best_map = copy.deepcopy(self)
        best_score = self.evaluate_map()

        for _ in range(iterations):
            new_map = copy.deepcopy(best_map)
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            new_map.background[y][x] = random.choice(['.', 't', 'w'])
            new_score = new_map.evaluate_map()

            if new_score > best_score:
                best_map = new_map
                best_score = new_score

        return best_map.to_xml()

    def to_xml(self):
        xml_str = "<gamestate>\n"
        xml_str += "\t<entity id=\"0\">\n"
        xml_str += "\t\t<type>map</type>\n"
        xml_str += f"\t\t<width>{self.width}</width>\n"
        xml_str += f"\t\t<height>{self.height}</height>\n"
        xml_str += "\t\t<background>\n"
        for row in self.background:
            xml_str += f"\t\t\t<row>{''.join(row)}</row>\n"
        xml_str += "\t\t</background>\n"
        xml_str += "\t</entity>\n"

        entity_id = 1
        for player_id, _, _ in self.players:
            xml_str += f"\t<entity id=\"{entity_id}\">\n"
            xml_str += f"\t\t<type>WPlayer</type>\n"
            xml_str += f"\t\t<gold>2000</gold>\n"
            xml_str += f"\t\t<wood>1500</wood>\n"
            xml_str += f"\t\t<owner>player{player_id + 1}</owner>\n"
            xml_str += "\t</entity>\n"
            entity_id += 1

        for i, (x, y) in enumerate(self.gold_mines):
            xml_str += f"\t<entity id=\"{entity_id}\">\n"
            xml_str += "\t\t<type>WGoldMine</type>\n"
            xml_str += f"\t\t<x>{x}</x>\n"
            xml_str += f"\t\t<y>{y}</y>\n"
            xml_str += f"\t\t<remaining_gold>100000</remaining_gold>\n"
            xml_str += f"\t\t<current_hitpoints>25500</current_hitpoints>\n"
            xml_str += "\t</entity>\n"
            entity_id += 1

        for i, (peasant_id, x, y) in enumerate(self.peasants):
            xml_str += f"\t<entity id=\"{entity_id}\">\n"
            xml_str += "\t\t<type>WPeasant</type>\n"
            xml_str += f"\t\t<x>{x}</x>\n"
            xml_str += f"\t\t<y>{y}</y>\n"
            xml_str += f"\t\t<owner>player{peasant_id + 1}</owner>\n"
            xml_str += f"\t\t<current_hitpoints>30</current_hitpoints>\n"
            xml_str += "\t</entity>\n"
            entity_id += 1

        xml_str += "</gamestate>\n"
        return xml_str

    def save_to_file(self, filename):
        xml_str = self.to_xml()
        with open(filename, 'w') as file:
            file.write(xml_str)


map_gen = MapGenerator(32, 32)
map_gen.generate_random_map()
best_map_xml = map_gen.hill_climb()
map_gen.save_to_file('map.xml')
