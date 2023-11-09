import sys
import time

create_id = order = None
now_time = [1, 2, 3]
parcel_object = {
    "length": None, 
    "width": None, 
    "height": None,
    "weight": None,
    "completed": False,
    "barcode": None, "time": None, "id": create_id, "serve": None,
    "pic": {
        "path": None, 
        "scan_path": None, 
        "yolo_save_path": "D:/nextsls/photo/default/", 
        "lw_h_path": f"D:/nextsls/temp/photo/{now_time[0]}/{now_time[1]}/{now_time[2]}/", 
        }, 
    "status": 2,
    "order": order,
    "lw_source_arr": None,
    "lw_origin_res": None,
    "h_source_arr": None,
    "h_origin_res": None,
    "lw_method": False,
    "h_method": False,
    "pulse_length": None,
    "cm_cv_pix": False,
    "cm_mult": False,
    "check_barcode": True,
    "pic_wait_count": 1,
    "pic_wait_time": int(time.time()),
    "info": ""
}

class Parcel:

    def __init__(self, parcel_object):

        # sys.web
        # return parcel_object
        pass

    def run(self, parcel_object):
        return parcel_object

if __name__ == "main":

    parcel = Parcel()
    print(parcel.run())