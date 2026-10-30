# PlasX Modernization Summary (Python 3.13)

This document summarizes the changes made to modernize **PlasX** to support modern Python versions (Python 3.10 through 3.13) and modern scientific package versions (NumPy 2.x, Pandas 3.x, SciPy 1.18+, Numba 0.68+, and scikit-learn 1.9+).

---

## 1. Environment & Dependencies

PlasX was updated and verified using Python 3.13 via the Conda environment `mobmess-py313` on macOS (Apple Silicon):

```bash
conda create -y -n mobmess-py313 -c conda-forge -c bioconda \
    python=3.13 numpy pandas scipy scikit-learn numba python-blosc pytest
conda activate mobmess-py313
pip install -e .
```

### Verified Dependency Versions
* **Python**: 3.13.16
* **NumPy**: 2.5.4
* **Pandas**: 3.0.6
* **SciPy**: 1.18.1
* **Numba**: 0.68.0
* **python-blosc**: 1.11.4
* **scikit-learn**: 1.9.1

---

## 2. Incompatibilities Identified and Resolved

### A. NumPy 1.24+ & 2.0 Incompatibilities
* **`np.str` / `np.bool` Dtype Removals**:
  * In NumPy 1.24+, the aliases `np.bool` and `np.str` were removed, triggering fatal `AttributeError: module 'numpy' has no attribute 'bool'` / `'str'`.
* **Fixes**:
  * `plasx/mmseqs.py`:
    * Line 507: Changed `read_h(..., dtype=np.str)` to `dtype=str`.
    * Line 796: Changed `scipy.sparse.coo_matrix((np.ones(..., np.bool), ...))` to `bool`.
    * Line 1221: Changed `np.issubdtype(..., np.bool)` to `np.bool_`.
    * Line 1228: Changed `scipy.sparse.identity(..., dtype=np.bool)` to `bool`.
  * `plasx/utils.py`:
    * Lines 364 & 372: Replaced `x.astype(np.bool)` with `x.astype(bool)` in `downcast_uint()`.

### B. Pandas 2.x & 3.x Deprecations
* **`pd.api.types.is_categorical_dtype` Deprecation**:
  * In Pandas 2.x/3.x, `is_categorical_dtype` is deprecated and generates `Pandas4Warning`.
* **Fixes**:
  * `plasx/pd_utils.py`:
    * Lines 768 & 776 (`remove_unused_categories`): Replaced `pd.api.types.is_categorical_dtype(s)` with `isinstance(s.dtype, pd.CategoricalDtype)`.
    * Line 799 (`fast_duplicated`): Replaced `is_categorical_dtype` check with `isinstance(df[c].dtype, pd.CategoricalDtype)`.

### C. Packaging Modernization
* **`pyproject.toml`**: Added modern PEP 517/621 packaging configuration with `setuptools.build_meta`.
* **`setup.py`**:
  * Updated `python_requires` from `>=3.7, <4` to `>=3.10`.
  * Added classifiers for Python 3.10, 3.11, 3.12, and 3.13.
  * Added optional test dependency `extras_require={'test': ['pytest']}`.
* **`.gitignore`**: Added standard Python/build gitignore patterns (`__pycache__`, `*.egg-info`, `.pytest_cache`, etc.).
* **Test Suite**: Added `test/test_plasx.py` to test module imports, data type downcasting, categorical manipulations, Numba operations, MMseqs sparse conversion, and CLI execution.

---

## 3. Verification Results

```bash
$ conda run -n mobmess-py313 pytest test/test_plasx.py -v
============================= test session starts ==============================
platform darwin -- Python 3.13.16, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/cnicolaou/LocalOnly/dev/github.com/cosnicolaou/PlasX
configfile: pyproject.toml
collected 6 items

test/test_plasx.py::test_imports PASSED                                  [ 16%]
test/test_plasx.py::test_downcast_uint PASSED                            [ 33%]
test/test_plasx.py::test_pd_utils_categorical PASSED                     [ 50%]
test/test_plasx.py::test_nb_utils_operations PASSED                      [ 66%]
test/test_plasx.py::test_mmseqs_sparse PASSED                            [ 83%]
test/test_plasx.py::test_cli_help PASSED                                 [100%]

============================== 6 passed in 0.63s ===============================
```

### CLI Verification
```bash
$ conda run -n mobmess-py313 plasx -h
usage: plasx [-h] {predict,search_de_novo_families,extract_cog_and_pfam_profiles} ...

A plasmid sequence classifier
...
```
Everything passes cleanly with 0 warnings.
