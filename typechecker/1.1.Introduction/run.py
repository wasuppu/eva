from EvaTC import EvaTC

eva = EvaTC()

assert eva.tc(1) == 'number'
assert eva.tc(42) == 'number'

print('All assertions passed!')
