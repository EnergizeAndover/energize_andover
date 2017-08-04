from NAEInteract1 import main, findNAE, close
import sched, time

def pull_data():
    findNAE()
    s = sched.scheduler(time.time, time.sleep)
    try:
        while(True):
            s.enter(10, 1, main, ())
            s.run()
    except:
        close()
pull_data()