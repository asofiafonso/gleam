__author__ = "Andra Stroe"
__version__ = "0.1"

import glob

import numpy as np
from astropy.io import fits
from astropy.table import QTable, Column
from astropy import units as u

import gleam.constants as c


def read_lof(file1):
    """
    For each sample, quadrants and extensions, it reads the head file produced 
    by specpro, which contains a list of the sources and their properties
    Input:
        data_path: folder location of head file and all the individual spectra
                   ! assumes the name contains "_zinfo.dat" in order to find it
                   and that there is only 1 such file in each folder
        The format of the head file is the following
        #Setup Pointing SourceNumber RA DEC Sample Redshift Confidence Crew Comments
    Return: 
        Astropy Table with measurements of interest: the source number, RA, DEC,
        the parent sample, redshift (from specpro) and the z confidence
    """
    data = np.array(np.genfromtxt(file1, dtype="U8,U20,i,f,f,U10,f,f,U2,U20,U20"))

    # Extract each measurement of interest into a separate Table
    t = QTable()
    t["Setup"] = Column(
        [datum[0] for datum in data], dtype="U", description="Telescope setup",
    )
    t["Pointing"] = Column(
        [datum[1] for datum in data],
        dtype="U",
        description="Stack type or telescope source",
    )
    t["SourceNumber"] = Column(
        [datum[2] for datum in data], dtype="U", description="SourceNumber"
    )
    t["RA"] = Column(
        [datum[3] for datum in data],
        unit=u.degree,
        dtype="f",
        description="Right Ascension",
    )
    t["DEC"] = Column(
        [datum[4] for datum in data],
        unit=u.degree,
        dtype="f",
        description="Declination",
    )
    t["Sample"] = Column(
        [datum[5] for datum in data], dtype="U", description="Parent sample"
    )
    t["Redshift"] = Column(
        [datum[6] for datum in data], dtype="f", description="Redshift"
    )
    t["Confidence"] = Column(
        [datum[7] for datum in data],
        dtype="f",
        description="Confidence as assigned by user. "
        "Scales from 1 (best) to 5 (worst)",
    )
    t["Membership"] = Column([datum[9] for datum in data], dtype="U20")
    t["Type"] = Column([datum[10] for datum in data], dtype="U20", description="Type")
    return t


def naming_convention(data_path, sample, source_number, setup, pointing, mod):
    """
    Naming convention for files which starts with type of file and is followed
    by details about the source and setup, in order: setup, pointing, source
    number, and parent sample
    """
    return (
        f"{data_path}/{mod}.{setup}.{pointing}.{source_number.astype(int):03d}.{sample}"
    )