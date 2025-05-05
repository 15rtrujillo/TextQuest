import pygame as pg

from game import Game


def main():
    """Main entrypoint"""
    pg.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
