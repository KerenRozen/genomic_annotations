import gzip

from services.consts import CHROMOSOME_TO_INT_GH38, GH38_GENOME, CLASSIFICATIONS_ORDER_GH38
from services.match_classifications.match_classifications import decode_strand

def build(chr, start, end, s):
    types = set()
    with gzip.open(GH38_GENOME, 'rt') as f:
        for row in f:
            if not row.startswith('#'):
                fields = row.strip().split('\t')
                seg_type = fields[2]
                if fields[2] != 'chromosome':
                    chromosome = CHROMOSOME_TO_INT_GH38[fields[0]]
                    start_pos = int(fields[3])
                    end_pos = int(fields[4])
                    strand = fields[6]
                    if chr == chromosome and decode_strand(s) == strand and start <= end_pos and end >= start_pos:
                        types.add(seg_type)
    f.close()
    print(types)
    l = [0] * 25
    for t in types:
        l[24-CLASSIFICATIONS_ORDER_GH38[t]] = 1
    print(l)


if __name__ == '__main__':
    build(1, 235448349, 235448440, 15)
    build(10, 112445437, 112445650, 16)
    build(11, 407315, 414923, 16)
    build(12, 45050420, 45051603, 15)
    build(14, 21269298, 21269410, 16)
    build(3, 100, 300, 15)
    build(18, 641327, 641541, 15)
    build(23, 51340284, 51340402, 16)
#    build(68, 300, 800, 15)