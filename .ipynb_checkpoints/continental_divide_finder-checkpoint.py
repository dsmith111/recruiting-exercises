# Continental Divide Challenge
# I didn't get a chance to actually code this during the interview, so here it is. So whenever you're not busy, I would appreciate any feedback
# It was nice talking to you Braden, thanks for the advice you've already given!


class Continental_Divide:
    
    def __init__(self, map):
        self.map = map
        self.divides = []
        self.upTrend = True
        self.cardinal = [[0, 1], [-1, 0], [0, -1], [1, 0]]
        self.potential_div = []
        self.prev = []
        
    def setUp_visited(self):
        linear_map = []
        
        for strip in self.map:
            linear_map += strip
            
        self.visited = dict.fromkeys(list(range(len(linear_map))), False)
    
    def valid_neighbor(self, row, col):
        
        for direction in range(4):
            new_row = row + self.cardinal[direction][0]
            new_col = col + self.cardinal[direction][1]
            
            if new_row >= len(self.map) or new_row < 0:
                continue
            
            if new_col >= len(self.map[0]) or new_col < 0:
                continue
            
            if self.upTrend:
                if self.map[new_row][new_col] >= self.map[row][col]:

                    if [new_row, new_col] in self.divides or self.visited[new_col + (new_row * 3)] == True:
                        continue
                
                else:
                    
                    if [new_row, new_col] in self.divides or self.visited[new_col + (new_row * 3)] == True:
                        continue
                    
                    self.upTrend = False
                    self.potential_div = [row, col]
                
                self.prev = [row, col]
                return [new_row, new_col]
            
            else:
                if self.map[new_row][new_col] <= self.map[row][col]:
                    if [new_row, new_col] in self.divides or self.visited[new_col + (new_row * 3)] == True:
                        continue
                    
                    return [new_row, new_col]
                
        return self.prev
            
            
        
    def crawl(self):
        
           
            self.setUp_visited()
            for row in range(len(self.map)):
                col = 0
                new_row = row
                new_col = col
                self.upTrend = True
                    
                while True:
                    index = new_col + (new_row * 3)
                    self.visited[index] = True
                    coordinates = self.valid_neighbor(new_row, new_col)
                    
                    if coordinates == [row, col] or coordinates == None:
                        break
                    new_row, new_col = coordinates
                    
                    if new_col + 1 >= len(self.map[0]):
                        self.divides.append(self.potential_div)
                        break
                        
            return self.divides
                
            
# Main (Uncomment for a non unit-test testing)
#continent = [[1, 2, 1, 1],
#             [3, 1, 1, 2],
#             [1, 1, 3, 2]]

#cd = Continental_Divide(continent)

#print("Continental Divides:\n{}".format(cd.crawl()))
            