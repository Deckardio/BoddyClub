import sys
import time
import click


@click.command()
@click.argument("log_filename", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def start(log_filename: str):
    sys.stdout.reconfigure(encoding='ISO-8859-1')
    with open(log_filename, 'r', encoding='ISO-8859-1') as rr:
        for line in rr:
            line = line + '\n'
            sys.stdout.write(line)
            # print(line)
            time.sleep(0.01)


if __name__ == "__main__":
    start()
