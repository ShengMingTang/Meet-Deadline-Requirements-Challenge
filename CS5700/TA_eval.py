"""
This is the CS5700 Introduction to MM Term Project 1: Meet the deadline Requirements Challenge

TA: Shengming Tang
emial: shengming0308@gapp.nthu.edu.tw

This file will be used to evaluate all of the studnets' scripts

For Students:
    Note that since we will use our script to evaluate your codes


    Template has been provided in s000000000/solution.py
    This module must include config = {'USE_CWND': True/False, 'ENABLE_LOG': True/False}
    Class instantiation of the MySolution() must remain as it is or it must inherit at least the two parent classes
    the methods call of select_block(.), on_packet_sent(.), cc_trigger(.) must remain the same

    Any additional method is okay to implemented by yourselves



directory structure:

root
|
|   --- s000000001 (f's{studentID}')
|   |
|   |   --- solution.py
|   |   --- sideModule.py
|   |   --- requirements.txt
|   |   --- output (produced at runtime)
|       |
|       |   --- run{i} (produced at runtime)
|       |   --- ...
|   --- s000000002
|   .
|   .
|   .
|   --- hidden (testcase)
|   |
|   |   --- background_traffic_traces
|   |   |
|   |   |   --- *.csv
|   |
|   |   --- scenario*
|   |   |
|   |   |   --- blocks
|   |   |   --- newtworks
|
|   qoe.csv (for your total qoe)

"""

import argparse
from cgi import test
from simple_emulator import SimpleEmulator, create_emulator

# We provided some function of plotting to make you analyze result easily in utils.py
from simple_emulator import analyze_emulator, plot_rate

# we use our qoe
# from simple_emulator import cal_qoe

import random
import importlib

# evaluation
from pathlib import Path
import sys
import json
import re
import csv
import numpy as np
import subprocess
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"

RANDOM_SEED = 0

def cal_qoe(x=0, run_dir=None):
    block_data = []
    qoe = .0
    tmp = [3, 2, 1]
    if run_dir:
        if run_dir[-1] != '/':
            run_dir += '/'
    else:
        run_dir = './'
    with open(run_dir + "output/block.log", "r") as f:
        for line in f.readlines():
            data = json.loads(line.replace("'", '"'))
            # not finished
            if data["Miss_ddl"] == 0 and data["Size"] - data["Finished_bytes"] > 0.000001:
                continue
            block_data.append(data)
    for block in block_data:        
        priority = float(tmp[int(block['Priority'])] / 3)
        if block["Miss_ddl"] == 0:
            qoe += priority
        elif abs(x) > 0.00001:
            qoe -= x*priority
    return qoe
def run_and_plot(emulator, network_trace, log_packet_file, **kwargs):
    # Run the emulator and you can specify the time for the emualtor's running.
    # It will run until there is no packet can sent by default.
    emulator.run_for_dur()

    # print the debug information of links and senders
    emulator.print_debug()

    # Output the picture of emulator-analysis.png
    # You can get more information from https://github.com/AItransCompetition/simple_emulator/tree/master#emulator-analysispng.
    # analyze_emulator(log_packet_file, file_range="all", sender=[1])

    # Output the picture of rate_changing.png
    # You can get more information from https://github.com/AItransCompetition/simple_emulator/tree/master#cwnd_changingpng
    # plot_rate(log_packet_file, trace_file=network_trace, file_range="all", sender=[1])

    print("Qoe : %d" % (cal_qoe(run_dir=kwargs['RUN_DIR'])) )
def evaluate(solution_file, block_traces, network_trace, log_packet_file, config=None, second_block_file=None, **kwargs):
    # fixed random seed
    # import random
    # random.seed(1)

    # import the solution
    solution = importlib.import_module(solution_file)

    # Use the object you created above
    my_solution = solution.MySolution()

    # Create the emulator using your solution
    # Set second_block_file=None if you want to evaluate your solution in situation of single flow
    # Specify ENABLE_LOG to decide whether or not output the log of packets. ENABLE_LOG=True by default.
    # You can get more information about parameters at https://github.com/AItransCompetition/simple_emulator/tree/master#constant
    emulator = create_emulator(
        block_file=block_traces,
        second_block_file=second_block_file,
        trace_file=network_trace,
        solution=my_solution,

        # config
        USE_CWND=config['USE_CWND'],
        # enable logging packet. You can train faster if ENABLE_LOG=False
        ENABLE_LOG=config['ENABLE_LOG'],

        # Extra params
        **kwargs
    )
    run_and_plot(emulator, network_trace, log_packet_file, **kwargs)

