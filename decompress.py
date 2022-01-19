import os
from os import walk
from tqdm import tqdm
import argparse
import numpy
import DracoPy
import open3d as o3d
import logging


def decompress(sp, dp, sn=None, ext='.ply'):
    
    files = []
    for dirpath, dirnames, filenames in walk(sp):
        files = [x for x in filenames if not x.startswith('log')]

    # print(files)

    #compress each objects
    LOG.info('Start conversion')
    for file in tqdm(files):
        sn = file[:-4]
        fname = os.path.join(sp, file)
        print(fname)
        binary = readDrc(fname)
        if ext == '.ply':
            desname = "".join([sn, ext])
            desfile = os.path.join(dp, desname)
            writePly(desfile, binary)
        LOG.info('Saved {0}'.format(desfile))
    LOG.info('Finished conversion')

def readDrc(filename):
    f = open(filename, 'rb')
    contents = f.read()
    f.close()
    return contents


def writePly(filename, contents):
    # convert into ply
    rpoints = DracoPy.decode(contents)
    print(type(rpoints.points))
    print('number of points: {}'.format(len(rpoints.points)))
    pcl = o3d.geometry.PointCloud()
    pcl.points = o3d.utility.Vector3dVector(rpoints.points)
    o3d.io.write_point_cloud(filename, pcl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='decompress pointclouds')
    parser.add_argument('-spath', default='data/draco', help='source file path to the draco file(s)')
    parser.add_argument('-dpath', default='data/pcl', help='destination file path to the pointcloud(s)')
    parser.add_argument('-sname', help='shared name for compressed obj')

    args = parser.parse_args()

    srcpath = os.path.join(os.getcwd(), args.spath)
    despath = os.path.join(os.getcwd(), args.dpath)
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
        # print(logfname)
    logpath = os.path.join(despath, logfname)
    LOG = logging.getLogger('compress')
    LOG.handlers = []
    LOG.setLevel(logging.INFO)
    fhandler = logging.FileHandler(logpath)
    LOG.addHandler(fhandler)

    decompress(srcpath, despath, args.sname)