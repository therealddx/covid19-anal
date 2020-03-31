import os # for file i/o

def ExtractState_FromFile(arg_stateName, arg_csvFile):
  # 
  # Grab records that pertain to Utah.
  # 
  #   find all records that have "Utah" in that column. (state record)
  # 
  #   for each state record:
  #     find the value of those columns.
  # 
  # get the sum of all: Confirmed, Deaths, Recovered for any given state.
  # 

  # 1. open file.
  csvFileReader = open(arg_csvFile)

  # 2. find out which columns show key information.
  debug = False

  # 2a. get the first record.
  prototypeRecord = csvFileReader.readline().split(',')

  # 2b. predicate search: "Province/State"
  stateIndex = 0 # output of this step.
  for eachField in prototypeRecord:
    if "province" in eachField.lower() and "state" in eachField.lower():
      break
    stateIndex += 1

  # 2c. predicate search: "Confirmed"
  confirmedIndex = 0
  for eachField in prototypeRecord:
    if "confirmed" in eachField.lower():
      break
    confirmedIndex += 1

  # 2d: predicate search: "Deaths"
  deathsIndex = 0
  for eachField in prototypeRecord:
    if "deaths" in eachField.lower():
      break
    deathsIndex += 1

  # 2e: predicate search: "Recovered"
  recoveredIndex = 0
  for eachField in prototypeRecord:
    if "recovered" in eachField.lower():
      break
    recoveredIndex += 1

  if debug:
    print(str(stateIndex) + ", " +
      str(confirmedIndex) + ", " +
      str(deathsIndex) + ", " +
      str(recoveredIndex))

  # 3. obtain all records specific to this state.
  stateRecords = []
  for eachLine in csvFileReader:
    if eachLine.split(',')[stateIndex] == arg_stateName:
      stateRecords.append(eachLine)

  if debug:
    for eachItem in stateRecords:
      print(eachItem)

  # 4. aggregate state records into one sum for this state.
  cumConfirmed = 0
  cumDeaths = 0
  cumRecovered = 0
  for eachRecord in stateRecords:
    cumConfirmed += int(eachRecord.split(',')[confirmedIndex])
    cumDeaths    += int(eachRecord.split(',')[deathsIndex])
    cumRecovered += int(eachRecord.split(',')[recoveredIndex])

  # 5. obtain the date.
  fileDate = \
    arg_csvFile[arg_csvFile.rindex('/') + 1:].replace(".csv", "")

  # 6. print the report for this day.
  # date:
  #   Confirmed:
  #   Deaths:
  #   Recovered:
  if debug:
    print("Date: " + fileDate)
    print("  Confirmed : " + str(cumConfirmed) )
    print("  Deaths    : " + str(cumDeaths)    )
    print("  Recovered : " + str(cumRecovered) )

  # 7. return the object.
  #   { "DATE" : fileDate
  #   , "CONFIRMED" : cumConfirmed
  #   , "DEATHS" : cumDeaths
  #   , "RECOVERED" : cumRecovered }
  toReturn = {}
  toReturn["DATE"] = fileDate
  toReturn["CONFIRMED"] = cumConfirmed
  toReturn["DEATHS"] = cumDeaths
  toReturn["RECOVERED"] = cumRecovered

  # ret.
  return toReturn

def main():

  # args.
  targetState = "Utah"
  csvDirectory = \
    "../covid19-data/csse_covid_19_data/csse_covid_19_daily_reports/"

  # create output file.
  outputCsvFile = "./covid19_analyzer.csv"
  if os.path.exists(outputCsvFile):
    os.remove(outputCsvFile)
  outputFile = open("./covid19_analyzer.csv", "a")
  outputFile.write("Aggregated State Data for: " + targetState + "\n")
  outputFile.write("DATE,CONFIRMED,DEATHS,RECOVERED" + "\n")

  # find available dates.
  allDateFiles = []
  for rootDir, allDirs, allFiles in os.walk(csvDirectory):
    for eachFile in allFiles:
      if eachFile.endswith(".csv"): # predicate.
        allDateFiles.append(eachFile)

  # for each date that exists:
  for eachDateFile in allDateFiles:

    # get the data object on it.
    dayDict = \
      ExtractState_FromFile(targetState,
        csvDirectory + eachDateFile)

    # output it.
    outputFile.write(
      str(dayDict["DATE"]) + "," +
      str(dayDict["CONFIRMED"]) + "," +
      str(dayDict["DEATHS"]) + "," +
      str(dayDict["RECOVERED"]) + "\n")

  # close.
  outputFile.close()

# 
# run.
# 
main()

