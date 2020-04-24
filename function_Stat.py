from models import Stat, Country, Users


def search(country_name):
    try:
        stat = Stat.get(Stat.country_name == country_name)
    except:
        return False

    l = []
    l.append(stat.country_name)
    l.append(stat.cases)
    l.append(stat.deaths)
    l.append(stat.total_recovered)
    l.append(stat.new_cases)
    l.append(stat.new_deaths)
    l.append(str(stat.updated))
    return l


def top_10():
    top10_country = []
    top10_cases = []
    i = 0
    try:
        Stats = Stat.select().order_by(-Stat.cases)
        for stat in Stats:
            i += 1
            if i > 1:
                top10_country.append(stat.country_name)
                top10_cases.append(stat.cases)
            if i == 11:
                break
    except:
        return False

    return top10_country, top10_cases


def changei(country_name):
    a = list(country_name)
    for i in range(len(a)):
        if a[i] == "і":
            a[i] = "i"
        elif a[i] == "І":
            a[i] = "I"
    return "".join(a)


def translate_country(country_name, froom):
    if country_name == "world":
        return country_name
    if froom == "Ukrainian":
        country_name = changei(country_name)
        country = Country.get(Country.Ukrainian == country_name)
    elif froom == "Russian":
        country = Country.get(Country.Russian == country_name)
    elif froom == "Belorussian":
        country = Country.get(Country.Belorussian == country_name)
    elif froom == "English":
        country = Country.get(Country.English == country_name)
    elif froom == "Spanish":
        country = Country.get(Country.Spanish == country_name)
    elif froom == "German":
        country = Country.get(Country.German == country_name)
    elif froom == "French":
        country = Country.get(Country.French == country_name)
    elif froom == "Italian":
        country = Country.get(Country.Italian == country_name)
    elif froom == "Japanese":
        country = Country.get(Country.Japanese == country_name)
    elif froom == "Latvian":
        country = Country.get(Country.Latvian == country_name)
    elif froom == "Czech":
        country = Country.get(Country.Czech == country_name)
    try:
        a = country.English
        return a
    except:
        return False


def translate_country_en(country_name, to):
    if to == "Ukrainian":
        country = Country.get(Country.English == country_name)
        return country.Ukrainian
    elif to == "Russian":
        country = Country.get(Country.English == country_name)
        return country.Russian
    elif to == "Belorussian":
        country = Country.get(Country.English == country_name)
        return country.Belorussian
    elif to == "English":
        country = Country.get(Country.English == country_name)
        return country.English
    elif to == "Spanish":
        country = Country.get(Country.English == country_name)
        return country.Spanish
    elif to == "German":
        country = Country.get(Country.English == country_name)
        return country.German
    elif to == "French":
        country = Country.get(Country.English == country_name)
        return country.French
    elif to == "Italian":
        country = Country.get(Country.English == country_name)
        return country.Italian
    elif to == "Japanese":
        country = Country.get(Country.English == country_name)
        return country.Japanese
    elif to == "Latvian":
        country = Country.get(Country.English == country_name)
        return country.Latvian
    elif to == "Czech":
        country = Country.get(Country.English == country_name)
        return country.Czech
    else:
        return False


def C(str1):
    str1 = list(str(str1))
    str1.reverse()
    str2 = []
    for i in range(len(str1)):
        if i % 3 == 0 and i != 0:
            str2.append(",")
        str2.append(str1[i])

    str2.reverse()
    return "".join(str2)
