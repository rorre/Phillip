from notAiess import notAiess
import click
from datetime import datetime

@click.command()
@click.option("--datentime", "-d", help="Starting datetime point")
@click.argument('apikey')
@click.argument('hookurl')
def main(apikey, hookurl, datentime):
    dt = datetime.strptime(datentime, '%Y-%m-%dT%H:%M:%S+00:00')
    nA = notAiess(apikey, hookurl, dt)
    nA.run()

if __name__ == "__main__":
    main()