import pdf2doi
import requests
import json
import os

pdf2doi.config.set('verbose',False)

#results = pdf2doi.pdf2doi(r'D:\Projects\Academic\FindMyResearch\FindMyResearch\Tests\TestPapers\2410.18402v1.Low_Rank_Tensor_Learning_by_Generalized_Nonconvex_Regularization.pdf')
results = pdf2doi.pdf2doi(r'D:\Projects\Academic\FindMyResearch\FindMyResearch\Tests\TestPapers')

print(results[5])
print(results[5]['path'].split('\\')[-1])
#print(results['validation_info'])