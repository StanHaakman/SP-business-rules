import psycopg2

from _functions.config import config


class DataSender:

    def __init__(self):
        pass

    def openconnection(self):
        db = config()
        con = psycopg2.connect(**db)
        return con

    def copy_products_csv(self, pathname):
        con = self.openconnection()
        cur = con.cursor()

        query = f"COPY products( idproducts, name, brand, category, deeplink, doelgroep, fastmover, target, herhaalaankopen, price )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_products_properties_csv(self, pathname):
        con = self.openconnection()
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
        con = self.openconnection()
        cur = con.cursor()

        query = f"COPY visitors(idVisitors, TypeVisitors, latest_visit )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_csv(self, pathname):
        con = self.openconnection()
        cur = con.cursor()

        query = f"COPY sessions( idsessions,identifier, sessie_start, sessie_end )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_buids_csv(self, pathname):
        con = self.openconnection()
        cur = con.cursor()

        query = f"COPY buids( buids, sessions_idsessions )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_has_sale_csv(self, pathname):
        con = self.openconnection()
        cur = con.cursor()

        query = f"COPY orders(Products_idProducts, Sessions_idSessions, has_been_sold)" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()

    def copy_sessions_buids_csv(self, pathname):
        con = self.openconnection()
        cur = con.cursor()

        query = f"COPY buids( buids, sessions_idsessions )" \
                f"FROM '{pathname}'" \
                f"DELIMITER ','" \
                f"CSV HEADER;"

        cur.execute(query)
        con.commit()
        con.close()
   
