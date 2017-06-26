#!/usr/bin/env python3
from main import Obs, db
from datetime import datetime

import pyspeedtest
st = pyspeedtest.SpeedTest()
print("Starting")

ping_res = st.ping()
dl_res = st.download()

obs = Obs(datetime.now(), ping_res, dl_res)
db.session.add(obs)
db.session.commit()
print("Finished")