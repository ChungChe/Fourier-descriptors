import os
import golden
import cv2

def compare():
    file_path = os.path.expanduser('test')
    print(file_path)
    err_count = 0
    for file_name in sorted(os.listdir(file_path)):
        full_file_name = "{}/{}".format(file_path, file_name)
        if not os.path.exists(full_file_name):
            print("{} not exists".format(full_file_name))
            continue
        print("checking file_name: {}".format(file_name))
        v = extact_contours(full_file_name)
        if file_name.split('.')[0].split('_')[0] == "None":
            if v == None:
                continue
            else:
                print("Value mismatch for {}, value should be {}, not {}".format(file_name, "None", v))
                err_count += 1
                continue
        golden_val = int(file_name.split('.')[0].split('_')[0])
        if v != None and int(v) != golden_val:
            print("Value mismatch for {}, value should be {}, not {}".format(file_name, golden_val, v))
            err_count += 1
    if err_count == 0:
        print("regression: PASS")
    else:
        print("regression: FAIL ({})".format(err_count))

        #print("Value : {}".format(v))
def extact_contours(file_name):
    im = cv2.imread(file_name)
    return golden.identify_number(im)
if __name__ == "__main__":
    compare()
