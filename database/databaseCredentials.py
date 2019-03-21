import csv


class Credentials:
    with open('./database/database_credentials.csv', 'r') as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in readcsv:
            user_name = row[0]
            password = row[1]
            host = row[2]
            port = row[3]
            database_name = row[4]

    def getDatabaseCredentials(self):
        return self
