# this file used for ploting ROC curves of different learning rates
import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
import glob
from sklearn.metrics import roc_curve, auc,roc_auc_score

# load test label
Test_Y = np.load ("test_label.npy")
print(Test_Y.shape)

# load results
results = {}
for f in glob.glob("predict/*.npy") :
    lr = f.split('\\')[-1].split('_s')[0].replace('_'," = ")
    rows = np.load(f)
    if lr in results:
        results[lr] = results[lr] + [rows]
    else :
        results[lr] = [rows]

# Run classifier with cross-validation and plot ROC curves
plt.figure(figsize=(16,10))
for key , values in results.items() :
    print(key)
    tprs = []
    aucs = []
    areas = []
    mean_fpr = np.linspace(0, 1, 100)

    for i in range(30):
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(Test_Y[i].flatten(), values[0][i].flatten())
        area = roc_auc_score(Test_Y[i].flatten(), values[0][i].flatten())
        areas.append(area)
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    y_plot = plt.plot(mean_fpr, mean_tpr,
             label=f'{key} , AUROC = {np.mean(areas):.2f}' ,
             lw=2, alpha=.8)
    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color=y_plot[0].get_color(), alpha=.1)


plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
         label='Chance', alpha=.8)

plt.xlim([0.00, 1.00])
plt.ylim([0.00, 1.00])
plt.xlabel('False Positive Rate',fontsize=18)
plt.ylabel('True Positive Rate',fontsize=18)
plt.title('Receiver operating characteristic of propsed models'.title(),fontsize=20)
plt.legend(loc="lower right",fontsize=14)
plt.savefig('figure6.png')
plt.show()