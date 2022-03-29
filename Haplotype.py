import sys
from random import randint
from typing import List

class Haplotype:
    def __init__(self, rows: int, cols: int) -> List[List[str]]:
        self.rows = rows
        self.cols = cols
        #self.matrix = [self.generate_haplotype() for _ in range(self.rows)]
        self.matrix = self.read_data()


    def generate_haplotype(self) -> list:
        return [randint(0,1) for _ in range(self.cols)]

    def write_out(self):
        with open('data.txt', 'w') as data:
            for row in range(self.rows):
                for col in range(self.cols):
                    data.write(str(self.matrix[row][col]))
                data.write('\n')

    def read_data(self) -> list:
        retval = []
        with open('data.txt', 'r') as data:
            for line in data.readlines():
                print(line)
                row = []
                for c in line[:-1]:
                    row.append(int(c))
                retval.append(row)
        print(retval)
        return retval


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('ERROR')
        print('Must include number of sequences and sequence length')
        exit()
    num_sequences = int(sys.argv[1])
    seq_len = int(sys.argv[2])
    H = Haplotype(num_sequences, seq_len)
    H.write_out()
