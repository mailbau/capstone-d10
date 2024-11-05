def convert_to_dict_format(tps_data, tps_status_data, path_data):
    # Extracting point data
    point_dict = []
    tps_id_to_point_id = {}
    point_id = 0
    for tps_id, tps_info in tps_data.items():
        # Find demand/status value for the tps_id or default to 0.0
        status_entry = next((status for status in tps_status_data.values() if status['tpsId'] == tps_id), None)
        demand_value = status_entry['status'] if status_entry else 0.0
        
        point_dict.append({
            "point": point_id, 
            "name": tps_info["name"], 
            "coordinates": (float(tps_info["latitude"]), float(tps_info["longitude"])), 
            "demand": demand_value
        })
        tps_id_to_point_id[tps_id] = point_id
        point_id += 1
    
    # Extracting path data
    path_dict = []
    # path_id = 0
    for path_id_str, path_info in path_data.items():
        start_id = tps_id_to_point_id[path_info["initialTPS"]]
        end_id = tps_id_to_point_id[path_info["endTPS"]]
        path_dict.append({
            "path_id": path_id_str, 
            "start_id": start_id, 
            "end_id": end_id, 
            "distance": path_info["distance"]
        })
        # path_id += 1
    
    return point_dict, path_dict

# Example usage with given data
tps_data = {
  "-OAS440Ha7EjF_f2MTwm": {
    "address": "Niron, Pandowoharjo, Sleman, Sleman Regency, Special Region of Yogyakarta 55512",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/xTTDEtUQoAShq1yx5",
    "latitude": "-7.7051764",
    "longitude": "110.3605896",
    "name": "TPS 3R BUMDESA AMARTA PANDOWOHARJO"
  },
  "-OAS440tFje7vRLUVQUf": {
    "address": "7957+H25, Mlati Beningan, Sendangadi, Kec. Mlati, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55285",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/E2w9uFshZp4XJPoq7",
    "latitude": "-7.7230226",
    "longitude": "110.3469479",
    "name": "VESPA"
  },
  "-OAS441ZAN7E0u1No34N": {
    "address": "Trihanggo, Gamping, Sleman Regency, Special Region of Yogyakarta",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/bWeidMhs8rfzAHoD9",
    "latitude": "-7.7403728",
    "longitude": "110.3500104",
    "name": "ADHI JASA MARGA"
  },
  "-OAS442SU8h3E1yMe2Mh": {
    "address": "Jl. Magelang, Mlati Glondong, Sendangadi, Kec. Mlati, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55285",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/cinzRuMNHU1yVwYs5",
    "latitude": "-7.7388252",
    "longitude": "110.3626073",
    "name": "SPBU MLATI"
  },
  "-OAS4430aL4reZbpSh0n": {
    "address": "Jl. Magelang Km. 7, 8 Mlati, Mlati Glondong, Sendangadi, Kec. Sleman, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55285",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/X1bzteaQM1zMhthd6",
    "latitude": "-7.7352338",
    "longitude": "110.3626942",
    "name": "GEREJA MLATI"
  },
  "-OAS443ap0dJTlq7UzAI": {
    "address": "Jl. Magelang No.Km. 9, Banaran, Sendangadi, Kec. Mlati, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55285",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/FDTACxWYkt4xb86r9",
    "latitude": "-7.728415",
    "longitude": "110.3638894",
    "name": "RESTORAN PRINGSEWU"
  },
  "-OAS4449SiRLtCXJk3B7": {
    "address": "79J5+6CH, Jaran, Tridadi, Kec. Sleman, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55511",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/pP2GksprU4QMHmSeA",
    "latitude": "-7.7194279",
    "longitude": "110.3586221",
    "name": "STADION TRIDADI"
  },
  "-OAS444fRJ-t7ZUZDVWU": {
    "address": "79H5+P5R, Jl. KRT Pringgodiningrat, Jaran, Tridadi, Kec. Sleman, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55511",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/cvXXx7xBUAeNFruS7",
    "latitude": "-7.7206334",
    "longitude": "110.3578888",
    "name": "LAPANGAN TENIS SLEMAN"
  },
  "-OAS445FOs-bHdQf7GnI": {
    "address": "Jl. Turgo No.1, Beran, Tridadi, Kec. Sleman, Kabupaten Sleman, Daerah Istimewa Yogyakarta 63352",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/99AWXzaN8XmEttHx6",
    "latitude": "-7.7208712",
    "longitude": "110.3594597",
    "name": "GEDUNG SERBAGUNA SLEMAN"
  },
  "-OAbvaj7i0rvIdbk8KIb": {
    "address": "Komplek Perkantoran Pemda Kabupaten Sleman Jalan KRT Pringgodiningrat No.9 Beran, Beran Kidul, Tridadi, Kec. Sleman, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55511",
    "capacity": 10,
    "gmapsLink": "https://maps.app.goo.gl/pnRy9XCbs8sPUdcr8",
    "latitude": "-7.7194201",
    "longitude": "110.3550329",
    "name": "Dinas Lingkungan Hidup"
  },
  "-OAkudzPCsvVxg3nVb4R": {
    "address": "77J6+JCJ, Sutun, Sendangsari, Kec. Minggir, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55562",
    "capacity": 60,
    "gmapsLink": "https://maps.app.goo.gl/optJbb8QP8yc1aKr8",
    "latitude": "-7.7253404",
    "longitude": "110.2736666",
    "name": "TPST SENDANGSARI"
  }
}

