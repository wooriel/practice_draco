import os
from os import walk
import tqdm
import argparse
import numpy
import DracoPy
import open3d as o3d


#preprocess one ply file
def genPath(fp, dp, sn=''):
    srcpath = os.path.join(os.getcwd(), fp)
    despath = os.path.join(os.getcwd(), dp)
    os.makedirs(despath, exist_ok=True)
    print(srcpath)
    print(despath)

    files = []
    for dirpath, dirnames, filenames in walk(srcpath):
        files.extend(filenames)
    
    #compress each objects
    for file in files:
        # get object file extension
        extension = file[-4:].lower()
        if extension == '.ply':
            fname = os.path.join(srcpath, file)
            pointcl= readPly(fname)
        binary = DracoPy.encode()

def readPly(filename):
    # read into ply
    pcl = o3d.io.read_point_cloud(filename)
    print(pcl)
    return pcl

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='compress a pointcloud')
    # when argument is required, input without the variable name (fpath -> input fpath content)
    parser.add_argument('-fpath', default='/data', help='file path to the pointcloud(s)')
    parser.add_argument('-dpath', default='/data_c', help='destination file path for the compressed pointcloud(s)')
    parser.add_argument('-sname', help='shared name for compressed obj')

    args = parser.parse_args()
    print(args.fpath)
    print(args.dpath) #destination path