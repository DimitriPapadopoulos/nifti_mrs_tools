'''FSL-MRS test script

Test the tools script

Copyright Will Clarke, University of Oxford, 2021'''

# Imports
import subprocess
from pathlib import Path
import nibabel as nib

# Files
testsPath = Path('/Users/wclarke/Documents/Python/fsl_mrs/fsl_mrs/tests')
# testsPath = Path(__file__).parent

# Testing vis option
svs = testsPath / 'testdata/fsl_mrs/metab.nii.gz'
svs_raw = testsPath / 'testdata/fsl_mrs_preproc/metab_raw.nii.gz'
basis = testsPath / 'testdata/fsl_mrs/steam_basis'


def test_vis_svs(tmp_path):
    subprocess.check_call(['mrs_tools', 'vis',
                           '--ppmlim', '0.2', '4.2',
                           '--save', str(tmp_path / 'svs.png'),
                           svs])

    assert (tmp_path / 'svs.png').exists()

    subprocess.check_call(['mrs_tools', 'vis',
                           '--ppmlim', '0.2', '4.2',
                           '--save', str(tmp_path / 'svs2.png'),
                           svs.with_suffix('').with_suffix('')])

    assert (tmp_path / 'svs2.png').exists()

    subprocess.check_call(['mrs_tools', 'vis',
                           '--ppmlim', '0.2', '4.2',
                           '--display_dim', 'DIM_DYN',
                           '--save', str(tmp_path / 'svs3.png'),
                           svs_raw])

    assert (tmp_path / 'svs3.png').exists()

    subprocess.check_call(['mrs_tools', 'vis',
                           '--ppmlim', '0.2', '4.2',
                           '--display_dim', 'DIM_COIL',
                           '--no_mean',
                           '--save', str(tmp_path / 'svs4.png'),
                           svs_raw])

    assert (tmp_path / 'svs4.png').exists()


def test_vis_basis(tmp_path):
    subprocess.check_call(['mrs_tools', 'vis',
                           '--ppmlim', '0.2', '4.2',
                           '--save', str(tmp_path / 'basis.png'),
                           basis])

    assert (tmp_path / 'basis.png').exists()


# Testing info option
processed = testsPath / 'testdata/fsl_mrs/metab.nii.gz'
unprocessed = testsPath / 'testdata/fsl_mrs_preproc/metab_raw.nii.gz'


def test_single_info(tmp_path):
    subprocess.check_call(['mrs_tools', 'info', str(processed)])


def test_multi_info(tmp_path):
    subprocess.check_call(['mrs_tools', 'info', str(processed), str(unprocessed)])


# Testing merge option
test_data_merge_1 = testsPath / 'testdata' / 'fsl_mrs_preproc' / 'wref_raw.nii.gz'
test_data_merge_2 = testsPath / 'testdata' / 'fsl_mrs_preproc' / 'quant_raw.nii.gz'


def test_merge(tmp_path):
    """The tests here only check that the expected files are created.
    I rely on the much more detailed tests in test_utils_nifti_mrs_tools_split_merge.py
    to check that the merge is carried out correctly.
    """
    subprocess.check_call(['mrs_tools', 'merge',
                           '--dim', 'DIM_DYN',
                           '--output', str(tmp_path),
                           '--filename', 'test_2_merge',
                           '--files', str(test_data_merge_1), str(test_data_merge_2)])

    assert (tmp_path / 'test_2_merge.nii.gz').exists()

    subprocess.check_call(['mrs_tools', 'merge',
                           '--dim', 'DIM_DYN',
                           '--output', str(tmp_path),
                           '--filename', 'test_3_merge',
                           '--files', str(test_data_merge_1), str(test_data_merge_2), str(test_data_merge_2)])

    assert (tmp_path / 'test_3_merge.nii.gz').exists()

    subprocess.check_call(['mrs_tools', 'merge',
                           '--dim', 'DIM_DYN',
                           '--output', str(tmp_path),
                           '--files', str(test_data_merge_1), str(test_data_merge_2)])

    assert (tmp_path / 'wref_raw_quant_raw_merged.nii.gz').exists()


