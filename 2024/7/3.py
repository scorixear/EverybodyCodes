import os, sys
import time

class Chariot:
    def __init__(self, actions: list[str]):
        self.power: int = 10
        self.total: int = 0
        self.actions: list[str] = actions
    def move(self, track: list[str]):
        laps_total = 0
        # every 11 laps, we reached get back to the starting condition
        # since 2024/11 = 184, we can just multiply the total power by 184
        for i in range(len(track)*11):
            # get the action for the current lap
            action = self.actions[i % len(self.actions)]
            # get the action of the track
            track_action = track[(i+1) % len(track)]
            # if the track action does nothing
            if track_action == "=" or track_action == "S":
                # apply chariot action
                if action == "+":
                    self.power += 1
                elif action == "-":
                    self.power -= 1
                    if self.power < 0:
                        self.power = 0
            # otherwise apply the track action
            elif track_action == "+":
                self.power += 1
            elif track_action == "-":
                self.power -= 1
                if self.power < 0:
                    self.power = 0
            laps_total += self.power
        self.total = laps_total * 184

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    with open(os.path.join(sys.path[0],"i3t.txt"), "r", encoding="utf-8") as f:
        track_lines = f.read().strip().split("\n")
    # we start at the top left corner and move right
    track = ['S', track_lines[0][1]]
    prev_x = 0
    prev_y = 0
    current_x = 1
    current_y = 0
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # move until we find the start
    while True:
        found_start = False
        # try all moves
        for move in moves:
            next_x = current_x + move[0]
            next_y = current_y + move[1]
            # if we are going back, ignore
            if next_x == prev_x and next_y == prev_y:
                continue
            # if we are in bounds
            if 0 <= next_y < len(track_lines) and 0 <= next_x < len(track_lines[next_y]):
                # if we are on the track
                if track_lines[next_y][next_x] != " ":
                    # if we found the start, ignore
                    if track_lines[next_y][next_x] == "S":
                        found_start = True
                        break
                    # add the track step to the track
                    track.append(track_lines[next_y][next_x])
                    prev_x = current_x
                    prev_y = current_y
                    current_x = next_x
                    current_y = next_y
                    break
        # iterate until we find the start
        if found_start:
            break
    print("".join(track))
    
    # calculate the total score for the enemy chariot
    enemy_chariot = Chariot(lines[0].split(":")[1].split(","))
    enemy_chariot.move(track)
    enemy_total = enemy_chariot.total
    
    # all possible moves
    possible_moves = (["+"]*5)+(["-"]*3)+(["="]*3)
    # we don't want to repeat the same moves
    seen: set[str] = set()
    # start the recursive function
    print(find_winning(possible_moves[:], track, enemy_total, [], seen))

def find_winning(possible_moves: list[str], track: list[str], enemy_total: int, moves: list[str], seen: set[str]):
    # if we already saw this combination of moves, ignore
    if "".join(moves) in seen:
        return 0
    seen.add("".join(moves))
    # if we have used all possible moves
    if(len(possible_moves) == 0):
        # calculate the total score for the chariot
        chariot = Chariot(moves)
        chariot.move(track)
        # if the chariot has a higher score than the enemy, return 1
        if chariot.total > enemy_total:
            return 1
        return 0
    counter = 0
    # try all possible moves
    for i, move in enumerate(possible_moves):
        # remove the move from the list
        new_possible_moves = possible_moves[:]
        new_possible_moves.pop(i)
        # and find all possible winning actions with the remaining moves
        counter += find_winning(new_possible_moves, track, enemy_total, moves+[move], seen)
    return counter

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
