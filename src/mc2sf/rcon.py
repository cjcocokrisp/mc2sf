from rcon import Client
from mc2sf.util import calc_file_size_with_units, get_time_units


def rcon_prepare_for_backup(ip: str, port: int, pwd: str):
    with Client(ip, port, passwd=pwd) as client:
        client.run(
            "say",
            "A backup of this server is starting, saving will be temporarily be disabled and all changes will be saved in RAM so if the server goes down it will not be saved. Another message will be sent when the backup is complete.",
        )

        client.run("save-all")
        client.run("save-off")


def recon_cleanup(ip: str, port: int, pwd: str, elapsed, file_details):
    file_size, size_units = calc_file_size_with_units(file_details)
    time_units = get_time_units(elapsed)

    with Client(ip, port, passwd=pwd) as client:
        client.run("save-on")
        client.run(
            "say",
            f"The backup has been completed in {round(elapsed, 2)} {time_units} with a size of {round(file_size, 2)} {size_units}. Saving has been turned back on.",
        )
