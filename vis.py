from matplotlib import pyplot as plt
import cv2

def plot_split_images(orig_img_mask_arr, patch_arr_list, orig_filename):

    """
    uses plt.figure and grid.spec to plot our orginal image/mask and its corresponding patches
    not sure why our orig img/mask isn't taking up all columns
    :param orig_img_mask: the original image or mask
    :param patches_list: our patches
    :return:
    """

    num_patches = len(patch_arr_list)
    fig = plt.figure(figsize=(10,10))
    rows = 2
    columns = num_patches
    axs = []
    gs = fig.add_gridspec(rows, columns)

    #plotting orginal image/mask
    axs.append(fig.add_subplot(gs[0, :columns]))  # large subplot (2 rows, 2 columns)
    orig_img_mask_arr=cv2.cvtColor(orig_img_mask_arr, cv2.COLOR_BGR2RGB)
    plt.imshow(orig_img_mask_arr)
    plt.title(orig_filename)
    plt.xticks([])
    plt.yticks([])

    for i in range(columns):
        axs.append(fig.add_subplot(gs[1, i]))  # small subplot (1st row, 3rd column)
        plt.imshow(patch_arr_list[i])
        plt.title(f'No.{i}')
        # plt.xticks([])
        # plt.yticks([])
    plt.show()
