#!/usr/bin/env python3

import sys
import random
import math
from numpy import *

if len(sys.argv) < 3:
	print("Usage: blast.py sequence1 sequence2")
	quit()

seq1 = sys.argv[1]
seq2 = sys.argv[2]

#print(seq1)
#print(seq2)

if len(seq1) < len(seq2):
   t = seq1
   seq1 = seq2
   seq2 = t

# Smith-Waterman:
# for each word in sequence1:
#    for each word in sequence2:
#       set s[i,j] = 1 if match, -1 otherwise
#
#  choose a gap penalty (-1, I guess?)
#
#  initialise scoring matrix to 1+len(seq1) * 1+len(seq2)
#   first row + column = 0
#  
#  Scoring: 
#   for each element from left to right, top to bottom, consider score of substitution (diagonal score) or adding gaps (horizontal or vertical scores). If neither scores are positive, set element to 0, otherwise use highest score and record source of the score.
# 
# Traceback: starting with element with highest score, step through to the highest score recursively.


# Needleman-Wunsch:
# Scoring: +1 if match, -1 if gap or mismatch
#
#   Consider a linear gap penalty. Score2 and score3 are +1 if
#      top and left were also score2 and score3, respectively.
#      Otherwise, we'll rank a sequence with a single new trait insert worse than one with a trait replaced.
#     Not a bad problem, and maybe nice to have some error
#     Oooh, could "upgrade" the sequence analysis algorithm this way.
# 
# Prepend '-' to each sequence
# Initialise a S matrix of n+1 * m+1
# Start with a 0 in (0,0)
# for i in 0..m
#    for j in 0..n
#       score1 = match(seq1(i),seq2(j)) + S(i-1,j-1)
#       score2 = -1 + S(i,j-1) (+1 if S(i,j-1) == S2(i,j-1))
#       score3 = -1 + S(i-1,j) (ditto)
#       S(i,j) = max(score1)
#       S1(i,j) = score1
#       S2(i,j) = score2
#       S3(i,j) = score3
#
# Then walk back from bottom right corner

def match(A, B):
	if A == B:
		return 1
	return -1

seq1 = '-' + seq1
seq2 = '-' + seq2
S = zeros((len(seq1),len(seq2)),dtype=int16)
S1 = zeros((len(seq1),len(seq2)),dtype=int16)
S2 = zeros((len(seq1),len(seq2)),dtype=int16)
S3 = zeros((len(seq1),len(seq2)),dtype=int16)
for i in range(1,len(seq1)):
	S[i][0] = S[i-1][0] - 1
	
for j in range(1,len(seq2)):
	S[0][j] = S[0][j-1] - 1	
	
for i in range(1,len(seq1)):
	for j in range(1,len(seq2)):
		score1 = S[i-1][j-1] + match(seq1[i],seq2[j]) 
		S1[i][j] = score1
		score2 = S[i][j-1] - 1
		if S[i][j-1] == S2[i][j-1]:
		   score2 += 1
		S2[i][j] = score2		
		score3 = S[i-1][j] - 1
		if S[i-1][j] == S3[i-1][j]:
		   score3 += 1
		S3[i][j] = score3		
		S[i][j] = max(score1,score2,score3)

#print(S)

distance = 0
similarity = 0
align1 = ''
align2 = ''
i = len(seq1)-1
j = len(seq2)-1
done = False
while not done:
	score1 = S[i-1][j-1]
	score2 = S[i][j-1]   
	score3 = S[i-1][j]
	smax = max(score1,score2,score3)
	if score1 == smax:
		align1 += seq1[i]
		align2 += seq2[j]
		if not seq1[i] == seq2[j]:
		   distance += 1	
		else:
			similarity += 1	
		i -= 1
		j -= 1
	elif score2 == smax:
		align1 += '-'
		align2 += seq2[j]
		j -= 1
		if len(align1)>2 and not align1[-2] == '-': 
			distance += 1
	else:
		align1 += seq1[i]
		align2 += '-'
		i -= 1
		if len(align2)>2 and not align2[-2] == '-': 
			distance += 1

		
	if i == 0 or j == 0:
		done = True

print("Sequence lengths:",len(seq1)-1,",",len(seq2)-1)		
print("Edit distance:",distance)
print("Similarity:",similarity,100.*similarity/(len(seq1)-1),"%")
print(align1[::-1])
print(align2[::-1])

#for i in range(len(align1)):
#   print(align1[len(align1)-i-1],align2[len(align1)-i-1])
