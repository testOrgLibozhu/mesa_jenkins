#!/usr/bin/python

"""Measures performance of apitrace files"""

import csv
import datetime
import json
import os
from urllib import urlretrieve
from . import Options, run_batch_command, ProjectMap, RevisionSpecification

class ApiTracePerf(object):
    """builder for apitrace performance measurements"""
    def __init__(self, config_file):
        self.p_map = ProjectMap()
        self.opt = Options()
        config_path = self.p_map.project_build_dir() + "/" + config_file
        self.conf = json.load(open(config_path))

    def build(self):
        """downloads the trace file if necessary"""
        local_file = self.conf["file"]
        if not os.path.exists(local_file):
            dirname = os.path.split(local_file)[0]
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            urlretrieve(self.conf["url"], local_file)

    def clean(self):
        """no artifacts are left by this test"""
        pass

    def test(self):
        """call framestat, process output into a score"""
        iterations = self.conf["iterations"]
        frames = self.conf["frames"]
        build_root = self.p_map.build_root()
        hardware = self.opt.hardware
        framestat = build_root + "/bin/framestat"
        current_project = self.p_map.current_project()
        out_dir = build_root + "/scores/" + current_project + "/" + hardware
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_path = out_dir + "/" + current_project + "_" + hardware + "_trace.csv"
        cmd = [framestat, "-n", str(iterations),
               "-o", out_path,
               "-f", self.conf["file"]]
        cmd += [str(n) for n in frames]
        perf_prefix = build_root + "/" + hardware + "/usr/local/lib"
        env = {"LD_LIBRARY_PATH" : perf_prefix,
               "LIBGL_DRIVERS_PATH" : perf_prefix + "/dri"}
        self.opt.update_env(env)

        run_batch_command(cmd, env=env)

        out_fh = open(out_path, "rb")
        out_fh.readline()  # first line is file name
        reader = csv.DictReader(out_fh, delimiter='\t')
        results = {}
        for row in reader:
            iteration = 0
            while str(iteration) in row:
                if iteration not in results:
                    results[iteration] = []
                results[iteration].append(int(row[str(iteration)]))
                iteration += 1
        revision = str(RevisionSpecification().revision("mesa"))
        result = {current_project :
                  {hardware :
                   {"mesa=" + revision :
                    [{"score" : [sum(l) / float(len(l)) for l in results.values()]}]
                   }
                  }}

        outf = out_dir + "/" + datetime.datetime.now().isoformat() + ".json"
        with open(outf, 'w') as outf:
            json.dump(result, fp=outf)
