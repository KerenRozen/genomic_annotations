import argparse
import gzip
import numpy as np
from pathlib import Path

from services.consts import CHROMOSOME_TO_INT_GH37, CHROMOSOME_TO_INT_GH38, CELL_TYPES_LABELS, PARTIAL_SUMS_GH37, \
    PARTIAL_SUMS_GH38

ENCYCLOPEDIA_LENGTH = {
    37: 164785,
    38: 164738
}
GENOME_LENGTH = {
    37: 3101804739,
    38: 3099411205,
}
PARTIAL_SUMS = {
    37: PARTIAL_SUMS_GH37,
    38: PARTIAL_SUMS_GH38
}
CHROMOSOME_TO_INT = {
    37: CHROMOSOME_TO_INT_GH37,
    38: CHROMOSOME_TO_INT_GH38
}


def init_db(input_file, reference_genome):
    """
    Using '2 lists' method.
    Input:  input_file- path to 'segway_encyclopedia.bed'
            reference_genome- 37 for gh37 or 38 for gh38
    The file has 164785 rows. It contains segments from chromosomes 1-22 | 'X'.
    """
    chromosome_int = CHROMOSOME_TO_INT[reference_genome]
    partial_sums = PARTIAL_SUMS[reference_genome]
    genome_length = GENOME_LENGTH[reference_genome]
    nucleotides_db = np.zeros(genome_length, dtype=np.uintc)
    values_db = np.empty([ENCYCLOPEDIA_LENGTH[reference_genome]+1,3],dtype=object)
    values_db[0] = np.array([np.float16(0), np.float16(0), np.array([0 for i in range(164)], dtype=np.uint8)], dtype=np.object)
    with gzip.open(Path(input_file), 'rt') as f:
        next(f) # Skip header
        for line_number, row in enumerate(f, start=1):
            fields = row.strip().split('\t')
            chromosome = chromosome_int[fields[0][3:]] if '_' not in fields[0] else chromosome_int[fields[0][3:fields[0].index('_')]]
            start = int(fields[1])
            end = int(fields[2])
            values_db[line_number][0] = np.float16(fields[3]) # sum_score
            values_db[line_number][1] = np.float16(fields[4]) # mean_score
            cells = np.array([CELL_TYPES_LABELS[fields[i]] for i in range(5, 169)], dtype=np.uint8)
            values_db[line_number][2] = cells # cell types annotations
            index = partial_sums[chromosome-1]
            nucleotides_db[index+start-1:index+end] = line_number

    f.close()

    return nucleotides_db, values_db


def main():
    """
    Receives from user: path to segway_encyclopedia.bed file, path to save nucleotides_DB, path to save annotations_DB,
                        genome_reference (37 or 38)
    :return: Saves 2 .npz files: the nucleotides DB and the annotations DB.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("functional_DNA_elements", help="path to segway_encyclopedia.bed file")
    parser.add_argument("db_file", help="path to save DB file")
    parser.add_argument("genome_reference", help="37 for gh37 or 38 for gh38")
    args = parser.parse_args()
    nucleotides_db, values_db = init_db(args.functional_DNA_elements, int(args.genome_reference))
    np.savez_compressed(args.db_file, nucleotides_db, values_db)


if __name__ == '__main__':
    main()