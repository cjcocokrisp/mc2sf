def calc_file_size_with_units(file_details):
    upload_size = file_details["size"] / 1000000000
    size_units = "GB"
    if upload_size < 1:
        upload_size = upload_size * 1000
        size_units = "MB"

    return (upload_size, size_units)


def get_time_units(time):
    time_units = "sec"
    if time > 60:
        time = time / 60
        time_units = "min"

    if time > 60:
        time = time / 60
        time_units = "hrs"

    return time, time_units
