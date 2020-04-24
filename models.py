from peewee import (SqliteDatabase, Model, IntegerField, DateTimeField, BooleanField, datetime as peewee_datetime,
                    CharField)
import config
import reques as req


def add_country(country):
    if country["country_name"]:
        a = Stat.create(country_name=country["country_name"], cases=country["cases"].replace(",",""), deaths=country["deaths"].replace(",",""),
                        total_recovered=country["total_recovered"].replace(",",""), new_deaths=0, new_cases=0)
        a.save()


def add_world(country):
    a = Stat.create(country_name="world", cases=country["total_cases"].replace(",",""), deaths=country["total_deaths"].replace(",",""),
                    total_recovered=country["total_recovered"].replace(",",""), new_deaths=0, new_cases=0)

    a.save()


db = SqliteDatabase(config.DB_NAME)


class _Stat(Model):
    class Meta:
        database = db


class Stat(_Stat):
    country_name = CharField(max_length=15, index=True)
    cases = IntegerField()
    deaths = IntegerField()
    total_recovered = IntegerField()
    new_deaths = IntegerField()
    new_cases = IntegerField()
    updated = DateTimeField(default=peewee_datetime.datetime.now)

    class Meta:
        db_table = "stat"
        order_by = ("cases")

    def __str__(self):
        return "Country: %s, cases: %s, deaths: %s, total recovered: %s, new deaths: %s, new cases: %s, updated: %s" % (
            self.country_name, self.cases, self.deaths, self.total_recovered, self.new_deaths, self.new_cases,
            self.updated)


class Country(_Stat):
    Russian = CharField()
    Ukrainian = CharField()
    Belorussian = CharField()
    English = CharField()
    Spanish = CharField()
    Portuguese = CharField()
    German = CharField()
    French = CharField()
    Italian = CharField()
    Polish = CharField()
    Japanese = CharField()
    Lithuanian = CharField()
    Latvian = CharField()
    Czech = CharField()

    class Meta:
        db_table = "country_names"
        order_by = ("English",)

    def __str__(self):
        return "Russian: %s\nUkrainian: %s\nBelorussian: %s\nEnglish: %s\nSpanish: %s\nPortuguese: %s\nGerman: %s\nFrench: %s\nItalian: %s\nPolish: %s\nJapanese: %s\nLithuanian: %s\nLatvian: %s\nCzech: %s" % (
            self.Russian, self.Ukrainian, self.Belorussian, self.English, self.Spanish, self.Portuguese, self.German,
            self.French, self.Italian, self.Polish, self.Japanese, self.Lithuanian, self.Latvian, self.Czech)


class Users(_Stat):
    user_id = IntegerField()
    ua = BooleanField(default=False)
    ru = BooleanField(default=False)
    uk = BooleanField(default=False)
    us = BooleanField(default=False)

    class Meta:
        db_table = "users_id"

    def __str__(self):
        return "User_id: %s, ua - %s, ru - %s, uk - %s, us - %s" % (self.user_id, self.ua, self.ru, self.uk, self.us)


def init_db():
    db.drop_tables(Stat)
    Stat.create_table()
    Statistic = req.cases_by_country()["countries_stat"]
    count = 0

    for i in Statistic:
        add_country(Statistic[count])
        count += 1

    add_world(req.worldstat())

    print("db created!")


def init_dbc(ll):
    Country.create_table()
    for i in ll:
        Country.create(Russian=i[1], Ukrainian=i[2], Belorussian=i[3], English=i[4], Spanish=i[5], Portuguese=i[6],
                       German=i[7], French=i[8], Italian=i[9],
                       Polish=i[10], Japanese=i[11], Lithuanian=i[12], Latvian=i[13], Czech=i[14])

    print("db_country created!")


def init_users():
    db.drop_tables(Users)
    Users.create_table()
