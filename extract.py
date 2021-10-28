from datetime import datetime
from fractions import Fraction
from sys import argv

from PIL import ExifTags, Image


# tag values to corresponding exif tags
def exif_tag(raw):
    tagged = {}
    for key, val in raw.items():
        try:
            tagged[ExifTags.TAGS[key]] = val
        except KeyError:
            pass
    return tagged


# extract specificed tags
def exif_extract(tagged):
    targets= ["ExifImageWidth", "ExifImageHeight", "Make", "Model",
             "DateTimeOriginal", "OffsetTimeOriginal", "ExposureTime",
             "FNumber", "FocalLength", "LensModel", "ISOSpeedRatings",
             "ImageDescription", "GPSInfo"]
    extracted = {}
    for tag in tagged:
        if tag in targets:
                extracted[tag] = tagged[tag]
    return extracted


# tag values to corresponding GPS tag
def gps_tag(gps):
    gps_tagged = {}
    for key, val in gps.items():
        try:
            gps_tagged[ExifTags.GPSTAGS[key]] = val
        except KeyError:
            pass
    return gps_tagged


# calculate the latitude/longitude
def gps_convert(dms, ref):
    deg = dms[0]
    min = dms[1] / 60
    sec = dms[2] / 3600
    dms_converted = float(deg + min + sec)
    if ref in ["S", "W"]:
        dms_converted = -dms_converted
    return round(dms_converted, 5)


# convert the gps coordinate
def gps_coordinate(extracted):
    gpstagged = gps_tag(extracted)
    lat = gps_convert(gpstagged["GPSLatitude"], gpstagged["GPSLatitudeRef"])
    lon = gps_convert(gpstagged["GPSLongitude"], gpstagged["GPSLongitudeRef"])
    return (lat, lon)


# convert date and time value to more reader-friendly
def time_convert(extracted):
    ptime = "%Y:%m:%d %H:%M:%S"
    ftime = "%b %d, %Y %H:%M:%S"
    try:
        time_converted = "{} {}".format(extracted["DateTimeOriginal"],
             extracted["OffsetTimeOriginal"])
        ptime += " %z"
        ftime += " %Z"
    except KeyError:
        time_converted = extracted["DateTimeOriginal"]
    time_converted = datetime.strptime(time_converted, ptime).strftime(ftime)
    return time_converted


# convert shutter value to fraction format
def shutter_convert(shutter):
    if shutter < 1:
        denominator = round(1 / shutter)
        shutter_converted = Fraction(1, denominator)
    else:
        shutter_converted = shutter
    return shutter_converted


# convert exif data to human conventional
def exif_convert(extracted):
    convert = dict.fromkeys(["Resolution", "Capture Time", "Camera", "Lens",
                             "Focal Length", "Shutter Speeds", "F/stops",
                             "ISO", "Geolocation"])
    for tag in extracted:
        if tag == "ExifImageWidth" or tag == "ExifImageHeight":
            if convert["Resolution"] == None:
                pixel_count = (extracted["ExifImageWidth"]
                     * extracted["ExifImageHeight"] / 1000000)
                convert["Resolution"] = "{} x {} ({:.2f} MP)".format(
                    extracted["ExifImageWidth"], extracted["ExifImageHeight"],
                     pixel_count)
        elif tag == "DateTimeOriginal":
            convert["Capture Time"] = time_convert(extracted)
        elif tag == "Model":
            convert["Camera"] = extracted["Make"] + " " + extracted["Model"]
        elif tag == "LensModel":
            convert["Lens"] = extracted["LensModel"]
        elif tag == "FocalLength":
            convert["Focal Length"] = "{} mm".format(extracted["FocalLength"])
        elif tag == "ExposureTime":
            shutter = shutter_convert(extracted["ExposureTime"])
            convert["Shutter Speeds"] = "{} sec".format(shutter)
        elif tag == "FNumber":
            convert["F/stops"] = "f/{}".format(extracted["FNumber"])
        elif tag == "ISOSpeedRatings":
            convert["ISO"] = extracted["ISOSpeedRatings"]
        elif tag == "ImageDescription":
            convert["Description"] = extracted["ImageDescription"]
        elif tag == "GPSInfo":
            convert["Geolocation"] = gps_coordinate(extracted["GPSInfo"])
    return convert


def process(file):
    try:
        img = Image.open(file)
    except FileNotFoundError:
        return print("File Not Found")
    except OSError:
        return print("Cannot open file")
    img.close()
    img_raw = img._getexif()
    if img_raw == None:
        return print("No exif data")
    img_tagged = exif_tag(img_raw)
    img_extracted = exif_extract(img_tagged)
    img_converted = exif_convert(img_extracted)
    return img_converted

if __name__ == "__main__":
    print(process(argv[1]))
