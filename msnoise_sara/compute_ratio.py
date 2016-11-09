import time

import bottleneck as bn
from msnoise.api import *
from .api import get_sara_param

def main():
    db = connect()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('*** Starting: Compute SARA_RATIO ***')

    while is_next_job(db, jobtype='SARA_RATIO'):
        t0 = time.time()
        jobs = get_next_job(db, jobtype='SARA_RATIO')
        stations = []
        pairs = []
        refs = []

        for job in jobs:
            refs.append(job.ref)
            pairs.append(job.pair)
            netsta1, netsta2 = job.pair.split(':')
            stations.append(netsta1)
            stations.append(netsta2)
            goal_day = job.day

        stations = np.unique(stations)

        logging.info("New SARA Job: %s (%i pairs with %i stations)" %
                     (goal_day, len(pairs), len(stations)))

        logging.debug("Preloading all envelopes and applying site and sensitivity")
        all = {}
        for station in stations:
            tmp = get_sara_param(db, station)
            sensitivity = tmp.sensitivity
            site_effect = tmp.site_effect
            tmp = read(os.path.join("SARA", "ENV", station, "%s.MSEED"%goal_day))
            for trace in tmp:
                trace.data /= (sensitivity * site_effect)
            all[station] = tmp

        logging.debug("Computing all pairs")
        for job in jobs:
            netsta1, netsta2 = job.pair.split(':')
            trace = Trace()
            trace.data = all[netsta1][0].data / all[netsta2][0].data
            trace.stats.starttime = all[netsta1][0].stats.starttime
            trace.stats.delta = all[netsta1][0].stats.delta

            env_output_dir = os.path.join('SARA','RATIO', job.pair.replace(":","_"))
            if not os.path.isdir(env_output_dir):
                os.makedirs(env_output_dir)
            trace.write(os.path.join(env_output_dir, goal_day+'.MSEED'),
                        format="MSEED", encoding="FLOAT32")

            update_job(db, job.day, job.pair, 'SARA_RATIO', 'D')
        logging.info("Done. It took %.2f seconds" % (time.time()-t0))