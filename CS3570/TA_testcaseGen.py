from pathlib import Path
import numpy as np
def diff(d):
    '''
    calculate diff for the first column
    copy the rest
    '''
    ret = np.array(d)
    ret[:-1, 0] = ret[1:, 0] - ret[:-1, 0]
    ret[:-1, 1:] = ret[1:, 1:]
    ret = ret[:-1]
    return ret
def genByTime(data: np.array, totalTime: float, dur: int):
    '''
    generate [time, any...]
    '''
    curT = 0.0
    gen = []
    while curT < totalTime:
        idx = np.random.randint(0, data.shape[0])
        burst = min(data.shape[0] - idx, np.random.randint(dur))
        for j in range(idx, idx + burst):
            if curT >= totalTime:
                break
            else:
                gen.append([curT, *data[j, 1:]])
                curT += data[j, 0]
    return np.array(gen)
def generateBackground(dur: int, totalTime: float, num: int):
    data = []
    for p in (Path('..')/'datasets'/'background_traffic_traces').glob('*.csv'):
        d = np.loadtxt(str(p), dtype=np.float32, delimiter=',')
        data.extend(diff(d))
    data = np.array(data)
    
    dir = Path('hidden')/'background_traffic_traces'
    dir.mkdir(exist_ok=True, parents=True)

    for i in range(num):
        gen = genByTime(data, totalTime, dur)
        gen = np.array(gen)
        np.savetxt(dir/f'{i}.csv', gen, fmt='%.4f', delimiter=',')

def generateScenarios(dur: int, totalTime: float, num: int):
    '''
    simple_emulator/objects/applicaiton.py/create_blok_by_csv

     if "video" in csv_file:
                priority = 2
            elif "audio" in csv_file:
                priority = 1
            if "priority-" in csv_file:
                priority = int(csv_file[int(csv_file.index("priority-") + len("priority-"))])
    '''
    # priority mode
    dataPri = [[], [], []]
    files = [
        # 0
        [Path('..')/'datasets'/'scenario_1'/'blocks'/'block-priority-0.csv',
        Path('..')/'datasets'/'scenario_3'/'blocks'/'block-priority-0-ddl-0.15-.csv'],
        # 1
        [Path('..')/'datasets'/'scenario_1'/'blocks'/'block-priority-1.csv',
        Path('..')/'datasets'/'scenario_2'/'blocks'/'block_audio.csv',
        Path('..')/'datasets'/'scenario_3'/'blocks'/'block-priority-1-ddl-0.5-.csv'
        ],
        # 2
        [Path('..')/'datasets'/'scenario_1'/'blocks'/'block-priority-2.csv',
        Path('..')/'datasets'/'scenario_2'/'blocks'/'block_video.csv',
        Path('..')/'datasets'/'scenario_3'/'blocks'/'block-priority-2-ddl-0.2-.csv'
        ],
    ]
    for i in range(len(files)):
        for j in files[i]:
            d = np.loadtxt(str(j), dtype=np.float32, delimiter=',')
            dataPri[i].extend(diff(d))
    for i in range(len(dataPri)):
        dataPri[i] = np.array(dataPri[i])

    # networks
    dataNw = []
    for p in (Path('..')/'datasets').rglob('traces*.txt'):
        d = np.loadtxt(str(p), dtype=np.float32, delimiter=',')
        dataNw.extend(diff(d))
    dataNw = np.array(dataNw)

    for i in range(num):
        dir = Path('hidden')/f'scenario_{i}'
        dir.mkdir(exist_ok=True, parents=True)
        bdir = dir/'blocks'
        bdir.mkdir(exist_ok=True)
        ndir = dir/'networks'
        ndir.mkdir(exist_ok=True)
        
        # block
        for j in range(len(dataPri)):
            gen = genByTime(dataPri[0], totalTime, dur)
            np.savetxt(bdir/f'block-priority-{j}.csv', gen, fmt='%.4f', delimiter=',')
        # nw
        gen = genByTime(dataNw, totalTime, dur)
        np.savetxt(str(ndir/f'traces_0.txt'), gen, fmt='%.4f', delimiter=',')


if __name__ == '__main__':
    generateBackground(5, 20.0, 5)
    generateScenarios(5, 20.0, 5)