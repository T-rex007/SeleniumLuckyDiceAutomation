import sys
import argparse

parser = argparse.ArgumentParser()

assertion_statment ="Ooops you may have entered an invalid bot mode\n\tAvailible modes are 'live', 'demo' and 'test'"
parser.add_argument("mode", help ="Opening Bot in demo mode", type = str)
args = parser.parse_args()
assert((args.mode == 'demo')|(args.mode =='live')|(args.mode=='test')), assertion_statment

if __name__ == '__main__' :
    print('Runnin Bot in {} mode'.format(args.mode))