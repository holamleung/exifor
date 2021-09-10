from PIL import Image, ExifTags
from datetime import datetime
from fractions import Fraction

FILEPATH = "/home/holam/Projects/imfo/sources/test8.jpg"


def exif_tag(raw):
    tagged = {}
    for key, val in raw.items():
        tagged[ExifTags.TAGS[key]] = val
        if key == "GPSInfo":
            gpstagged = gps_tag(tagged["key"])
    return tagged


def exif_extract(tagged):
    targets= [
        "ExifImageWidth",
        "ExifImageHeight",
        "Make",
        "Model",
        "DateTimeOriginal",
        "OffsetTimeOriginal",
        # "ShutterSpeedValue",
        "ExposureTime",
        "FNumber",
        "FocalLength",
        "LensModel",
        "ISOSpeedRatings",
        "GPSInfo"
    ]
    extracted = {}
    for tag in tagged:
        if tag in targets:
                extracted[tag] = tagged[tag]
    return extracted


def gps_tag(gps):
    gps_tagged = {}
    for key, val in gps.items():
        gps_tagged[ExifTags.GPSTAGS[key]] = val
    return gps_tagged

def gps_convert(dms, ref):
    deg = dms[0]
    min = dms[1] / 60
    sec = dms[2] / 3600
    dms_converted = float(deg + min + sec)
    if ref in ["S", "W"]:
        dms_converted = -dms_converted
    return round(dms_converted, 5)


def gps_coordinate(extracted):
    gpstagged = gps_tag(extracted)
    lat = gps_convert(gpstagged["GPSLatitude"], gpstagged["GPSLatitudeRef"])
    lon = gps_convert(gpstagged["GPSLongitude"], gpstagged["GPSLongitudeRef"])
    return (lat, lon)


def time_convert(extracted):
    ptime = "%Y:%m:%d %H:%M:%S"
    ftime = "%b %d, %Y %H:%M:%S"
    try:
        time_converted = "{} {}".format(extracted["DateTimeOriginal"], extracted["OffsetTimeOriginal"])
        ptime += " %z"
        ftime += " %Z"
    except KeyError:
        time_converted = extracted["DateTimeOriginal"]
    time_converted = datetime.strptime(time_converted, ptime).strftime(ftime)
    return time_converted


def shutter_convert(shutter):
    if shutter < 1:
        denominator = round(1 / shutter)
        shutter_converted = Fraction(1, denominator)
    else:
        shutter_converted = raw
    return shutter_converted


def exif_convert(extracted):
    convert = {}
    for tag in extracted:
        if tag == "ExifImageWidth" or tag == "ExifImageHeight":
            if "Resolution" not in convert:
                pixel_count = extracted["ExifImageWidth"] * extracted["ExifImageHeight"] / 1000000
                convert["Resolution"] = "{} x {} ({:.2f} MP)".format(extracted["ExifImageWidth"], extracted["ExifImageHeight"], pixel_count)
        elif tag == "DateTimeOriginal":
            convert["CaptureTime"] = time_convert(extracted)
        elif tag == "Model":
            convert["Camera"] = extracted["Make"] + " " + extracted["Model"]
        elif tag == "LensModel":
            convert["Lens"] = extracted["LensModel"]
        elif tag == "FocalLength":
            convert["FocalLength"] = "{} mm".format(extracted["FocalLength"])
        elif tag == "ExposureTime":
            shutter = shutter_convert(extracted["ExposureTime"])
            convert["ShutterSpeeds"] = "{} sec".format(shutter)
        elif tag == "FNumber":
            convert["F/stops"] = "f/{}".format(extracted["FNumber"])
        elif tag == "ISOSpeedRatings":
            convert["ISO"] = extracted["ISOSpeedRatings"]
        elif tag == "GPSInfo":
            convert["GEOLocation"] = gps_coordinate(extracted["GPSInfo"])
    return convert


try:
    with Image.open(FILEPATH) as img:
        img_raw = img._getexif()
        # img_format = img.format
        # print(img_format)
        if img_raw != None:
            # print(img_raw)
            img_tagged = exif_tag(img_raw)
            #print(img_tagged)
            img_extracted = exif_extract(img_tagged)
            print(img_extracted)
            img_converted = exif_convert(img_extracted)
            print(img_converted)
        else:
            print("No EXIF data")
except FileNotFoundError:
        print("File Not Found")
except OSError:
        print("Cannot open file")