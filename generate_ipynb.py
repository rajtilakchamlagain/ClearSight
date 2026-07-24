import nbformat as nbf
with open('test_all.py', encoding='utf-8') as f:
    code = f.read()

nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_code_cell(code)]
nbf.write(nb, 'ClearSight_Test.ipynb')
