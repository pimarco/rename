File Renamer
============

usage: rename.py [-h] [-r] [-c COLLISION] [-s] [-e EXT_IN] [-p PREFIX_IN] [-x EXT_OUT] [--version] dir methods

CMELSoft - File rename utility that can be use to automatically rename several files in a directory

positional arguments:

  dir: directory that contains the files to rename
  
  methods: renaming methods specified with method[+method] where method=cdate|mdate|imgdate|num1-9|name|lname|uname

optional arguments:

  -h, --help    show this help message and exit
  
  -r            rename file recursively in all directory under the specified one
  
  -c COLLISION  add a rename collision number with the specified number of digit (no collision number is added by default)
  
  -s            show the new file name that will be used without renaming any files
  
  -e EXT_IN     extension of the files that will be renamed (all files rename by default)
  
  -p PREFIX_IN  the file name prefix of the files that will be renamed (all files rename by default)
  
  -x EXT_OUT    file extension of the renamed file (keep the same extension by default
  
  --version     show program's version number and exit
  
## Examples

WARNING: Always use the -s option before trying to rename any files to make sure you get the result you want before doing the real file renaming.

Rename image files from directory myimage with the family prefix followed by the image date and jpg extension.

```
rename.py -x jpg myimage family+imgdate
```

Use the -c option if some file renaming result in collision (with same file name)

```
rename.py -c1 myimage family+imgdate
```

Use the num method to add a file number in the resulting file name

```
rename.py myimage family+imgdate+num3
```