tps_status_data = {
  "-OAeqgZHdT6WtmGfRQSy": {
    "status": 0.5,
    "timestamp": "2024-11-02T03:10:59.855Z",
    "tpsId": "-OAS440Ha7EjF_f2MTwm"
  },
  "-OAer3a5nA3Qs5-OC2lv": {
    "status": 0.1,
    "timestamp": "2024-11-02T03:12:38.283Z",
    "tpsId": "-OAS440tFje7vRLUVQUf"
  },
  "-OAer5zsiAmAz2nmlLT-": {
    "status": 0.4,
    "timestamp": "2024-11-02T03:12:48.128Z",
    "tpsId": "-OAS441ZAN7E0u1No34N"
  },
  "-OAer899yqwdWz_xnjKf": {
    "status": 0.7,
    "timestamp": "2024-11-02T03:12:56.978Z",
    "tpsId": "-OAS442SU8h3E1yMe2Mh"
  },
  "-OAerAW8XtPM8tDKXV3s": {
    "status": 0.9,
    "timestamp": "2024-11-02T03:13:06.641Z",
    "tpsId": "-OAS4430aL4reZbpSh0n"
  },
  "-OAerCV8xiHQEurfvqZb": {
    "status": 0.6,
    "timestamp": "2024-11-02T03:13:14.768Z",
    "tpsId": "-OAS443ap0dJTlq7UzAI"
  },
  "-OAerET-Qsh3oowQbjDY": {
    "status": 0.3,
    "timestamp": "2024-11-02T03:13:22.824Z",
    "tpsId": "-OAS4449SiRLtCXJk3B7"
  },
  "-OAerGKLhITwr7Py2LwU": {
    "status": 0.8,
    "timestamp": "2024-11-02T03:13:30.462Z",
    "tpsId": "-OAS444fRJ-t7ZUZDVWU"
  },
  "-OAerJHKdA2YesHDZVsj": {
    "status": 0.5,
    "timestamp": "2024-11-02T03:13:42.557Z",
    "tpsId": "-OAS445FOs-bHdQf7GnI"
  }
}

