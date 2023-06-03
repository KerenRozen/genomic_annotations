import argparse
import gzip
import numpy as np
from pathlib import Path

from services.consts import CHROMOSOME_TO_INT_GH38, PARTIAL_SUMS_GH38, REGULATORY_REGIONS_ORDER


def init_regulations_db(path):
    #db = np.zeros(249250621, dtype=np.uintc) # Local machine
    #db = np.zeros(6203609478, dtype=np.uintc) # Gh37
    db = np.zeros(6198822410, dtype = np.uintc) # Gh38
    with gzip.open(Path(path), 'rt') as f:
        for row in f:
            if not row.startswith('#'):
                fields = row.strip().split('\t')
                seg_type = fields[2]
                chromosome = CHROMOSOME_TO_INT_GH38[fields[0]]
                start_pos = int(fields[3])
                end_pos = int(fields[4])
                strand = fields[6]
                if strand == '+':
                    index = PARTIAL_SUMS_GH38[chromosome-1]
                    db[index+start_pos-1: index+end_pos] |= 2 ** REGULATORY_REGIONS_ORDER[seg_type]
                elif strand == '-':
                    index = PARTIAL_SUMS_GH38[chromosome+193]
                    db[index+start_pos-1: index+end_pos] |= 2 ** REGULATORY_REGIONS_ORDER[seg_type]
                else:
                    index1 = PARTIAL_SUMS_GH38[chromosome-1]
                    index2 = PARTIAL_SUMS_GH38[chromosome+193]
                    db[index1+start_pos-1: index1+end_pos] |= 2**REGULATORY_REGIONS_ORDER[seg_type]
                    db[index2+start_pos-1 :index2+end_pos] |= 2 ** REGULATORY_REGIONS_ORDER[seg_type]

    f.close()
    return db


def main():
    """
    Create regulations DB in .npy file from the gff file.
    The GFF path and the path where the DB will be stored are received as input from the user.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("regulation_file", help="path to the match_regulations file")
    parser.add_argument("regulation_db_file", help="path to the match_regulations DB will be saved")
    args = parser.parse_args()
    db = init_regulations_db(args.regulation_file)
    np.save(Path(args.regulation_db_file), db)


if __name__ == '__main__':
    main()