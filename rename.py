#!/usr/bin/env python

import os
import argparse
import glob
import time
from PIL import Image

inc = 1

# Returns the image date from a jpg image file (if available)
def get_jpg_date(file):
    T = None

    # For subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    exif = Image.open(file)._getexif()
    
    if exif != None:
        for t in tags:
            dat = exif.get(t[0])
            sub = exif.get(t[1], 0)
            dat = dat[0] if type(dat) == tuple else dat
            sub = sub[0] if type(sub) == tuple else sub
            if dat != None: 
                T = dat.replace(':', '-').replace(' ', '_')
                break
    return T

def rename_file(file, methods, ext, show, file_number, collision):
    file_dir = os.path.dirname(file)
    file_name = os.path.basename(file)
    
    if ext == None:
        if file.find('.') >= 0:
            file_ext = file.split('.')[1]
        else:
            file_ext = ''
    else:
        file_ext = ext

    method_list = methods.split('+')
    new_file_name = ''
    
    for method in method_list:
        if method == 'cdate':
            str_to_add = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime(os.path.getctime(file)))
        elif method == 'mdate':
            str_to_add = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime(os.path.getmtime(file)))
        elif method == 'imgdate':
            str_to_add = get_jpg_date(file)
            if str_to_add == None:
                print('WARNING - %s does not include any image date, so the modified file date is used.' % (file))
                str_to_add = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime(os.path.getmtime(file)))
        elif method[0:3] == 'num':
            str_to_add = str(file_number)
            collision = 0       # No collision number need to be added when a file number is part of the name.
            if len(method) > 3:
                try:
                    pad = int(method[3])
                    str_to_add = str_to_add.zfill(pad)
                except:
                    pass
        elif method == 'name':
            str_to_add = file_name
        elif method == 'lname':
            str_to_add = file_name.lower()
        elif method == 'uname':
            str_to_add = file_name.upper()
        else:    
            str_to_add = method
        
        if new_file_name == '':
            new_file_name = str_to_add
        else:
            new_file_name += '_' + str_to_add

    if collision == 0:
        new_file = os.path.join(file_dir, new_file_name + '.' + file_ext)
    else:
        col_nb = 0
        col_nb_str = str(str(col_nb).zfill(collision))
        new_file = os.path.join(file_dir, new_file_name + '_' + col_nb_str + '.' + file_ext)
    
    print('%s will be renamed to %s' % (file, new_file))

    if not show:
        error = True
        
        while error:
            try:
                os.rename(file, new_file)
                error = False
            except Exception as e:
                print('ERROR - Unable to rename file (%s)' % (e))
                if collision == 0: return
                col_nb += 1
                col_nb_str = str(str(col_nb).zfill(collision))
                new_file = os.path.join(file_dir, new_file_name + '_' + col_nb_str + '.' + file_ext)
                print('%s will be renamed to %s' % (file, new_file))
    
def main():
    desc = 'CMELSoft - File rename utility that can be use to automatically rename several files in a directory'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-r', action='store_true', dest='recurse', default=False, help='rename file recursively in all directory under the specified one')
    parser.add_argument('-c', action='store', dest='collision', type=int, default=0, help='add a rename collision number with the specified number of digit (no collision number is added by default)')
    parser.add_argument('-s', action='store_true', dest='show', default=False, help='show the new file name that will be used without renaming any files')
    parser.add_argument('-e', action='store', dest='ext_in', type=str, default=None, help='extension of the files that will be renamed (all files rename by default)')
    parser.add_argument('-p', action='store', dest='prefix_in', type=str, default=None, help='the file name prefix of the files that will be renamed (all files rename by default)')
    parser.add_argument('-x', action='store', dest='ext_out', type=str, default=None, help='file extension of the renamed file (keep the same extension by default')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('dir', type=str, help='directory that contains the files to rename')
    parser.add_argument('methods', type=str, help='renaming methods specified with method[+method] where method=cdate|mdate|imgdate|num1-9|name|lname|uname')
    args = parser.parse_args()

    file_number = 1
    
    try:
        if args.recurse:
            for x in os.walk(args.dir):
                if args.ext_in == None and args.prefix_in == None:
                    file_list = glob.glob(os.path.join(x[0], '*.*'))
                elif args.prefix_in == None:
                    file_list = glob.glob(os.path.join(x[0], '*.' + args.ext_in))
                elif args.ext == None:
                    file_list = glob.glob(os.path.join(x[0], args.prefix_in + '*.*'))
                else:
                    file_list = glob.glob(os.path.join(x[0], args.prefix_in + '*.' + args.ext_in))
                                          
                for file in file_list:
                    rename_file(file, args.methods, args.ext_out, args.show, file_number, args.collision)
                    file_number += 1
        else:
            for file in os.listdir(args.dir):
                if args.ext_in != None and not file.endswith('.' + args.ext_in):
                    continue
                elif args.prefix_in != None and not os.path.basename(file).startswith(args.prefix_in):
                    continue
                rename_file(os.path.join(args.dir, file), args.methods, args.ext_out, args.show, file_number, args.collision)
                file_number += 1

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    