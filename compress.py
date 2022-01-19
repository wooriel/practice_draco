import os
from os import walk
from tqdm import tqdm
import argparse
import numpy
import DracoPy
import open3d as o3d
import logging
import time


#preprocess multiple ply files in same directory
def compress(sp, dp, sn=None):

    files = []
    for dirpath, dirnames, filenames in walk(sp):
        files.extend(filenames)
    
    #compress each objects
    LOG.info('Start conversion')
    for file in tqdm(files):
        # get saving file name
        # if sn == None:
        sn = file[:-4]
        # get object file extension
        extension = file[-4:].lower()
        if extension == '.ply':
            fname = os.path.join(sp, file)
            pcl= readPly(fname)
        binary = DracoPy.encode(pcl.points)
        desname = "".join([sn, '.drc'])
        desfile = os.path.join(dp, desname)
        print(desfile)
        writeDrc(desfile, binary)
        LOG.info('Saved {0}'.format(desfile))
    LOG.info('Finished conversion')

def readPly(filename):
    # read into ply
    pcl = o3d.io.read_point_cloud(filename)
    print(type(pcl))
    return pcl


def writeDrc(filename, contents):
    # write in drc in destination file
    f = open(filename, 'wb')
    f.write(contents)
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='compress pointclouds')
    # when argument is required, input without the variable name (fpath -> input fpath content)
    parser.add_argument('-spath', default='data/gt_pcl', help='source file path to the pointcloud(s)')
    parser.add_argument('-dpath', default='data/draco', help='destination file path for the draco file(s)')
    parser.add_argument('-sname', help='shared name for compressed obj')

    args = parser.parse_args()
    srcpath = os.path.join(os.getcwd(), args.spath)
    despath = os.path.join(os.getcwd(), args.dpath)
    # make destination folder if not exist
    os.makedirs(despath, exist_ok=True)

    # logging - save in destination folder
    log = 'log'
    extension = '.txt'
    logfname = ''.join([log, extension])
    i = 0
    print(os.path.join(despath, logfname))
    while os.path.exists(os.path.join(despath, logfname)):
        i += 1
        logfname = ''.join([log, str(i), extension])
        print(logfname)
    logpath = os.path.join(despath, logfname)
    LOG = logging.getLogger('compress')
    LOG.handlers = []
    LOG.setLevel(logging.INFO)
    fhandler = logging.FileHandler(logpath)
    LOG.addHandler(fhandler)
    # logging.basicConfig(filename=logfname, filemode='w', level=logging.INFO)

    compress(srcpath, despath, args.sname)