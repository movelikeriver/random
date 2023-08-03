import csv
import json
import sys


def get_index(col_list, col):
    idx = col_list.index(col)
    if idx >= 0:
        return idx
    print(f"can not find {col}")
    return -1


def parse_reject_reason(input):
    ret = []
    input = input.strip()[1:-1]

    while True:
        ee = len(input)
        idx1 = input.rfind(':', 0, ee)
        idx2 = input.rfind(' ', 0, idx1)
        ret.append(input[idx2+1 : ee].strip(','))
        if idx2 < 0:
            break
        input = input[:idx2]

    return ret


# list_map[rejection] = {elem_id, elem_id, ...}
def get_top_cnt(list_map, total_size):
    m = {}
    for reject_reason in list_map:
        m[reject_reason] = len(list_map[reject_reason])

    tp_list = [(x[0], x[1], float(x[1])/float(total_size)) for x in m.items()]
    return sorted(tp_list, key=lambda x : x[1], reverse=True)


def test_parse_reject_reason():
    arr = parse_reject_reason('[103615:Prohibited Industry - Medical Institutions, Devices and Services, 100125:Prohibited Industry]')
    print(arr)


#####################
# validate functions

def validate_with_all(row, header):
    return True


def validate_with_appeal_conversation(row, header):
    idx2 = get_index(header, 'appeal_detail')

    if row[idx2] == 'NULL':
        return False

    return True


def parse_appeal_conversation(row, header):
    idx = get_index(header, 'appeal_detail')

    if row[idx] == 'NULL':
        return []

    return json.loads(row[idx])


def handle_detailed_conv(row, header):
    idx = get_index(header, 'appeal_detail')

    if row[idx] == 'NULL':
        return []

    txt = json.loads(row[idx])[0]  ## already pre-filtered
    idx = txt.find(' A1:')
    if idx == -1:
        # print(f"=========== error =========\n {row} ")
        return False, []

    txt_q = txt[3:idx].replace('</p>', ' ').replace('<p>', ' ').strip()
    txt_a = txt[idx+4:].replace('</p>', ' ').replace('<p>', ' ').strip()
    print(f"\n=====\n{txt_q}\n=====\n{txt_a}\n=====\n")
    return True, segment(txt_a)


def segment(txt):
    arr = [x.strip() for x in txt.split(' ') if not x.strip()]
    if len(arr) <= 3:
        return [' '.join(arr)]

    ret = []
    for i in range(0, len(arr)-3):
        ret.append(' '.join([arr[i], arr[i+1], arr[i+2]]))

    return ret


def validate_with_overturn(row, header):
    idx1 = get_index(header, 'is_overturn')

    if row[idx1] != '1':
        return False

    return True


def stats_reject_reason(filename, validate_fn, top_k=50):
    reject_reason_adv_map = {}
    reject_reason_ad_map = {}
    adv_map = {}
    ad_map = {}

    with open(adg_fn) as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        header = []
        for row in r:
            if not header:
                header = row
                idx1 = get_index(header, 'ad_id')
                idx2 = get_index(header, 'advertiser_id')
                idx3 = get_index(header, 'reject_reason')
                continue

            if not validate_fn(row, header):
                # filter out invalid rows
                continue

            ad_id = row[idx1]
            adv_id = row[idx2]
            reject_reason = row[idx3]
            arr = parse_reject_reason(reject_reason)
            for elem in arr:
                elem = elem.strip()

                # ad
                if elem not in reject_reason_ad_map:
                    reject_reason_ad_map[elem] = {}
                reject_reason_ad_map[elem][ad_id] = True
                ad_map[ad_id] = True

                # adv
                if elem not in reject_reason_adv_map:
                    reject_reason_adv_map[elem] = {}
                reject_reason_adv_map[elem][adv_id] = True
                adv_map[adv_id] = True

    s = len(ad_map)
    arr = get_top_cnt(reject_reason_ad_map, s)
    print(f"\n=== reject_reason sorted by num of ads, total {s} ===")
    for elem in arr[:top_k]:
        print(elem)

    s = len(adv_map)
    arr = get_top_cnt(reject_reason_adv_map, s)
    print(f"\n=== reject_reason sorted by num of adv, total {s} ===")
    for elem in arr[:top_k]:
        print(elem)


def sample_rows(filename, total_sample):
    cnt_all = 0
    cnt = 0

    seg_map = {}

    with open(adg_fn) as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        header = []
        for row in r:
            if not header:
                header = row
                idx1 = get_index(header, 'ad_id')
                idx2 = get_index(header, 'advertiser_id')
                idx3 = get_index(header, 'reject_reason')
                idx4 = get_index(header, 'appeal_detail')
                idx5 = get_index(header, 'is_overturn')

                continue

            cnt_all += 1

            if row[idx4] == 'NULL':
                # appeal_detail
                continue

            arr = parse_appeal_conversation(row, header)
            if len(arr) > 1:
                continue

            is_overturn = row[idx5] == '1'

            success, ret = handle_detailed_conv(row, header)
            if success:
                for elem in ret:
                    if elem not in seg_map:
                        seg_map[elem] = [0, 0]
                    if is_overturn:
                        seg_map[elem][0] += 1
                    else:
                        seg_map[elem][1] += 1

            # if cnt < total_sample:
            #    print(row)
            cnt += 1

    seg_list = seg_map.items()
    seg_list = sorted(seg_list, key=lambda x : x[1][0] - 3 * x[1][1], reverse=True)
    for elem in seg_list[:100]:
        print(f"{elem[0]}, {elem[1][0]}, {elem[1][0]/cnt}, {elem[1][1]}, {elem[1][1]/cnt}")

    print(f"{cnt} out of {cnt_all} are eligible!")


#######
# main


adg_fn = sys.argv[1]


print('\n\nvalidate_with_all')
stats_reject_reason(adg_fn, validate_with_all, top_k=50)

print('\n\nvalidate_with_appeal_conversation')
stats_reject_reason(adg_fn, validate_with_appeal_conversation, top_k=50)

print('\n\nvalidate_with_overturn')
stats_reject_reason(adg_fn, validate_with_overturn, top_k=50)

# sample rows
sample_rows(adg_fn, total_sample=100)
