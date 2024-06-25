import sys

from src.load_map import LoadMap


def main():
    map = LoadMap(sys.argv[1])
    print(map.get_start_coordinates())
    print(map.get_goal_coordinates())
    print(map.get_speed())
    print(map.get_optimal_actions())


if __name__ == "__main__":
    main()
