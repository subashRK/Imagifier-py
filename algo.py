from utils import get_rc

# Square root takes processing time, so squares are compared directly
MAX_DIFF_LEN = (255 ** 2) * 3

# Two pixels are considered as vectors in RGB vector space and closeness is determined by the distance between the two vectors
def cmp_pxls(pxl1, pxl2):
    # To avoid overflow errors because by default they are only 8bits
    pxl1 = [int(x) for x in pxl1]
    pxl2 = [int(x) for x in pxl2]

    pxl_diff = [abs(pxl1[0] - pxl2[0]), abs(pxl1[1] - pxl2[1]), abs(pxl1[2] - pxl2[2])]
    # Vector len -> sqrt of sum of squares of the components, since sqrt takes time, vals are compared directly
    pxl_diff_len = (pxl_diff[0] ** 2 + pxl_diff[1] ** 2 + pxl_diff[2] ** 2)
    norm_len = pxl_diff_len / MAX_DIFF_LEN
    return 1 - norm_len # 1 indicates same pixel, 0.99 indicates almost same and so on. 


# Test
pix_count = {}
o_pix_count = {}

def calculate_freq(output_img, tot_pix, w):
    for i in range(0, tot_pix):
        r, c = get_rc(i, w)
        o_pix_count[str(output_img[r][c][0]) + str(output_img[r][c][1]) + str(output_img[r][c][2])] = o_pix_count.get(str(output_img[r][c][0]) + str(output_img[r][c][1]) + str(output_img[r][c][2]), 0) + 1

#test end

# Try: Algo 1
def first_fit(input_img, target_img, rad):
    h = len(target_img)
    w = len(target_img[0])
    output_img = [[[] for j in range(0, w)] for i in range(0, h)]
    rad_pxls_h = int(h * rad)
    rad_pxls_w = int(w * rad)
    tot_pix = w * h
    taken = [0 for i in range(0, tot_pix)]
    count = 0

    for i in range(0, tot_pix):
        r, c = get_rc(i, w)

        closest = 0
        index = [0, 0]

        for j in range(max([0, r - (rad_pxls_h // 2)]), min([h, r + (rad_pxls_h // 2)])):
            for k in range(max([0, c - (rad_pxls_w // 2)]), min([w, c + (rad_pxls_w // 2)])):
                if (taken[j * w + k] == 1):
                    continue
                
                closeness = cmp_pxls(input_img[j][k], target_img[r][c])

                if (closeness > closest):
                    closest = closeness
                    index[0] = j
                    index[1] = k

        count += 1
        print(f"Processing: {((count / tot_pix) * 100):.2f}% completed")
        #test start
        pix_count[str(input_img[r][c][0]) + str(input_img[r][c][1]) + str(input_img[r][c][2])] = pix_count.get(str(input_img[r][c][0]) + str(input_img[r][c][1]) + str(input_img[r][c][2]), 0) + 1
        taken[index[0] * w + index[1]] = 1
        output_img[r][c] = input_img[index[0]][index[1]]

    calculate_freq(output_img, tot_pix, w)

    count = 0


    for i in pix_count.keys():
        if pix_count[i] != o_pix_count.get(i, 0):
            count += 1
            print("Mismatch!", pix_count[i], o_pix_count.get(i, 0))

    print("no of mismatch", count)
#test end
    return output_img

# Try: Algo 2 (Best fit rather than first fit)
def best_fit(input_img, target_img, rad):
    h = len(target_img)
    w = len(target_img[0])
    output_img = [[[0, 0, 0] for j in range(0, w)] for i in range(0, h)]
    rad_pxls_h = int(h * rad)
    rad_pxls_w = int(w * rad)
    tot_pix = w * h
    taken = [0 for i in range(0, tot_pix)]
    taken_by = [0 for i in range(0, tot_pix)]
    closeness_arr = [0 for i in range(0, tot_pix)] # stores the closeness value of the matched pixels, corresponds to target images
    count = 0

    def check(i):
        nonlocal count, output_img, taken, taken_by, closeness_arr
        r, c = get_rc(i, w)

        closeness = closest = 0
        index = [0, 0]

        for j in range(max([0, r - (rad_pxls_h // 2)]), min([h, r + (rad_pxls_h // 2)])):
            for k in range(max([0, c - (rad_pxls_w // 2)]), min([w, c + (rad_pxls_w // 2)])):
                closeness = cmp_pxls(input_img[j][k], target_img[r][c])

                nr, nc = get_rc(taken_by[j * w + k], w)

                if taken[j * w + k] == 1 and closeness <= closeness_arr[nr * w + nc]:
                    # print("continue", i, nr * w + nc)
                    continue

                if (closeness > closest):
                    closest = closeness
                    index[0] = j
                    index[1] = k

        nr, nc = get_rc(taken_by[index[0] * w + index[1]], w)

        if closest != 0 and taken[index[0] * w + index[1]] == 1 and closest > closeness_arr[nr * w + nc]:
            old_i = taken_by[index[0] * w + index[1]]
            taken_by[index[0] * w + index[1]] = i
            # print("rec", old_i, i, closeness_arr[nr * w + nc], closest)
            closeness_arr[i] = closest
            check(old_i)
        else:
            count += 1

        if index[0] != None:
            print(f"Processing: {((count / tot_pix) * 100):.2f}% completed")
            taken[index[0] * w + index[1]] = 1
            taken_by[index[0] * w + index[1]] = i
            closeness_arr[i] = closest
            output_img[r][c] = input_img[index[0]][index[1]]

    for i in range(0, tot_pix):
        #test start
        r, c = get_rc(i, w)
        pix_count[str(input_img[r][c][0]) + str(input_img[r][c][1]) + str(input_img[r][c][2])] = pix_count.get(str(input_img[r][c][0]) + str(input_img[r][c][1]) + str(input_img[r][c][2]), 0) + 1
        # test end
        check(i)

    #test start
    calculate_freq(output_img, tot_pix, w)

    count = 0


    for i in pix_count.keys():

        if pix_count[i] != o_pix_count.get(i, 0):
            count += 1
            print("Mismatch!")

    print("no of mismatch", count)
    #test end

    return output_img
