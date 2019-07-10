from notAiess import notAiess
import click

@click.command()
@click.argument('apikey')
@click.argument('hookurl')
def main(apikey, hookurl):
    nA = notAiess(apikey, hookurl)
    nA.run()

if __name__ == "__main__":
    main()