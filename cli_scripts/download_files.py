#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 10:09:13 2018

@author: evenhuis, moisbo
"""
# from Parse_OMERO_Properties import datasetId, imageId, plateId

import sys
import argparse
import os
import omero
from omero.gateway import BlitzGateway
from Parse_OMERO_Properties import USERNAME, PASSWORD, HOST, PORT


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def download_dataset(Id, path, orig=False, tif=False):
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    download a dataset from OMERO
        INPUT : conn, the connection needs to be open
        Id    : ID of the dataset
        path  : location of local filesystem
        fmt   : "o" is original , "t" is tiff
    """

    # get the data set
    dataset = conn.getObject('Dataset', Id)
    if (dataset == None):
        print("Dataset ID {} not found in group".format(Id))
        sys.exit(1)

    # get the images
    imgs = list(dataset.listChildren())

    # this is the directory to place the data in
    ds_name = dataset.getName()
    print("{}/".format(ds_name))
    reldir = os.path.join(path, ds_name)
    if (not os.path.isdir(reldir)):
        os.makedirs(reldir)

    for img in imgs:
        print(" " * len(ds_name) + "/{}".format(img.getName()))

        if (orig):
            for orig in img.getImportedImageFiles():
                name = orig.getName()
                file_path = os.path.join(reldir, name)

                if (not os.path.exists(file_path)):
                    with open(str(file_path), 'w') as f:
                        for chunk in orig.getFileInChunks():
                            f.write(chunk)

        if (tif):
            name = os.path.basename(img.getName()) + ".ome.tif"
            file_path = os.path.join(reldir, name)
            file_size, block_gen = img.exportOmeTiff(bufsize=65536)
            with open(str(file_path), "wb") as f:
                for piece in block_gen:
                    f.write(piece)

    return


def main():

    try:
        conn.connect()

        user = conn.getUser()
        print "Current user:"
        print "   ID:", user.getId()
        print "   Username:", user.getName()
        print "   Full Name:", user.getFullName()

        if args.group is not None:
            print("change group")
            new_group = args.group
            groups = [g.getName() for g in conn.listGroups()]
            print(groups)
            if new_group not in groups:
                print("{} not found in groups:".format(new_group))
                for gn in groups:
                    print("    {}".format(gn))
                conn.close()
                sys.exit(1)
            else:
                conn.setGroupNameForSession(new_group)

        print(args.dataset)
        for d_id in args.dataset:
            download_dataset(d_id, path, orig=args.orig, tif=args.tif)

        print(args.project)
        for p_id in args.project:
            project = conn.getObject('Project', p_id)
            path_p = os.path.join(path, project.getName())
            if project is None:
                print("project ID {} not found in group {}".format(p_id, orig=args.orig, tif=args.tif))
                conn.close()
                sys.exit(1)

            for ds in list(project.listChildren()):
                download_dataset(ds.getId(), path_p, orig=args.orig, tif=args.tif)

        conn.close()

    except Exception as e:
        print "cannot connect: ", e
        sys.exit(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download datasets and projects from OMERO')
    parser.add_argument('-p', '--project', nargs="+", default=[], help="IDs of projects to download")
    parser.add_argument('-d', '--dataset', nargs="+", default=[], help="IDs of datasets to download")
    parser.add_argument('-g', '--group', nargs="?", help="name of group")
    parser.add_argument('-o', '--orig', action="store_true", default=False, help="download originals")
    parser.add_argument('-t', '--tif', action="store_true", default=False, help="download OME-TIFs")
    parser.add_argument('-f', '--files', default="/tmp/downloads", help="location of the downloads folder")
    args = parser.parse_args()

    download_path = args.files
    if os.path.isdir(download_path) and os.path.exists(download_path):
        print "writing output to ", download_path
    else:
        print "cannot find ", download_path
        sys.exit(1)

    conn = BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT)

    path = download_path

    main()
