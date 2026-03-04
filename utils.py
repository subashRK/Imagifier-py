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

def compress(input_img, target_img, factor):
    inp_row = len(input_img)

    input_img = input_img[0::factor]
    target_img = target_img[0::factor]

    inp_row = len(input_img) # since compressed above we need to change

    for i in range(0, inp_row):
        input_img[i] = input_img[i][0::factor]
        target_img[i] = target_img[i][0::factor]

    return input_img, target_img

def get_rc(val, w):
    return val // w, val % w
