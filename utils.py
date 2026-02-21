def truncate_img(input_img, target_img):
    inp_row, inp_col, tar_row, tar_col = len(input_img), len(input_img[0]), len(target_img), len(target_img[0])

    # Truncate row
    if inp_row > tar_row:
        diff = inp_row - tar_row
        offset_ind = int(diff / 2)
        input_img = input_img[offset_ind:(offset_ind+tar_row)]
        inp_row = tar_row # Since no. of rows has been truncated, we should update it.
    elif tar_row > inp_row:
        diff = tar_row - inp_row
        offset_ind = int(diff / 2)
        target_img = target_img[offset_ind:(offset_ind+inp_row)]
        tar_row = inp_row # Since no. of rows has been truncated, we should update it.

    # Truncate column
    if inp_col > tar_col:
        for i in range(0, inp_row):
            diff = inp_col - tar_col
            offset_ind = int(diff / 2)
            input_img[i] = input_img[i][offset_ind:(offset_ind+tar_col)]
            inp_col = tar_col
    elif tar_col > inp_col:
        for i in range(0, inp_row):
            diff = tar_col - inp_col
            offset_ind = int(diff / 2)
            target_img[i] = target_img[i][offset_ind:(offset_ind+inp_col)]
            tar_col = inp_col

    return input_img, target_img

def compress(input_img, target_img, w, h):
    inp_row, inp_col = len(input_img), len(input_img[0])
    factor_h = int(inp_row / h) # Factor to reduce by
    factor_w = int(inp_col / w) # Factor to reduce by

    input_img = input_img[0::factor_h]
    target_img = target_img[0::factor_h]

    inp_row = len(input_img) # since compressed above we need to chaneg

    for i in range(0, inp_row):
        input_img[i] = input_img[i][0::factor_w]
        target_img[i] = target_img[i][0::factor_w]

    return input_img, target_img

def get_rc(val, w):
    return val // w, val % w

def arr_in_arr(arr1, arr2):
    for i in arr2:
        if i[0] == arr1[0] and i[1] == arr1[1]:
            return 1
            
    return 0
