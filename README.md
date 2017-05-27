Simple Manual Image Categorizer
===============================
Got unsorted images? Get off your duff and sort them.
Give SMIC a source path full of unlabeled images and
a destination directory with a subdirectory for each
category. The GUI will use the subdirectory names as
labels. For speedy categorization, the numbers 1-9
are hotkeys to assign their respective category.

Installation
------------
`pip install simple-manual-image-categorizer`

Example
-------
To sort a hotdog detector dataset:

`smic path/to/source/hotdog/images path/of/destination`

Where `path/to/destination` has subdirectories `hotdog` and `not_hotdog`
