import pickle

# Load data
print "Loading job pages..."
jobpages = pickle.load(open("data/clean_job_data.pydata", "rb" ))
print "Loading random web pages..."
randompages = pickle.load(open("data/clean_web_data1.pydata", "rb" ))
#randompages += pickle.load(open("data/clean_web_data2.pydata", "rb" ))
#randompages += pickle.load(open("data/clean_web_data3.pydata", "rb" ))
#randompages += pickle.load(open("data/clean_web_data4.pydata", "rb" ))
#randompages += pickle.load(open("data/clean_web_data5.pydata", "rb" ))
print "%d job pages loaded and %d random web pages loaded."

# While writing code just use a subset of the data
N = 500 # no of samples
jobpages = jobpages[:N]
randompages = randompages[:N]

# How to use:
j = jobpages[42]
print "url: " + str(j[0])
print "url tokens: " + str(j[1])
print "word list: " + str(j[2][:200]) # just show the first 200 words
