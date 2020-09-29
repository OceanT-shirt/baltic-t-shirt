from sqlalchemy import MetaData, create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

metadata = MetaData()
engine = create_engine('sqlite:///user_database', connect_args={'check_same_thread': False}, echo=False)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    city_climate = Column(String)
    city_meteo_data = relationship("Meteo", backref="city")


class Expense(Base):
    __tablename__ = 'expense'
    expense_id = Column(Integer, primary_key=True)
    expense_type = Column(String)
    unit = Column(String)
    expense_detail_data = relationship("ExpenseData", backref="expense")


class Meteo(Base):
    __tablename__ = 'meteo'
    id = Column(Integer, primary_key=True)
    city_id = Column(ForeignKey('city.city_id'))
    month = Column(String)
    average_humidity = Column(Integer)
    average_temperature = Column(Float)


class ExpenseData(Base):
    __tablename__ = 'expense_data'
    id = Column(Integer, primary_key=True)
    expense_id = Column(ForeignKey('expense.expense_id'))
    month = Column(String)
    cost = Column(Integer)
    quantity = Column(Float)


# Retrieving data from the database
def get_cities():
    return db_session.query(City)


def get_expenses():
    return db_session.query(Expense)


# Generating the set of average temperature values for a particular city
def get_city_temperature(city):
    return [month.average_temperature for month in city.city_meteo_data]


def get_city_humidity(city):
    return [month.average_humidity for month in city.city_meteo_data]


def get_exp_cost(expense):
    return [month.cost for month in expense.expense_detail_data]


def get_exp_quantity(expense):
    return [month.quantity for month in expense.expense_detail_data]


data = get_cities()
data_e = get_expenses()
MONTHS = [record.month for record in data[0].city_meteo_data]
CITIES = [city.city_name for city in data]
EXPENSES = [expense.expense_type for expense in data_e]
filtered = db_session.query(ExpenseData).filter(ExpenseData.month == "Jun")