def testCaseGen(scenarios, backgrounds):
    for scn in scenarios:
        # print(scn)
        for bg in backgrounds:
            for nw in scn.glob('networks/*.txt'):
                # yield ([block], network, background)
                yield ([str(i) for i in scn.glob('blocks/*.csv')], nw, str(bg))

def TAevalSingle(dir):
    print(f'evaluating {str(dir)}')
    
    os.chdir(dir)
    
    solution_file = f'{dir}.solution'
    solModule = importlib.import_module(solution_file)
    config = solModule.config

    # outputRoot = dir/'output'
    outputRoot = Path('output')
    outputRoot.mkdir(exist_ok=True)

    scenarios = list((Path('.')/'..'/'hidden').glob('scenario_*/'))
    backgrounds = list((Path('.')/'..'/'hidden'/'background_traffic_traces').glob('*.csv'))

    for i, (block_traces, network_trace, second_block_file) in enumerate(testCaseGen(scenarios, backgrounds)):
        log_packet_file = outputRoot/f'run{i}'
        log_packet_file.mkdir(exist_ok=True)
        runTimeLogFile = log_packet_file/'log.txt'
        errFile = log_packet_file/'err.txt'

        kwargs = {'RUN_DIR': str(log_packet_file)}
        with open(errFile, 'w') as sys.stderr:
            with open(runTimeLogFile, 'w') as sys.stdout:
                evaluate(
                    solution_file=solution_file,
                    block_traces=block_traces,
                    network_trace=network_trace,
                    log_packet_file=log_packet_file,
                    config=config,
                    second_block_file=second_block_file,

                    **kwargs
                )
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print(f'  run {i} evaluated')
    os.chdir(Path('..'))
    print(f'finish evaulating {str(dir)}')

    # calculate QoE
    print(f'Calculating QoE of {str(dir)}')
    qoe = []
    for p in (dir/'output').glob('run[0-9]*/log.txt'):
        with open(p, 'r') as f:
            for line in f.readlines():
                g = re.match(r'(?P<key>Qoe : )(?P<val>[0-9]*.[0-9]*)', line)
                if g:
                    qoe.append(float(g.group('val')))
    return {'qoe': qoe}


if __name__ == '__main__':
    # Random seed will be different when evaluating
    random.seed(RANDOM_SEED)
    
    sys.path.insert(0, '.')
    root = Path('.')
    scenarios = list((root/'hidden').glob('scenario_*/'))
    backgrounds = list((root/'hidden'/'background_traffic_traces').glob('*.csv'))
    print('============== TA Info ==============')
    print(f'Used scenarios {[str(scn) for scn in scenarios]}')
    print(f'Used background traffic {[str(bg) for bg in backgrounds]}')
    numTestCases = 0
    for item in testCaseGen(scenarios, backgrounds):
        numTestCases += 1
    print(f'Used testcases: {numTestCases}')
    print('============== TA Info ==============')

    total_qoe = root/'qoe.csv'
    with open(total_qoe, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['studentID', *[f'run{i}' for i in range(numTestCases)], 'totalQoe'])
        for dir in root.glob('s[0-9]*/'):
        # for dir in root.glob('s[0-9]*1/'):
            env = f'Env_{str(dir)}'
            req = str(dir/'requirements.txt')
            subprocess.run(['conda', 'env', 'remove', '--name', env, '-y'])
            subprocess.run(['conda', 'create', '--name', env, '-y'])
            subprocess.run(['conda', 'activate', env])
            subprocess.run(['conda', 'config', '--env', '--set', 'always_yes', 'true'])
            subprocess.run(['conda', 'install', 'pip'])
            # subprocess.run(['conda', 'config', '--append', 'channels', 'conda-forge'])
            subprocess.run(['pip', 'install', '-r', req])
            try:
                stat = TAevalSingle(dir)
                print(f'{dir} qoe = {stat["qoe"]}')
                writer.writerow([dir.stem, *(stat['qoe']), np.sum(np.array(stat["qoe"]))])
            except Exception as e:
                print(f'{str(dir)} raise ')

                

            subprocess.run(['conda', 'deactivate'])

