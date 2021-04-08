import psycopg2

from _functions.config import config


class DataSender:

    def __init__(self):
        pass

    def open_connection(self):
        db = config()
        con = psycopg2.connect(**db)
        return con

    def copy_products_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY products( idproducts, name, brand, category, sub_category, sub_sub_category, deeplink, doelgroep, fastmover, target, herhaalaankopen, price, folder_actief, discount )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_products_properties_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY properties( products_idproducts,properties )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"
        try:
            cur.execute(query)
        except Exception as e:
            print(e)
        con.commit()
        con.close()

    def copy_profiles_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY visitors(idVisitors, TypeVisitors, previously_recommended, buids )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY sessions( idsessions, identifier, has_sale, buid, products )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_buids_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY buids( buids, sessions_idsessions )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_has_sale_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY orders(Products_idProducts, Sessions_idSessions, has_been_sold)" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_buids_csv(self, pathname):
        con = self.open_connection()
        cur = con.cursor()

        query = f"COPY buids( buids, sessions_idsessions )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()
