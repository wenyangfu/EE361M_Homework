Author:	Ngo Xuan Bach (bachnx@jaist.ac.jp)
Date:		April, 2012.
Version:	v1.0
======================================

1. OVERVIEW

ListNet is a tool for learning-to-rank. It is implemented based on the ListNet algorithm:
Source paper: Learning to Rank: From Pairwise Approach to Listwise Approach (ICML 2007)

===============================================================================================================================================

2. HOW TO USE

2.1. Binary

a) learn
Usage: learn data_file iteration learning_rate model_file

b) multiLearn
When the training file is too big, we need to divide the file into some smaller files and 
put them into a directory. In this case, we use multiLearn.exe instead of using learn.exe. 

Usage: multiLearn dir_path iteration learning_rate model_file
	dir_path: the directory contains all training files

c) test
Usage: test model_file data_file output_file

2.2. Build
Please make a C++ project in MS Visual Studio and compile.

==================================================================

3. FILE FORMAT (TRAIN/TEST)
<line> .=. <target> qid:<qid> <feature>:<value> <feature>:<value> ... <feature>:<value>
<target> .=. <float>
<qid> .=. <positive integer>
<feature> .=. <positive integer>
<value> .=. <float>

Here is an example: 

3 qid:1 1:1 2:1 4:0.2
2 qid:1 3:1 4:0.1 5:1
1 qid:1 2:1 4:0.4
1 qid:1 3:1 4:0.3
1 qid:2 3:1 4:0.2
2 qid:2 1:1 2:1 3:1 4:0.4 
1 qid:2 3:1 4:0.1
1 qid:2 3:1 4:0.2 5:1
2 qid:3 3:1 4:0.1 5:1
3 qid:3 1:1 2:1 4:0.3
4 qid:3 1:1 4:0.4 5:1
1 qid:3 2:1 3:1 4:0.5

For more information, please contact me at: bachnx@jaist.ac.jp