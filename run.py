from notAiess import notAiess
import click
from datetime import datetime

@click.command()
@click.option("--datentime", "-d", help="Starting datetime point")
@click.argument('apikey')
@click.argument('webhook_url')
def main(apikey, webhook_url, datentime):
    dt = datetime.strptime(datentime, '%Y-%m-%dT%H:%M:%S+00:00')
    nA = notAiess(apikey, dt, list(), webhook_url)
    nA.run()

if __name__ == "__main__":
    main()