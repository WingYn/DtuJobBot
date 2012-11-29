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
print "job pages loaded and random web pages loaded."

# While writing code just use a subset of the data

