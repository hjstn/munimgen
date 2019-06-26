import csv
from os import path
from PIL import Image, ImageOps, ImageDraw, ImageFont

fontPath = path.abspath("HelveticaNowDisplayXBlk.otf")

countriesErratumReader = csv.DictReader(open("countries_erratum.csv", "r"))

countries = {}

with open("countries.csv", "r") as countriesCSV:
    countriesReader = csv.reader(countriesCSV)

    next(countriesReader, None)
    for countryLine in countriesReader:
        countries[countryLine[1]] = countryLine[0]

with open("countries_erratum.csv", "r") as countriesCSV:
    countriesReader = csv.reader(countriesCSV)

    next(countriesReader, None)
    for countryLine in countriesReader:
        countries[countryLine[1]] = countryLine[0]

def generateFlag(iso, wh):
    countryFlag = Image.open("flags/{0}.png".format(iso.lower()))
    countryFlag.load()

    countryFlag.thumbnail((wh - 2, wh - 2))

    pad_w = (wh - countryFlag.width - 2) // 2
    pad_h = (wh - countryFlag.height - 2) // 2

    pad = (pad_w, pad_h, pad_w, pad_h)

    return ImageOps.expand(ImageOps.expand(countryFlag, (1, 1), (0, 0, 0)), pad)

def getFont(size):
    return ImageFont.truetype(fontPath, size)

def scaleText(text, w, h):
    fontSize = 1

    font = getFont(1)

    textSize = font.getsize(text)

    while textSize[0] < w and textSize[1] < h:
        font = getFont(fontSize)
        fontSize += 1

        textSize = font.getsize(text)
    
    fontSize -= 1
    font = getFont(fontSize)

    return font

def drawText(placardDraw, text, w, h, x, y):
    font = scaleText(text, w, h)

    textSize = font.getsize(text)

    offset = font.getoffset(text)

    pad_w = (w - textSize[0] - offset[0]) // 2
    pad_h = (h - textSize[1] - offset[1]) // 2

    xy = (x + pad_w, y + pad_h)

    placardDraw.text(xy, text, (0, 0, 0), font)

def generatePlacard(committee, iso):
    committeeImg = Image.open("committees/{0}.png".format(committee))
    committeeImg.load()

    placard = Image.new("RGBA", committeeImg.size)

    placard.paste(committeeImg, (0, 0))

    flagImg = generateFlag(iso, 512)

    placard.paste(flagImg, (130, 320), mask=flagImg)

    placardDraw = ImageDraw.Draw(placard)

    drawText(placardDraw, countries[iso.upper()], 1236, 200, 682, 478)

    return placard

def generateDoublePlacard(committee, iso):
    placard = generatePlacard(committee, iso)

    privilegeImg = Image.open("privilege.png")
    privilegeImg.load()

    dPlacard = Image.new("RGBA", (placard.size[0], (placard.size[1] * 2) + 3), (0, 0, 255))

    dPlacard.paste(privilegeImg.rotate(180), (0, 0))

    dPlacard.paste(placard, (0, placard.size[1] + 3))

    dPlacard.save("output/{0}_{1}.png".format(committee, iso))

dataReader = csv.reader(open("data.csv", "r"))

committees = list(dataReader)

for committee in committees:
    for country in committee[1:]:
        generateDoublePlacard(committee[0], country)