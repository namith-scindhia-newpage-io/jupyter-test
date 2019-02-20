import nbformat
from nbformat.v4 import new_notebook, new_code_cell
from notebook import notebookapp
from nbconvert.preprocessors import ExecutePreprocessor
import os
import sys

# set default encoding to save notebook output
reload(sys)  
sys.setdefaultencoding('utf-8')

# directory of dataset
dataset_dir = '/tmp'
notebook_file_path = '{0}/{1}.ipynb'
dataset_file_path = '{0}/{1}.csv'

server = list(notebookapp.list_running_servers())[0]
juypter_url = server['url'] + 'notebooks/{0}?token=' + server['token']
notebook_dir = server['notebook_dir']

def load_dataset(dataset_file_name):
	ds_file_path = dataset_file_path.format(dataset_dir, dataset_file_name)
	if not os.path.isfile(ds_file_path):
		return "Dataset doesn't exist"

	nb_file = notebook_file_path.format(notebook_dir, dataset_file_name)
	
	# check if file exist under notebook dir
	if not os.path.isfile(nb_file):
		cells = []
		# add code to notebook
		cells.append(new_code_cell(source ='import pandas as pd', execution_count=1))
		cells.append(new_code_cell(source ='df = pd.read_csv(\'' + ds_file_path + '\')', execution_count=2))
		cells.append(new_code_cell(source ='df', execution_count=3))
		
		nb = new_notebook(cells = cells)
		# excute code under notebook
		ep = ExecutePreprocessor(timeout=1000, kernel_name='python3')
		ep.preprocess(nb, {})

		# save notebook to local 
		with open(nb_file, 'w') as f:
			nbformat.write(nb, f)
	return juypter_url.format(os.path.basename(nb_file))

# As argument need to pass name of dataset
print load_dataset(sys.argv[1])