import os
import time
from typing import Optional, TextIO

# Cribbed mostly from chia/daemon/server.py
def create_exclusive_lock(lockfile) -> Optional[TextIO]:
    """
    Open a lockfile exclusively.
    """

    try:
        fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        f = open(fd, "w")

        f.write("lock")
    except IOError:
        return None

    return f


def with_lock(lock_filename, run):
    """
    Ensure that this process and this thread is the only one operating on the
    resource associated with lock_filename systemwide.
    """

    lock_file = None
    while True:
        lock_file = create_exclusive_lock(lock_filename)
        if lock_file is not None:
            break

        time.sleep(0.1)

    try:
        run()
    finally:
        lock_file.close()
        os.remove(lock_filename)
