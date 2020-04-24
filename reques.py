import requests
import ast


def worldstat():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php"

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "72adbb094emshe766e14b9e3094bp137dfejsne3ea26f76000"
    }

    response = requests.request("GET", url, headers=headers)
    response = response.text

    response = dict(ast.literal_eval(response))


    return response


def cases_by_country():
    url1 = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"

    headers1 = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "72adbb094emshe766e14b9e3094bp137dfejsne3ea26f76000"
    }

    response1 = requests.request("GET", url1, headers=headers1)
    response1 = response1.text
    response1 = dict(ast.literal_eval(response1))
    return response1

if __name__ == "__main__":
    cases_by_country()
