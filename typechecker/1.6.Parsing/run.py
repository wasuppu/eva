from EvaTC import EvaTC
from testcases import testcases

eva = EvaTC()

for test in testcases:
    test(eva)

print('All assertions passed!')