# Test split option
test_data_split = testsPath / 'testdata' / 'fsl_mrs_preproc' / 'metab_raw.nii.gz'


def test_split(tmp_path):
    """The tests here only check that the expected files are created.
    I rely on the much more detailed tests in test_utils_nifti_mrs_tools_split_merge.py
    to check that the merge is carried out correctly.
    """
    subprocess.check_call(['mrs_tools', 'split',
                           '--dim', 'DIM_DYN',
                           '--index', '31',
                           '--output', str(tmp_path),
                           '--filename', 'split_file',
                           '--file', str(test_data_split)])

    assert (tmp_path / 'split_file_low.nii.gz').exists()
    assert (tmp_path / 'split_file_high.nii.gz').exists()
    f1 = nib.load(tmp_path / 'split_file_low.nii.gz')
    f2 = nib.load(tmp_path / 'split_file_high.nii.gz')
    assert f1.shape[5] == 32
    assert f2.shape[5] == 32

    subprocess.check_call(['mrs_tools', 'split',
                           '--dim', 'DIM_DYN',
                           '--index', '31',
                           '--output', str(tmp_path),
                           '--file', str(test_data_split)])

    assert (tmp_path / 'metab_raw_low.nii.gz').exists()
    assert (tmp_path / 'metab_raw_high.nii.gz').exists()
    f1 = nib.load(tmp_path / 'metab_raw_low.nii.gz')
    f2 = nib.load(tmp_path / 'metab_raw_high.nii.gz')
    assert f1.shape[5] == 32
    assert f2.shape[5] == 32

    subprocess.check_call(['mrs_tools', 'split',
                           '--dim', 'DIM_DYN',
                           '--indices', '31', '34', '40',
                           '--filename', 'indicies_select',
                           '--output', str(tmp_path),
                           '--file', str(test_data_split)])

    assert (tmp_path / 'indicies_select_others.nii.gz').exists()
    assert (tmp_path / 'indicies_select_selected.nii.gz').exists()
    f1 = nib.load(tmp_path / 'indicies_select_others.nii.gz')
    f2 = nib.load(tmp_path / 'indicies_select_selected.nii.gz')
    assert f1.shape[5] == 61
    assert f2.shape[5] == 3


# Test reorder option
def test_reorder(tmp_path):
    subprocess.check_call(['mrs_tools', 'reorder',
                           '--dim_order', 'DIM_DYN', 'DIM_COIL',
                           '--output', str(tmp_path),
                           '--filename', 'reordered_file',
                           '--file', str(test_data_split)])

    assert (tmp_path / 'reordered_file.nii.gz').exists()

    subprocess.check_call(['mrs_tools', 'reorder',
                           '--dim_order', 'DIM_COIL', 'DIM_DYN', 'DIM_EDIT',
                           '--output', str(tmp_path),
                           '--file', str(test_data_split)])

    assert (tmp_path / 'metab_raw_reordered.nii.gz').exists()

    subprocess.check_call(['mrs_tools', 'reorder',
                           '--dim_order', 'DIM_EDIT', 'DIM_COIL', 'DIM_DYN',
                           '--output', str(tmp_path),
                           '--filename', 'reordered_file',
                           '--file', str(test_data_split)])

    assert (tmp_path / 'reordered_file.nii.gz').exists()


# Test conjugate option
def test_conjugate(tmp_path):
    subprocess.check_call(['mrs_tools', 'conjugate',
                           '--output', str(tmp_path),
                           '--filename', 'conj_file',
                           '--file', str(svs)])

    assert (tmp_path / 'conj_file.nii.gz').exists()

    subprocess.check_call(['mrs_tools', 'conjugate',
                           '--output', str(tmp_path),
                           '--file', str(svs)])

    assert (tmp_path / 'metab.nii.gz').exists()
