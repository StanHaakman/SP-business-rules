from classes.rec_ad_create_tabel import Create_rec_ad
from classes.rec_prev_freq import Get_freq
create = Create_rec_ad()
get_freq = Get_freq()

create.create_table()
df = get_freq.get_dataframe(id=)
