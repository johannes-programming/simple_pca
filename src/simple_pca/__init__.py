import click as _click
import fileunity as _fu
import getoptify as _getoptify
import numpy as _np
import numpy.linalg as _la
import pandas as _pd


def calculate(data, dimension):
    df = _pd.DataFrame(data)
    df = df.copy()
    df = (df - df.mean()) / df.std()
    stdmatrix = df.to_numpy()
    cov_df = df.cov()
    cov_arr = cov_df.to_numpy()
    eigenvalues, eigenvectors = _la.eig(cov_arr)
    getreal = lambda x: x.real
    vgetreal = _np.vectorize(getreal)
    eigenvalues = vgetreal(eigenvalues)
    eigenvectors = vgetreal(eigenvectors)

    foo = list()
    for i, eigenvalue in enumerate(eigenvalues):
        eigenvector = eigenvectors[:, i]
        bar = eigenvalue, eigenvector
        foo.append(bar)
    sortkey = lambda x: x[0]
    foo.sort(key=sortkey, reverse=True)

    _eigenvalues = list()
    _eigenvectors = list()
    for eigenvalue, eigenvector in foo:
        _eigenvalues.append(eigenvalue)
        _eigenvectors.append(eigenvector)
    eigenvalues = _np.array(_eigenvalues)
    eigenvectors = _np.transpose(_np.array(_eigenvectors))

    convertedmatrix = stdmatrix * eigenvectors

    # drop zero-columns!

    converteddf = _pd.DataFrame(convertedmatrix)
    converteddf = (converteddf - converteddf.mean()) / converteddf.std()
    stdconvmatrix = converteddf.to_numpy()

    m, n = stdconvmatrix.shape
    if dimension is None:
        resizedmatrix = stdconvmatrix
    elif n < dimension:
        zeromatrix = _np.zeros((m, (dimension - n)))
        resizedmatrix = _np.concatenate((stdconvmatrix, zeromatrix), axis=1)
    else:
        resizedmatrix = stdconvmatrix[:, 0:dimension]

    return resizedmatrix


def run(*, infile, dimension: int = None):
    df = _fu.Simple_TSVUnit.load(infile).data
    df = df.map(lambda e: float(e.strip()))
    ans = calculate(data=df, dimension=dimension)
    return ans


@_getoptify.command(
    shortopts="hV",
    longopts=["help", "version", "infile=", "dimension="],
    allow_argv=True,
    gnu=True,
)
@_click.command(add_help_option=False)
@_click.option("--dimension", type=int)
@_click.option("--infile")
@_click.help_option("-h", "--help")
@_click.version_option(None, "-V", "--version")
def main(**kwargs):
    _click.echo(run(**kwargs))
