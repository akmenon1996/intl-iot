import os
import math
from multiprocessing import Process

src = "/Users/abhijit/Desktop/test_split/data"
dest = "/Users/abhijit/Desktop/test_split/results"
num_proc = 8
time_window = 30
slide_int = 5

if not os.path.isdir(dest):
    os.system("mkdir -pv %s" % dest)

def run(pid, files):
    for fname in files:
        print("P%s: IN: %s/%s" % (pid, src, fname))

        times = []
        fpath = src + "/" + fname
        with open(fpath, "r") as f:
            lines = f.readlines()
            times = [ float(l.split("\t")[1]) for l in lines ]

        start_int = times[0]
        end_int = start_int + time_window
        last_poss_start = math.ceil((times[len(times) - 1] - time_window) / slide_int) * slide_int
        start_idxes = [0]
        idx = 0
        num = 0
        last_bucket = False
        for t in times:
            while t - start_int >= slide_int and not last_bucket:
                if t > last_poss_start and last_poss_start - start_int < slide_int:
                    last_bucket = True

                start_int += slide_int
                start_idxes.append(idx)
            num_pop = 0
            for i in start_idxes:
                if t > end_int:
                    dest_file = "%s/%s_part_%d.txt" % (dest, fname[:-4], num)
                    print("P%s: OUT: %s" % (pid, dest_file))
                    os.system("sed -n \"%d,%dp\" %s > %s"
                              % (i + 1, idx, fpath, dest_file))
                    num_pop += 1
                    num += 1
                    end_int += slide_int

            [ start_idxes.pop(0) for _ in range(num_pop) ]
            idx += 1
        while len(start_idxes) > 0:
            dest_file = "%s/%s_part_%d.txt" % (dest, fname[:-4], num)
            print("P%s: OUT: %s" % (pid, dest_file))
            os.system("sed -n \"%d,%dp\" %s > %s"
                      % (start_idxes[0] + 1, idx, fpath, dest_file))
            start_idxes.pop(0)
            num += 1

######

files = [ [] for _ in range(num_proc) ]

index = 0
for fname in os.listdir(src):
    files[index].append(fname)
    index += 1
    if index >= num_proc:
        index = 0

procs = []
for pid, files in enumerate(files):
    p = Process(target=run, args=(pid, files))
    procs.append(p)
    p.start()
