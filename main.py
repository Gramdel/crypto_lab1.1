import sys

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALPHABET_CAPITAL = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
EXCEPTIONS = ' \t\n.,;:!?-\'"()'
LEN = 33


class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def show_arg_err(argv=None):
    if argv is None:
        print(f'{Color.RED}Invalid number of arguments! Use "-h" or "--help" for help.{Color.END}')
    else:
        print(f'{Color.RED}Invalid arguments: "{argv}"! Use "-h" or "--help" for help.{Color.END}')


def show_file_err(filename):
    print(f'{Color.RED}Could not open file "{filename}"!{Color.END}')


def show_char_warr(character, line_num, char_num):
    print(f'{Color.YELLOW}Found unexpected character "{character}" (line #{line_num}, position #{char_num}){Color.END}')


def show_help():
    print(f'''Usage:
    {Color.BOLD}-d <file> -k <key>{Color.END}
        Takes contents of the file and decodes them using Caesar's cipher.
        Key needs to be an integer in range [-{LEN - 1}; {LEN - 1}]. Decoded file will be called "decoded_<file>".
    {Color.BOLD}-e <file> -k <key>{Color.END}
        Takes contents of the file and encodes them using Caesar's cipher.
        Key needs to be an integer in range [-{LEN - 1}; {LEN - 1}]. Encoded file will be called "encoded_<file>".
    {Color.BOLD}-f <encoded_file> <reference_file>{Color.END}
        Takes contents of encoded file and performs frequency analysis.
        Outputs the frequency of each letter in encoded and reference files.
    {Color.BOLD}-h, --help{Color.END}
        Displays this message.''')


def encode(filename, key, decoding_mode=False):
    if decoding_mode:
        key *= -1
        new_filename = 'decoded_' + filename
    else:
        new_filename = 'encoded_' + filename

    try:
        with open(filename, 'r', encoding='utf8') as file, open(new_filename, 'w', encoding='utf8') as new_file:
            i = 0
            for line in file:
                i += 1
                new_line = ''
                for char in line:
                    if char in EXCEPTIONS:
                        new_line += char
                    elif char in ALPHABET:
                        index = ALPHABET.index(char)
                        new_line += ALPHABET[(index + key) % LEN]
                    elif char in ALPHABET_CAPITAL:
                        index = ALPHABET_CAPITAL.index(char)
                        new_line += ALPHABET_CAPITAL[(index + key) % LEN]
                    else:
                        show_char_warr(char, i, line.index(char) + 1)
                        new_line += char
                new_file.write(new_line)
        print(f'{Color.GREEN}Success! Check file "{new_filename}"{Color.END}')
    except FileNotFoundError:
        show_file_err(filename)


def analyze(en_filename, ref_filename):
    try:
        en_freq = [0] * LEN
        en_sum = 0
        en_max = 0
        with open(en_filename, 'r', encoding='utf8') as en_file:
            for line in en_file:
                for char in line:
                    if char.lower() in ALPHABET:
                        index = ALPHABET.index(char.lower())
                        en_freq[index] += 1
                        en_sum += 1
                        if en_freq[index] > en_freq[en_max]:
                            en_max = index
        ref_freq = [0] * LEN
        ref_sum = 0
        ref_max = 0
        with open(ref_filename, 'r', encoding='utf8') as ref_file:
            for line in ref_file:
                for char in line:
                    if char.lower() in ALPHABET:
                        index = ALPHABET.index(char.lower())
                        ref_freq[index] += 1
                        ref_sum += 1
                        if ref_freq[index] > ref_freq[ref_max]:
                            ref_max = index
        for i in range(0, LEN):
            print(Color.BLUE, ALPHABET_CAPITAL[i], Color.END,
                  "{:.3f}".format(en_freq[i] / en_sum), "{:.3f}".format(ref_freq[i] / ref_sum))
        print(
            f'\n{Color.BOLD}Most frequent letter in encoded text:\t {Color.GREEN}{ALPHABET_CAPITAL[en_max]}{Color.END} ({"{:.3f}".format(en_freq[en_max] / en_sum)})')
        print(
            f'{Color.BOLD}Most frequent letter in referenced text: {Color.GREEN}{ALPHABET_CAPITAL[ref_max]}{Color.END} ({"{:.3f}".format(ref_freq[ref_max] / ref_sum)})')

    except FileNotFoundError as e:
        show_file_err(e.filename)


if __name__ == '__main__':
    argc = len(sys.argv)
    if (argc < 2) | (argc == 3) | (argc > 5):
        show_arg_err()
    elif argc == 2:
        if (sys.argv[1] == "-h") | (sys.argv[1] == "--help"):
            show_help()
        else:
            show_arg_err(sys.argv[1])
    elif argc == 4:
        if sys.argv[1] == "-f":
            analyze(sys.argv[2], sys.argv[3])
        else:
            show_arg_err(sys.argv[1])
    else:
        try:
            k = int(sys.argv[4])
            if ((sys.argv[1] != "-d") & (sys.argv[1] != "-e")) | (sys.argv[3] != "-k") | (k > LEN - 1) | (k < -LEN + 1):
                raise ValueError
            encode(sys.argv[2], k, sys.argv[1] == "-d")
        except ValueError:
            show_arg_err(' '.join(sys.argv[1:]))
