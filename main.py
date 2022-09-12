import typer
import downloader
import config


def main(url: str):
    downloader.send_fic(url, config.email_address, config.password, config.kindle_email)


if __name__ == "__main__":
    typer.run(main)