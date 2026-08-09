#!/usr/bin/env python
import argparse
import sys

# torchlight
# import torchlight
from app.torchlight.torchlight import import_class


def generate(file_path):
    # file_path="D:/pose_estimate/openpouseDemo/djangoProject2/app/resource/media/ta_chi.mp4"
    sys.argv = ['main.py', 'demo_offline', '--openpose', 'D:/pose_estimate/openpose-1.7.0/build/x64/Release', '--video',
                file_path]
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

    response, name = p.start()
    return response, name


# if __name__ == '__main__':
#     response ,name=generate("D:/pose_estimate/openpouseDemo/djangoProject2/clean_and_jerk.mp4")
#     print(response,name)