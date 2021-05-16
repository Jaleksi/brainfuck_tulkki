from argparse import ArgumentParser

class BFParser:
    '''
        input_mode (int): are given arguments to bfparser treated as decimals
                          or bytes. 0=bytes, 1=decimals
        output_mode (int): when printing in bf is output shown as decimals or
                           bytes. 0=bytes, 1=decimals
        cell_count (int): number of cells in bf "tape"
    '''
    def __init__(
        self,
        input_mode=0,
        output_mode=1,
        cell_count=30_000
    ):
        self.output = ''
        self.input_mode = input_mode
        self.output_mode = output_mode
        self.cell_count = cell_count
        self.pointer = 0
        self.cells = [0 for _ in range(self.cell_count)]
        self.loop_stack = []
        self.character_index = 0

    def cleanup(self, raw_bf):
        bf = ''.join([c for c in raw_bf if c in '><,.[]+-'])
        if bf.count('[') != bf.count(']'):
            raise SyntaxError('bracket count doesn\'t match')
        return bf

    def parse(self, raw_bf):
        bf_code = self.cleanup(raw_bf)

        while self.character_index < len(bf_code):
            match bf_code[self.character_index]:
                case '>':
                    self.pointer += 1
                    if self.pointer > self.cell_count:
                        raise OverflowError
                case '<':
                    self.pointer -= 1
                    if self.pointer < 0:
                        raise OverflowError('underflow')
                case ',':
                    val = input('Input: ')
                    val = int(val) if self.input_mode == 1 else ord(val)
                    self.cells[self.pointer] = val
                case '.':
                    val = self.cells[self.pointer]
                    val = int(val) if self.output_mode == 1 else chr(val)
                    self.output += str(val)
                case '[':
                    if self.cells[self.pointer] == 0:
                        while bf_code[self.character_index] != ']':
                            self.character_index += 1
                        continue
                    self.loop_stack.append(self.character_index + 1)
                case ']':
                    if self.cells[self.pointer] != 0:
                        self.character_index = self.loop_stack[-1]
                        continue
                    self.loop_stack.pop()
                case '+':
                    self.cells[self.pointer] += 1
                case '-':
                    self.cells[self.pointer] -= 1

            self.character_index += 1

        if self.output:
            end = '' if self.output_mode == 0 else '\n'
            print(self.output, end=end)

if __name__ == '__main__':
    parser = ArgumentParser(description='Interpreter for brainfuck')
    parser.add_argument('file_path', type=str, help='Path to bf-file')
    parser.add_argument('--input-mode', type=int, default=0, help='0=bytes, 1=decimal')
    parser.add_argument('--output-mode', type=int, default=0, help='0=bytes, 1=decimal')
    args = parser.parse_args()

    with open(args.file_path, 'r') as bf_file:
        raw_bf = bf_file.read()

    bf_parser = BFParser(args.input_mode, args.input_mode)
    bf_parser.parse(raw_bf)
