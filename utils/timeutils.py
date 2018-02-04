import time

last_time = {}
def log_time_elps(tid, msg):
	if tid in last_time:
		t = last_time[tid]
		now = time.time()
		print("[%.3f]\t%s" % (now - t, msg))
		last_time[tid] = now
	else:
		print("Start %s\t%s" % (str(tid),msg))
		last_time[tid] = time.time()
def restart_time_elps(tid):
	last_time[tid] = time.time()
