# MachinLearning

from pylab import *
from scipy.io import loadmat
import neurolab as nl
from sklearn import cross_validation, tree
import scipy.linalg as linalg
from scipy import stats
from sklearn.mixture import GMM

#http://code.google.com/p/neurolab/
def ANN(X, y, attributeNames, C, hidden, K):
    """docstring for ANN 
    X: matrix of data
    y: vector of classes 
    attributeNames : set of attributeNames
    C: number of classes to classify 
    hidden : number of hidden attributes
    K: number of crossvalidation folds 
    """
    
    # Load Matlab data file and extract variables of interest
    #mat_data = loadmat('../Data/wine2.mat')
    #attributeNames = [name[0] for name in mat_data['attributeNames'][0]]
    #X = np.matrix(mat_data['X'])
    #y = np.matrix(mat_data['y'])
    N, M = X.shape
    #C = 2

    # Normalize and compute Principal Components
    Y = stats.zscore(X,0);
    U,S,V = linalg.svd(Y,full_matrices=False)
    V = mat(V).T

    # Components to be included as features
    k_pca = 8
    X = X*V[:,0:k_pca]
    N, M = X.shape

    # Parameters for neural network classifier
    n_hidden_units = hidden     # number of hidden units
    n_train = 1             # number of networks trained in each k-fold

    learning_rate = 0.0005  # rate of weights adaptation
    learning_goal = 200.0   # stop criterion 1 (train mse to be reached)
    max_epochs = 32         # stop criterion 2 (max epochs in training)

    # K-fold crossvalidation
    #K = 5                   # only five folds to speed up this example
    CV = cross_validation.KFold(N,K,shuffle=True)

    # Variable for classification error
    errors = np.zeros(K)
    error_hist = np.zeros((max_epochs,K))
    bestnet = list()
    k=0
    for train_index, test_index in CV:
        print('\nCrossvalidation fold: {0}/{1}'.format(k+1,K))    
    
        # extract training and test set for current CV fold
        X_train = X[train_index,:]
        y_train = y[train_index,:]
        X_test = X[test_index,:]
        y_test = y[test_index,:]
    
        best_train_error = 1e100
        for i in range(n_train):
            # Create randomly initialized network with 2 layers
            ann = nl.net.newff([[-1, 1]]*M, [n_hidden_units, 1], [nl.trans.LogSig(),nl.trans.LogSig()])
            # train network
            train_error = ann.train(X_train, y_train, goal=learning_goal, epochs=max_epochs, lr=learning_rate, show=round(max_epochs/8))
            if train_error[-1]<best_train_error:
                bestnet.append(ann)
                best_train_error = train_error[-1]
                error_hist[range(len(train_error)),k] = train_error
    
        y_est = bestnet[k].sim(X_test)
        y_est = (y_est>.5).astype(int)
        errors[k] = (y_est!=y_test).sum().astype(float)/y_test.shape[0]
        k+=1
    

    # Print the average classification error rate
    print('Error rate: {0}%'.format(100*mean(errors)))

    # Display the decision boundry for the last crossvalidation fold.
    # (create grid of points, compute network output for each point, color-code and plot).

    grid_range = [-1, 20, -1, 5]; delta = 0.1; levels = 100
    a = arange(grid_range[0],grid_range[1],delta)
    b = arange(grid_range[2],grid_range[3],delta)
    A, B = meshgrid(a, b)
    values = np.zeros(A.shape)

    show()
    # Display exemplary networks learning curve (best network of each fold)
    #figure(2); hold(True)
    #bn_id = argmax(error_hist[-1,:])
    #error_hist[error_hist==0] = learning_goal
    #for bn_id in range(K):
    #   plot(error_hist[:,bn_id]); 
    #   xlabel('epoch'); 
    #   ylabel('train error (mse)'); 
    #   title('Learning curve (best for each CV fold)')
    #
    #plot(range(max_epochs), [learning_goal]*max_epochs, '-.')
    #
    #
    #show()
    pass
    
