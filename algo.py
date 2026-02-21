import math

from utils import get_rc

MAX_DIFF_LEN = math.sqrt((255 ** 2) * 3)

# Two pixels are considered as vectors in RGB vector space and closeness is determined by the distance between the two vectors
def cmp_pxls(pxl1, pxl2):
    # To avoid overflow errors because by default they are only 8bits
    pxl1 = [int(x) for x in pxl1]
    pxl2 = [int(x) for x in pxl2]

    pxl_diff = [abs(pxl1[0] - pxl2[0]), abs(pxl1[1] - pxl2[1]), abs(pxl1[2] - pxl2[2])]
    # Vector len -> sqrt of sum of squares of the components
    pxl_diff_len = math.sqrt((pxl_diff[0] ** 2 + pxl_diff[1] ** 2 + pxl_diff[2] ** 2))
    norm_len = pxl_diff_len / MAX_DIFF_LEN
    return 1 - norm_len # 1 indicates same pixel, 0.99 indicates almost same and so on. 

# Try: Algo 1
def rearrange(input_img, target_img, rad):
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
        taken[index[0] * w + index[1]] = 1
        output_img[r][c] = input_img[index[0]][index[1]]

    return output_img
