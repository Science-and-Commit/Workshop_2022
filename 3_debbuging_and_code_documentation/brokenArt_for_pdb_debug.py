"""
Warning: This code is broken.
"""

import numpy as np
import matplotlib.pylab as plt

# make a random image
np.random.seed(99999)

# for each row, we will draw numbers from increasingly large pools of random numbers
new_image = []

dim1 = 25
dim2 = 7

for i in range(dim1):
    # draw random integers between 0 and 10*(i+1), no repeats!
    this_row = []
    for j in range(dim2):
        new_number = np.random.randint(0, 10*(i+1))
        if new_number not in this_row:
            this_row.append(new_number)

    # add this row to the image we are creating
    new_image.append(this_row)

new_image = np.array(new_image)

# now let's check how many of each number we generated
counts = {} # dictionary of counts per value
for i in range(dim1):
    for j in range(dim2):
        value = new_image[i, j]
        if value in counts:
            counts[value] += 1
        else:
            counts[value] = 0

print(counts)

# plot the resulting image. 
plt.figure()
plt.imshow(new_image, cmap="RdBu")
plt.gca().invert_yaxis()
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.title("Art")
plt.show()