path_data = {
  "-OAbUDDZZOwWTML3Rr-S": {
    "distance": 1.7,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaAdhi"
  },
  "-OAbUZp2_TSJ6j3uOuuF": {
    "distance": 3.1,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiVespa"
  },
  "-OAbVTLAVfmoF0ClWQ2l": {
    "distance": 0.27,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaSpbu"
  },
  "-OAbVmF6YZu8_MxeLldH": {
    "distance": 1.4,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuVespa"
  },
  "-OAbWAQPTS27HRE74Hvi": {
    "distance": 0.45,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuGereja"
  },
  "-OAbWJQkYAgNUMR71JPw": {
    "distance": 1.2,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaSpbu"
  },
  "-OAbXOzLPX-j13m1GjQC": {
    "distance": 1.6,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaPringsewu"
  },
  "-OAbXUR_-6iikQDw2OGx": {
    "distance": 1.7,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuGereja"
  },
  "-OAbXuW8mWbRqtbwTrOA": {
    "distance": 2.2,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuTenis"
  },
  "-OAbY-wEHQrplKaOWaFX": {
    "distance": 1.4,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisPringsewu"
  },
  "-OAbYGCit7uN_Ph2Vjri": {
    "distance": 0.23,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisStadion"
  },
  "-OAbYSYQGLAwna9o1kZB": {
    "distance": 0.23,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionTenis"
  },
  "-OAbYmrR2WnG0mngyPTs": {
    "distance": 2.3,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionBumdes"
  },
  "-OAbYsmL6lDDiKgUFXJC": {
    "distance": 2.4,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesStadion"
  },
  "-OAbZWrnwVJxSP90lWNL": {
    "distance": 7,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesVespa"
  },
  "-OAbZiNb2ODl3sZqpJkm": {
    "distance": 5,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesAdhi"
  },
  "-OAbZt8uKOhGt44qNpMJ": {
    "distance": 4.9,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesSpbu"
  },
  "-OAb_-VUYHQDn7wV4uZj": {
    "distance": 5.3,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesGereja"
  },
  "-OAb_9H2GBpxuEWRH0Xc": {
    "distance": 3.7,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesPringsewu"
  },
  "-OAb_YTuYhgTNCUkcaL4": {
    "distance": 2.6,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesTenis"
  },
  "-OAbvzBQUVDz7JxRUqIQ": {
    "distance": 2.2,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhBumdes"
  },
  "-OAbw4v3LtlNGBdSKutG": {
    "distance": 4.8,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhVespa"
  },
  "-OAbwCSf_e-25xG3vtnd": {
    "distance": 2.8,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhAdhi"
  },
  "-OAbwKvJCAz9m2CVNIae": {
    "distance": 2.7,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhSpbu"
  },
  "-OAbwSOfpCpqZqCxMbN3": {
    "distance": 3.2,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhGereja"
  },
  "-OAbwYh-oLlA2KSdkT2s": {
    "distance": 1.5,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhPringsewu"
  },
  "-OAbwe8MG8KonLaNlKWb": {
    "distance": 0.5,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhStadion"
  },
  "-OAbwlB-6ONy6s7e9IbJ": {
    "distance": 0.4,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhTenis"
  },
  "-OAbx2ENi46BZ8OZ0ps8": {
    "distance": 0.65,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAbvaj7i0rvIdbk8KIb",
    "pathName": "dlhSerbaguna"
  },
  "-OAbx9lB_2QUL2vl4Jxp": {
    "distance": 0.65,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaDlh"
  },
  "-OAbxNidmkpc2myuKrF6": {
    "distance": 0.4,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisDlh"
  },
  "-OAbxiTHuvj8xgoWOkYL": {
    "distance": 2.3,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuDlh"
  },
  "-OAbxqTIve2YKlbZU97f": {
    "distance": 2.2,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaDlh"
  },
  "-OAbxzjZ8lw3ZgehZhU0": {
    "distance": 2.6,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuDlh"
  },
  "-OAby3ol8BqVsteR0pKP": {
    "distance": 2.8,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiDlh"
  },
  "-OAbyBSie1_z8RnRpTy1": {
    "distance": 2.9,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaDlh"
  },
  "-OAbyIWodZ4O1wq4YVFo": {
    "distance": 2.2,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesDlh"
  },
  "-OAbz45FZL4D7XfQqWCD": {
    "distance": 2.8,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesSerbaguna"
  },
  "-OAbzTGdiGlaExHIdTXa": {
    "distance": 4.6,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaBumdes"
  },
  "-OAbzcKXp4aOALCu5MEd": {
    "distance": 0.7,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaGereja"
  },
  "-OAbzjLG7Qaow01-WAus": {
    "distance": 2.2,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaPringsewu"
  },
  "-OAbzr1jHLtETUjo7a_4": {
    "distance": 2.9,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaStadion"
  },
  "-OAbzyydch3veLLIxOIz": {
    "distance": 2.8,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaTenis"
  },
  "-OAc-7kgTFssHukCKjjB": {
    "distance": 2.5,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaSerbaguna"
  },
  "-OAc-MCkA8P7AQjtp6qf": {
    "distance": 4.8,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiBumdes"
  },
  "-OAc-WleaHdtIIRQPFU0": {
    "distance": 1.9,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiSpbu"
  },
  "-OAc-d-2jWIky-yLnCRP": {
    "distance": 2.3,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiGereja"
  },
  "-OAc-jeVsuUGP4ZWz1F3": {
    "distance": 3.1,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiPringsewu"
  },
  "-OAc-wFCstPFFzUVicSw": {
    "distance": 2.5,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiTenis"
  },
  "-OAc0151oz-Vop8RYHnT": {
    "distance": 2.7,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiStadion"
  },
  "-OAc0C-o8-y9FzrPZc6N": {
    "distance": 2.5,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiSerbaguna"
  },
  "-OAc0U9DjYrU4mPoIlDL": {
    "distance": 4.4,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuBumdes"
  },
  "-OAc0bYH48UXEdfaInd5": {
    "distance": 1.9,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuAdhi"
  },
  "-OAc0jQ6d6nOrg9t-ovD": {
    "distance": 2,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuPringsewu"
  },
  "-OAc0plKM-Fs3q4vmZ7G": {
    "distance": 2.7,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuStadion"
  },
  "-OAc0xP2ThqSmDwr2n2p": {
    "distance": 2.5,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuTenis"
  },
  "-OAc13GU77_5aR6TttnG": {
    "distance": 2.2,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuSerbaguna"
  },
  "-OAc1Hq50CJVk1zIXTVW": {
    "distance": 4,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaBumdes"
  },
  "-OAc1OYXxIi62nkwDhYD": {
    "distance": 4.8,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaVespa"
  },
  "-OAc1V-G50xc5iDwzyPY": {
    "distance": 3,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaAdhi"
  },
  "-OAc1e-lfx7UTX0x_D0d": {
    "distance": 2.3,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaStadion"
  },
  "-OAc1jQHlUIs6R8nUE_U": {
    "distance": 2.1,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaTenis"
  },
  "-OAc1qHL76du4gpK7-jZ": {
    "distance": 1.8,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaSerbaguna"
  },
  "-OAc21lrpl3ufjUEXP-k": {
    "distance": 4,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuBumdes"
  },
  "-OAc27iQZSSnFdWur0oh": {
    "distance": 3.4,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuVespa"
  },
  "-OAc2D0m33l8Dw37gqvz": {
    "distance": 4.7,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuAdhi"
  },
  "-OAc2MxbkkQ9Ebsjq0gd": {
    "distance": 1.3,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuSpbu"
  },
  "-OAc2UgqwNtlJhsATxYX": {
    "distance": 2.3,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuStadion"
  },
  "-OAc2doAlDAwK5AIZM0W": {
    "distance": 1.9,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuSerbaguna"
  },
  "-OAc2umwX9P2kO9Xca72": {
    "distance": 4.8,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionVespa"
  },
  "-OAc304C-q7sBoolEGKn": {
    "distance": 2.7,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionAdhi"
  },
  "-OAc36a0qm2dmg2wWHGJ": {
    "distance": 2.7,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionSpbu"
  },
  "-OAc3CFnuK8X3fj4z3La": {
    "distance": 3.2,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionGereja"
  },
  "-OAc3IJXNhctosJdLZp5": {
    "distance": 1.6,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionPringsewu"
  },
  "-OAc3SHuRBgY7F71sioJ": {
    "distance": 0.5,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionSerbaguna"
  },
  "-OAc3ZJjgKjciV3f-PKy": {
    "distance": 0.5,
    "endTPS": "-OAbvaj7i0rvIdbk8KIb",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionDlh"
  },
  "-OAc3lAdFBizRZAheaeI": {
    "distance": 2.6,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisBumdes"
  },
  "-OAc3r24hSA9zXh2zcCU": {
    "distance": 4.7,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisVespa"
  },
  "-OAc3vrn3g5wTzierfEB": {
    "distance": 2.5,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisAdhi"
  },
  "-OAc4284_4f_Ros8VPCJ": {
    "distance": 2.6,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisSpbu"
  },
  "-OAc47_plKv9iq39w7Rd": {
    "distance": 3.1,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisGereja"
  },
  "-OAc4cwpykvbzGreL15p": {
    "distance": 0.26,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisSerbaguna"
  },
  "-OAc4pEcEz-exnu7u5iL": {
    "distance": 2.4,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaBumdes"
  },
  "-OAc4vRSZl_ZxianiMuQ": {
    "distance": 4.4,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaVespa"
  },
  "-OAc505m7Ijy_Fe45i0Q": {
    "distance": 2.5,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaAdhi"
  },
  "-OAc55w8ADDroz6o3GaY": {
    "distance": 2.4,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaSpbu"
  },
  "-OAc5CPe_Z0J803rXD_J": {
    "distance": 2.8,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaGereja"
  },
  "-OAc5K0THdIWFy5GF4c9": {
    "distance": 1.2,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaPringsewu"
  },
  "-OAc5QBAlW43xxYDiUk-": {
    "distance": 0.5,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaStadion"
  },
  "-OAc5XXm-9BudU8X4p7K": {
    "distance": 0.26,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaTenis"
  },
  "-OAkvV0PznjysWSq-4IQ": {
    "distance": 15.5,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS440Ha7EjF_f2MTwm",
    "pathName": "bumdesSendangsari"
  },
  "-OAkvmgbw8sW33veMk5n": {
    "distance": 13,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS440tFje7vRLUVQUf",
    "pathName": "vespaSendangsari"
  },
  "-OAkvtSNZ2r2xoSRb-By": {
    "distance": 11.9,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS441ZAN7E0u1No34N",
    "pathName": "adhiSendangsari"
  },
  "-OAkw0QlFTjN0UauY4Gh": {
    "distance": 13.3,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS442SU8h3E1yMe2Mh",
    "pathName": "spbuSendangsari"
  },
  "-OAkw6LTlnSDhm_hR1D0": {
    "distance": 15.6,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS4430aL4reZbpSh0n",
    "pathName": "gerejaSendangsari"
  },
  "-OAkwMCChUsXfFEzvyip": {
    "distance": 14.4,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS443ap0dJTlq7UzAI",
    "pathName": "pringsewuSendangsari"
  },
  "-OAkwVm1CVmygmarMzVx": {
    "distance": 13.8,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS4449SiRLtCXJk3B7",
    "pathName": "stadionSendangsari"
  },
  "-OAkwchFAZSqHyYmQmQk": {
    "distance": 13.7,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS444fRJ-t7ZUZDVWU",
    "pathName": "tenisSendangsari"
  },
  "-OAkwm42VDlKQY2JCj3j": {
    "distance": 14,
    "endTPS": "-OAkudzPCsvVxg3nVb4R",
    "initialTPS": "-OAS445FOs-bHdQf7GnI",
    "pathName": "serbagunaSendangsari"
  },
  "-OAl3q3ukkrXchjLAYCC": {
    "distance": 15.7,
    "endTPS": "-OAS440Ha7EjF_f2MTwm",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariBumdes"
  },
  "-OAl3wcV8yS_9scZ2rF4": {
    "distance": 14.6,
    "endTPS": "-OAS440tFje7vRLUVQUf",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariVespa"
  },
  "-OAl41UOmhGMV0EHIqtB": {
    "distance": 11.9,
    "endTPS": "-OAS441ZAN7E0u1No34N",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariAdhi"
  },
  "-OAl47Q-OUEtbq-lodky": {
    "distance": 13.2,
    "endTPS": "-OAS442SU8h3E1yMe2Mh",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariSpbu"
  },
  "-OAl4DEqU1wFEEIcFRVr": {
    "distance": 13.7,
    "endTPS": "-OAS4430aL4reZbpSh0n",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariGereja"
  },
  "-OAl4IzFT_1Z8dAEsl7O": {
    "distance": 14.9,
    "endTPS": "-OAS443ap0dJTlq7UzAI",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariPringsewu"
  },
  "-OAl4PNzTBm-GyDyF_kH": {
    "distance": 13.8,
    "endTPS": "-OAS4449SiRLtCXJk3B7",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariStadion"
  },
  "-OAl4Vo6Tg0OixkBhKkV": {
    "distance": 13.7,
    "endTPS": "-OAS444fRJ-t7ZUZDVWU",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariTenis"
  },
  "-OAl4gd6Sgh0Hny16Z0p": {
    "distance": 14,
    "endTPS": "-OAS445FOs-bHdQf7GnI",
    "initialTPS": "-OAkudzPCsvVxg3nVb4R",
    "pathName": "sendangsariSerbaguna"
  }
}

point_dict, path_dict = convert_to_dict_format(tps_data, tps_status_data, path_data)


print("point_dict", point_dict)
print("path_dict", path_dict)