from classes.rec_ad_create_tabel import Create_rec_ad
from classes.rec_prev_freq import Get_freq
from classes.rec_ad_match import Rec_match


class rec_ad_engine:

    def __init__(self):
        self.create = Create_rec_ad()
        self.get_freq = Get_freq()
        self.match = Rec_match()

    def create_ad_table(self):
        self.create.create_table()

    def rec_ad(self):
        df = self.get_freq.get_dataframe(id='5a393eceed295900010386a8')
        self.match.check_match(df=df)
