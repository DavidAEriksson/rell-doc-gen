<div align="center">
  <h1 align="center">Rell Documentation Generator</h1>
  <h6>regex regex regex regex regex</h6>

</div>

## How to use

0. Write comments as described in `doc-gen.py` and make sure that your poject is structured as follows:
	1. ```
		a_folder/
			function.rell
    			module.rell
            		operation.rell
            		query.rell
        	main.rell
        	chromia.yml
        	etc..
	   ```
2. Clone or copy `doc-gen.py` into the `root/` of your project.
3. Run `python3 doc-gen.py`
4. A new file `MODULE_DEFINITIONS.md` will be created in the root of your project. If you want to change the name of this file you can update the variable `output_file_path`.

###### ❗ Note that this file is deleted and "re-made" every time the script runs.
