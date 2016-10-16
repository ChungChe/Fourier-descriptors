import threading
import os

def copy_and_sync_to_cloud():
    threading.Timer(600, copy_and_sync_to_cloud).start()
    # copy file
    cp_cmd = "cp -fr /home/duntex/Fourier-descriptors/curve.db /home/duntex/CurveGoGo/app/curve.db"
    os.system(cp_cmd)
    # sync to remote
    sync_cmd = "rclone sync /home/duntex/CurveGoGo/app/curve.db remote:/db"
    os.system(sync_cmd)
def copy_from_cloud():
    threading.Timer(600, copy_from_cloud).start()
    # sync from remote
    sync_cmd = "/Users/duntex/rclone129/rclone sync remote:/db/curve.db /Users/duntex/curve/app/curve.db"
    os.system(sync_cmd)

copy_and_sync_to_cloud()
