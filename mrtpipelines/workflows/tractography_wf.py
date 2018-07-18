from nipype.pipeline import engine as pe
from nipype.interfaces import mrtrix3 as mrt

import numpy as np

def genTemplateTract_wf(wdir=None, nfibers=1000000, nthreads=1, name='genTemplateTract_wf'):
    """

    Set up workflow to generate Tractography
    """

    # Register subjects to template
    # Generate tractography
    genTract = pe.Node(mrt.Tractography(), name='template_tckgen')
    genTract.base_dir = wdir
    genTract.inputs.backtrack
    genTract.inputs.n_tracks = nfibers
    genTract.inputs.out_file = 'template_variant-tckgen_streamlines-%d_tract.tck' % nfibers
    genTract.inputs.nthreads = nthreads

    # Sphereical-deconvoulution informed filtering of tractography
    siftTract = pe.Node(mrt.SIFT(), name='template_tcksift')
    siftTract.base_dir = wdir
    siftTract.inputs.term_number = np.int(nfibers / 2)
    siftTract.inputs.out_file = 'template_variant-sift_streamlines-%d_tract.tck' % np.int(nfibers / 2)
    siftTract.inputs.nthreads = nthreads

    tractConvert = pe.Node(mrt.TCKConvert(), name='template_tckconvert')
    tractConvert.base_dir = wdir
    tractConvert.inputs.out_file = 'template_variant_sift_streamlines-500K_tract.vtk'
    tractConvert.inputs.nthreads = nthreads

    # Build workflow
    workflow = pe.Workflow(name=name)

    workflow.connect([
        (genTract, siftTract, [('out_file', 'in_file')]),
        (siftTract, tractConvert, [('out_file', 'in_file')])
    ])

    return workflow