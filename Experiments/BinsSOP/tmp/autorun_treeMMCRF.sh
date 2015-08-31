

#for inname in 'emotions' 'yeast' 'scene' 'enron' 'cal500' 'fp' 'cancer' 'medical' 'toy10' 'toy50'
#for inname in 'emotions' 'yeast' 'scene' 'enron' #'cal500' 'fp' 'cancer' 'medical' 'toy10' 'toy50'
#for inname in  'cal500' 'fp' 'cancer' 'medical'
for inname in 'cancer'
#for inname in 'toy10' 'toy50'
do
    nohup matlab -nodesktop -nosplash -r "run_treeMMCRF '$inname'" &
done
wait
rm nohup.out
