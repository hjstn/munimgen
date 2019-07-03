import csv
from os import path
from PIL import Image, ImageOps, ImageDraw, ImageFont

# Colors

textColor = (0, 0, 0)
flagBorderColor = (0, 0, 0)
placardBorderColor = (0, 0, 255)
backgroundColor = (255, 255, 255)

# Pixel Constants

committeePadding = 512

flagPadding = 130
flagSize = 768

textHeight = 200
textPadding = 40

defaultFontSize = 40

# Globals

countries = {}
flags = {}

# Files

fontPath = path.abspath("HelveticaNowDisplayXBlk.otf")

# External Data

with open("countries.csv", "r") as countriesCSV:
    countriesReader = csv.reader(countriesCSV)

    next(countriesReader, None)
    for countryLine in countriesReader:
        countryLine[1] = countryLine[1].upper()
        countries[countryLine[1]] = countryLine[0]

with open("countries_erratum.csv", "r") as countriesCSV:
    countriesReader = csv.reader(countriesCSV)

    next(countriesReader, None)
    for countryLine in countriesReader:
        countryLine[1] = countryLine[1].upper()
        countries[countryLine[1]] = countryLine[0]
        if len(countryLine) >= 3:
            flags[countryLine[1]] = countryLine[2]

# Functions

def generateFlag(iso, wh):
    countryFlag = Image.open("flags/{0}.png".format(iso.lower()))
    countryFlag.load()

    countryFlag.thumbnail((wh - 2, wh - 2))

    pad_w = (wh - countryFlag.width - 2) // 2
    pad_h = (wh - countryFlag.height - 2) // 2

    pad = (pad_w, pad_h, pad_w, pad_h)

    return ImageOps.expand(ImageOps.expand(countryFlag, (1, 1), flagBorderColor), pad)

def getFont(size):
    return ImageFont.truetype(fontPath, size)

def scaleText(text, w, h):
    fontSize = defaultFontSize
    textSize = (0, 0)

    while textSize[0] < w and textSize[1] < h:
        font = getFont(fontSize)
        fontSize += 1

        textSize = font.getsize(text)
    
    fontSize -= 1
    font = getFont(fontSize)

    return font

def drawText(placardDraw, text, w, h, x, committeeHeight):
    font = scaleText(text, w, h)

    textSize = font.getsize(text)

    offset = font.getoffset(text)

    xy = (x + ((w - textSize[0] - offset[0]) // 2), (committeeHeight - textSize[1] - offset[1]) // 2)

    placardDraw.text(xy, text, textColor, font)

def generatePlacard(committeeImg, flagText, flagImg):
    # Initialization
    placardWidth = committeeImg.size[0] + (committeePadding * 2)

    placard = Image.new("RGBA", (placardWidth, committeeImg.size[1]), backgroundColor)

    placard.paste(committeeImg, (committeePadding, 0))

    # Draw Flag
    placard.paste(flagImg, (flagPadding, (committeeImg.size[1] - flagSize) // 2), mask=flagImg)

    # Draw Text
    placardDraw = ImageDraw.Draw(placard)
    drawText(placardDraw, flagText, (placardWidth - (2 * flagPadding) - flagSize - textPadding), textHeight, flagPadding + flagSize + textPadding, committeeImg.size[1])

    return placard

def generateDoublePlacard(sideA, sideB):
    placardWidth = sideA.size[0] + (2 * committeePadding)

    dPlacard = Image.new("RGBA", (placardWidth, (sideA.size[1] * 2) + 3), backgroundColor)

    dPlacard.paste(sideA.rotate(180), (committeePadding, 0))

    dPlacard.paste(sideB, ((placardWidth - sideB.size[0]) // 2, sideA.size[1] + 3))

    dDraw = ImageDraw.Draw(dPlacard)

    dDraw.rectangle([(0, sideA.size[1]), (placardWidth, sideA.size[1] + 3)], placardBorderColor)

    return dPlacard

# Input

dataList = list(csv.reader(open("data.csv", "r")))

# Preloaded Files

privilegeImg = Image.open("privilege.png")
privilegeImg.load()

# Code

for dataRow in dataList:
    committee = dataRow[0]

    committeeImg = Image.open("committees/{0}.png".format(committee))
    committeeImg.load()

    for iso in dataRow[1:]:
        iso = iso.upper()

        flagText = countries[iso]
        flagImg = generateFlag(flags[iso] if iso in flags else iso, flagSize)

        countryPlacard = generatePlacard(committeeImg, flagText, flagImg)

        finalPlacard = generateDoublePlacard(privilegeImg, countryPlacard)
        finalPlacard.save("output/{0}_{1}.png".format(committee, iso))