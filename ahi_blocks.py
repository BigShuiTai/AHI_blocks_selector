import argparse

global BZIP_FILE

def get_block_paths(ahi_blocks, upper, lower):
    blocks_id = []
    for i, ahi_block in enumerate(ahi_blocks, start=1):
        block_dummy, block_upper, block_lower = ahi_block.split(' ')
        del block_dummy
        block_upper, block_lower = float(block_upper), float(block_lower)
        if upper <= block_upper and upper >= block_lower and i not in blocks_id:
            blocks_id.append(i)
        if lower <= block_upper and lower >= block_lower and i not in blocks_id:
            blocks_id.append(i)
    selected_blocks = ['S%02d10' % bid for bid in range(min(blocks_id), max(blocks_id) + 1)]
    return selected_blocks

def search_blocks_from_files(files, lat, latspan):
    # get block areas
    with open('ahi_blocks.txt', 'r') as f:
        ahi_blocks = f.read().split('\n')
    upper, lower = (lat + latspan, lat - latspan)
    selected_blocks = get_block_paths(ahi_blocks, upper, lower)
    selected_files = []
    for block in selected_blocks:
        for file in files:
            if block in file:
                selected_files.append(file)
    return selected_files

def search_blocks_from_format(args):
    if int(args.band) == 3:
        res = '05'
    elif int(args.band) in range(5, 17):
        res = '20'
    else:
        res = '10'
    # get block areas
    with open('ahi_blocks.txt', 'r') as f:
        ahi_blocks = f.read().split('\n')
    upper, lower = (
        args.latitude + args.latitude_span, 
        args.latitude - args.latitude_span
    )
    selected_blocks = get_block_paths(ahi_blocks, upper, lower)
    for i, s in enumerate(selected_blocks):
        if BZIP_FILE:
            selected_blocks[i] = f'HS_H{"%02d" % args.ahi_sat_id}_{args.time[:-4]}_{args.time[-4:]}_B{args.band}_FLDK_R{res}_{s}.DAT.bz2'
        else:
            selected_blocks[i] = f'HS_H{"%02d" % args.ahi_sat_id}_{args.time[:-4]}_{args.time[-4:]}_B{args.band}_FLDK_R{res}_{s}.DAT'
    return selected_blocks

if __name__ == '__main__':
    # set arguments
    parser = argparse.ArgumentParser(description='AHI Blocks')
    parser.add_argument('-id', '--ahi_sat_id', default=9, type=int)
    parser.add_argument('-t', '--time', default='', type=str)
    parser.add_argument('-b', '--band', default='13', type=str)
    parser.add_argument('-lat', '--latitude', default=0, type=float)
    parser.add_argument('-latspan', '--latitude_span', default=5, type=float)
    parser.add_argument('-z', '--bzip', default=0, type=int)
    args = parser.parse_args()
    BZIP_FILE = (args.bzip == 0)
    selected_blocks = search_blocks_from_format(args)
    print(' '.join(selected_blocks))
