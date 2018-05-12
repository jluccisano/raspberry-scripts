#!/usr/bin/env python
import argparse
import sys
import json
from zone_control_helpers import *

# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 23/16	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

class ZoneControl(object):
    def set(self):
        parser = argparse.ArgumentParser(
            description='Set zone state high=1 or low=0')

        parser.add_argument('--zone', help='Set zone 1/2/3/4/5 or *', required=False)
        parser.add_argument('--state', help='Set state high=1 or low=0', required=True)

        args = parser.parse_args(sys.argv[2:])

        if args.zone:
            return json.dumps(set_zone(args.zone, args.state))

        else:
            return json.dumps(set_all_zones(args.state))

    def toggle(self):
        parser = argparse.ArgumentParser(
            description='Toggle zone value')

        parser.add_argument('--zone', help='Set zone 1/2/3/4/5', required=False)

        args = parser.parse_args(sys.argv[2:])

        if args.zone:
            return json.dumps(toggle_zone(args.zone))

    def get(self):
        parser = argparse.ArgumentParser(
            description='Set zone state high=1 or low=0')

        parser.add_argument('--zone', help='Set zone 1/2/3/4/5 or *', required=False)

        args = parser.parse_args(sys.argv[2:])

        if args.zone:
            return json.dumps(get_zone(args.zone))
        else:
            return json.dumps(get_all_zones())

    def scenario(self):
        parser = argparse.ArgumentParser(
            description='Set a json file')

        parser.add_argument('--json', help="[{ 'duration':10, 'zone':1, 'description':'Zone A'}...]", required=True)

        args = parser.parse_args(sys.argv[2:])
        run_scenario(args.json)

    def reset(self):
        return json.dumps(set_all_zones(1))

    def __init__(self):

        parser = argparse.ArgumentParser(
            description='Zone control',
            usage='''zone <command> [<args>]
		The most commonly used zone commands are:
		   set     Set zone value high or low
		   get     Get zone value high or low
		   toggle  Toggle zone value
		   reset Turn off all zones
           scenario Run a scenario from json
		''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


if __name__ == '__main__':
    ZoneControl()