def GMM_determNumOfK(X, y, attributeNames, classNames, KRange):
    """docstring for GMM_determNumOfK
    X: matrix of data
    y: vector of classes 
    attributeNames : set of attributeNames
    classNames:
    KRange: range of clusters to try 
    """
    # Load Matlab data file and extract variables of interest
    #mat_data = loadmat('..\\Data\\synth1.mat')
    #X = np.matrix(mat_data['X'])
    #y = np.matrix(mat_data['y'])
    #attributeNames = [name[0] for name in mat_data['attributeNames'].squeeze()]
    #classNames = [name[0][0] for name in mat_data['classNames']]
    N, M = X.shape
    C = len(classNames)


    # Range of K's to try
    #KRange = range(1,11)
    T = len(KRange)

    covar_type = 'full'     # you can try out 'diag' as well
    reps = 3                # number of fits with different initalizations, best result will be kept

    # Allocate variables
    BIC = np.zeros((T,1))
    AIC = np.zeros((T,1))
    CVE = np.zeros((T,1))

    # K-fold crossvalidation
    CV = cross_validation.KFold(N,10,shuffle=True)

    for t,K in enumerate(KRange):
            print('Fitting model for K={0}\n'.format(K))

            # Fit Gaussian mixture model
            gmm = GMM(n_components=K, covariance_type=covar_type, n_init=reps, params='wmc').fit(X)

            # Get BIC and AIC
            BIC[t,0] = gmm.bic(X)
            AIC[t,0] = gmm.aic(X)

            # For each crossvalidation fold
            for train_index, test_index in CV:

                # extract training and test set for current CV fold
                X_train = X[train_index]
                X_test = X[test_index]

                # Fit Gaussian mixture model to X_train
                gmm = GMM(n_components=K, covariance_type=covar_type, n_init=reps, params='wmc').fit(X_train)

                # compute negative log likelihood of X_test
                CVE[t] += -gmm.score(X_test).sum()
            

    # Plot results

    figure(1); hold(True)
    plot(KRange, BIC)
    plot(KRange, AIC)
    plot(KRange, 2*CVE)
    legend(['BIC', 'AIC', 'Crossvalidation'])
    xlabel('K')
    show()
    pass
    
def GMM(X, y, attributeNames, classNames, K, reps, cov_type):
    """docstring for GMM
    X: matrix of data
    y: vector of classes 
    attributeNames : set of attributeNames
    classNames:
    K: Number of clusters
    reps:  number of fits with different initalizations, best result will be kept
    cov_type: type of covariance, you can try out 'full' or 'diag' 
    """
    # Load Matlab data file and extract variables of interest
    #mat_data = loadmat('..\\Data\\synth1.mat')
    #X = np.matrix(mat_data['X'])
    #y = np.matrix(mat_data['y'])
    #attributeNames = [name[0] for name in mat_data['attributeNames'].squeeze()]
    #classNames = [name[0][0] for name in mat_data['classNames']]
    N, M = X.shape
    C = len(classNames)


    # Number of clusters
    #K = 4
    #cov_type = 'full'       # type of covariance, you can try out 'diag' as well
    #reps = 1                # number of fits with different initalizations, best result will be kept

    # Fit Gaussian mixture model
    gmm = GMM(n_components=K, covariance_type=cov_type, n_init=reps, params='wmc').fit(X)
    cls = gmm.predict(X)    # extract cluster labels
    cds = gmm.means_        # extract cluster centroids (means of gaussians)
    covs = gmm.covars_      # extract cluster shapes (covariances of gaussians)

    # Plot results:
    figure(figsize=(14,9))
    clusterplot(X, clusterid=cls, centroids=cds, y=y, covars=covs)
    show()
    pass
    
def PruningDecisionTree(X, y, attributeNames, classNames):
    """docstring for PruningDecisionTree
    X: matrix of data
    y: vector of classes 
    attributeNames : set of attributeNames
    classNames:
    """
    #mat_data = loadmat('../Data/wine2.mat')
    #X = np.matrix(mat_data['X'])
    #y = np.matrix(mat_data['y'], dtype=int)
    #attributeNames = [name[0] for name in mat_data['attributeNames'][0]]
    #classNames = [name[0][0] for name in mat_data['classNames']]
    N, M = X.shape
    C = len(classNames)

    # Tree complexity parameter - constraint on maximum depth
    tc = np.arange(2, 21, 1)

    # Simple holdout-set crossvalidation
    test_proportion = 0.5
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=test_proportion)

    # Initialize variables
    Error_train = np.empty((len(tc),1))
    Error_test = np.empty((len(tc),1))

    for i, t in enumerate(tc):
        # Fit decision tree classifier, Gini split criterion, different pruning levels
        dtc = tree.DecisionTreeClassifier(criterion='gini', max_depth=t)
        dtc = dtc.fit(X_train,y_train.ravel())

        # Evaluate classifier's misclassification rate over train/test data
        y_est_test = dtc.predict(X_test)
        y_est_train = dtc.predict(X_train)
        misclass_rate_test = sum(np.abs(np.mat(y_est_test).T - y_test)) / float(len(y_est_test))
        misclass_rate_train = sum(np.abs(np.mat(y_est_train).T - y_train)) / float(len(y_est_train))
        Error_test[i], Error_train[i] = misclass_rate_test, misclass_rate_train
    
    f = figure(); f.hold(True)
    plot(tc, Error_train)
    plot(tc, Error_test)
    xlabel('Model complexity (max tree depth)')
    ylabel('Error (misclassification rate)')
    legend(['Error_train','Error_test'])
    
    show()
    pass