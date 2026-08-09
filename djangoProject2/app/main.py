#!/usr/bin/env python
import argparse
import sys

# torchlight
# import torchlight
from app.torchlight.torchlight import import_class


def generate_real():
    sys.argv = ['main.py', 'demo', '--openpose', 'D:/pose_estimate/openpose-1.7.0/build/x64/Release', '--video',
                'camera_source']
    parser = argparse.ArgumentParser(description='Processor collection')

    # region register processor yapf: disable
    processors = dict()
    processors['recognition'] = import_class('app.processor.recognition.REC_Processor')
    processors['demo_old'] = import_class('app.processor.demo_old.Demo')
    processors['demo'] = import_class('app.processor.demo_realtime.DemoRealtime')
    processors['demo_offline'] = import_class('app.processor.demo_offline.DemoOffline')
    # endregion yapf: enable

    # add sub-parser
    subparsers = parser.add_subparsers(dest='processor')
    for k, p in processors.items():
        subparsers.add_parser(k, parents=[p.get_parser()])

    # read arguments
    arg = parser.parse_args()

    # start
    Processor = processors[arg.processor]
    p = Processor(sys.argv[2:])

    response = p.start()
    return response


if __name__ == '__main__':
    generate_real()
