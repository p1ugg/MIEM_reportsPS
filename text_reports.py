import pandas as pd

def get_most_expensive_books(df: pd.DataFrame, Count: int) -> pd.DataFrame:
    """
    Функция генерации отчетов о самых дорогих книгах.

    Parameters
    ----------
    df : pd.DataFrame
        Исходная таблица с данными.

    Count : int
        Количество возвращаемых книг.

    Returns
    -------
    pd.DataFrame
        Отчет о самых дорогих книгах.
    """
    data = {
        "Name": df['Name'].tolist(),
        "Author": df['Author'].tolist(),
        "Price": df['Price'].tolist(),
    }
    df = pd.DataFrame(data)

    # Преобразование столбца Price в числовой тип данных
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Удаление строк с некорректными значениями (NaN) в столбце Price
    df = df.dropna(subset=['Price'])

    # Выберем самые дорогие книги
    top_expensive_books = df.nlargest(Count, 'Price')

    return top_expensive_books

def get_most_discussed_authors(df: pd.DataFrame, Count: int) -> pd.DataFrame:
  """
    Функция генерации отчетов о 20 самых обсуждаемых авторов.

    Parameters
    ----------
    df : pd.DataFrame
        Исходная таблица с данными.

    Count : int
        Количество авторов

    Returns
    -------
    pd.DataFrame
        Отчет о 20 самых обсуждаемых авторов.
    """
  # Группируем данные по авторам и считаем среднее количество отзывов
  author_reviews = df.groupby('Author')['Reviews'].mean().reset_index()

  # Выбираем топ авторов по среднему количеству отзывов
  top_authors = author_reviews.nlargest(Count, 'Reviews')

  return top_authors

# Функция для расчета среднего рейтинга на страну
def get_average_rating_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Функция распределение среднего рейтинга в зависимости от страны.

    Parameters
    ----------
    df : pd.DataFrame
        Исходная таблица с данными.

    Returns
    -------
    pd.DataFrame
        Отчет о распределении среднего рейтинга в зависимости от страны
    """

    country_rating = df.groupby('Country')['User Rating'].mean().reset_index()
    return country_rating

def get_average_price_per_year(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Функция распределения средней стоимости книги в период с 2009 по 2019 года.

    Parameters
    ----------
    df : pd.DataFrame
      Исходная таблица с данными.

    Returns
    -------
    pd.DataFrame
      Отчет о распределении средней стоимости книги в период с 2009 по 2019 года
    """

    # Фильтруем данные по указанному периоду
    df_filtered = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Преобразуем столбец "Price" в числовой формат
    df_filtered['Price'] = pd.to_numeric(df_filtered['Price'], errors='coerce')

    # Группируем данные по годам и считаем среднюю стоимость
    year_price = df_filtered.groupby('Year')['Price'].mean().reset_index()

    return year_price

