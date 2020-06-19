import cython

@cython.boundscheck(False)
cpdef unsigned char[:, :, :] draw_many_pixels(
        unsigned char[:, :, :] image,
        unsigned char[:, :, :] colors,
        unsigned char[:, :] locations,
        int scale):

    cdef int i, x, y, x_s, y_s, c

    for i in range(colors[0].shape[0]):
        x = locations[i][0]
        y = locations[i][1]

        for c in range(3):
            for x_s in range(scale):
                for y_s in range(scale):
                    image[y * scale + y_s, x * scale + x_s, c] = colors[0, i, c]

    return image
