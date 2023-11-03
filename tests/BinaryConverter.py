import csv

# by default, the bit depth is 2BPP...
# but you can configure it to 4BPP for example
def csv2bin(path, bpp = 2):
    
    h = ''
    data = []

    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for l in reader:
            for i in l:
                data.append(int(i))

    # loop through each number in the array / 2
    for pixel in range(int(len(data) / 2)):

        # no error checking rn - check it later, this is for testing
        total = (data[pixel * 2] * pow(2, bpp)) + data[pixel * 2 + 1]
        h += hex(total)[2:]
    
    # create a byte array from the hex string
    b = bytes.fromhex(h)

    # DEBUG
    # output all the bytes we are writing -- useful for debugging
    print('Output Bytes: ', end='')
    for byte in b:
        print(hex(byte) + ' ', end='')
    print(end='\n')

    # return the bytes array
    return b

bytes_to_write = csv2bin('tests/pixels.csv')

with open('tests/binary.bin', 'wb') as file:
    file.write(bytes_to_write)
