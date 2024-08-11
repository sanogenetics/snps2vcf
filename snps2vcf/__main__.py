import logging
import sys
from pathlib import Path

from . import Converter

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
    converter = Converter()

    if len(sys.argv) == 1:
        # No arguments, use stdin and stdout
        stdin = sys.stdin.buffer
        stdout = sys.stdout.buffer
        converter.convert(stdin, stdout)
    elif len(sys.argv) == 3:
        # Two arguments, use input and output files
        input_file = Path(sys.argv[1])
        output_file = Path(sys.argv[2])

        with input_file.open("rb") as infile, output_file.open("wb") as outfile:
            converter.convert(infile, outfile)
    else:
        print("Invalid arguments", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
