"""Console script for Data_logger."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for Data_logger."""
    click.echo("Replace this message by putting your code into "
               "Data_logger.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
