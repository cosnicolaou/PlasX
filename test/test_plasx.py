import pytest
import numpy as np
import pandas as pd
import scipy.sparse

import plasx
import plasx.utils as utils
import plasx.pd_utils as pd_utils
import plasx.nb_utils as nb_utils
import plasx.fasta_utils as fasta_utils
import plasx.compress_utils as compress_utils
import plasx.mmseqs as mmseqs
import plasx.model as model
import plasx.plasx_script as plasx_script


def test_imports():
    assert plasx is not None
    assert utils is not None
    assert pd_utils is not None
    assert nb_utils is not None
    assert fasta_utils is not None
    assert compress_utils is not None
    assert mmseqs is not None
    assert model is not None


def test_downcast_uint():
    # Tests the fix for np.bool removal in numpy 1.24+
    empty = np.array([], dtype=np.uint8)
    downcast_empty = utils.downcast_uint(empty)
    assert downcast_empty.dtype == bool

    arr_bool = np.array([0, 1, 0, 1], dtype=np.int64)
    downcast_bool = utils.downcast_uint(arr_bool)
    assert downcast_bool.dtype == bool

    arr_uint8 = np.array([0, 5, 255], dtype=np.int64)
    downcast_uint8 = utils.downcast_uint(arr_uint8)
    assert downcast_uint8.dtype == np.uint8


def test_pd_utils_categorical():
    # Tests the fix for deprecated pd.api.types.is_categorical_dtype in pandas 2.x/3.x
    df = pd.DataFrame({
        'c1': pd.Categorical(['a', 'b', 'a']),
        'c2': [1, 2, 1]
    })
    cleaned = pd_utils.remove_unused_categories(df)
    assert isinstance(cleaned['c1'].dtype, pd.CategoricalDtype)

    dups = pd_utils.fast_duplicated(df)
    assert len(dups) == 3
    assert list(dups) == [False, False, True]


def test_nb_utils_operations():
    # Tests numba compilation and execution on Python 3.13
    a = np.array([1, 2, 3], dtype=np.float64)
    b = np.array([4, 5, 6], dtype=np.float64)
    added = nb_utils.nb_add(a, b)
    assert np.allclose(added, [5, 7, 9])

    divided = nb_utils.nb_divide(b, a)
    assert np.allclose(divided, [4.0, 2.5, 2.0])


def test_mmseqs_sparse():
    # Tests clu_to_sp dtype and sparse matrix conversion
    clu = pd.DataFrame({
        'representative': ['rep1', 'rep1', 'rep2'],
        'member': [0, 1, 2]
    })
    clu_sp, reps = mmseqs.clu_to_sp(clu)
    assert clu_sp.shape[0] == 2
    assert clu_sp.dtype == bool or np.issubdtype(clu_sp.dtype, np.bool_)


def test_cli_help():
    parser = plasx_script.get_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(['-h'])
    assert exc_info.value.code == 0
