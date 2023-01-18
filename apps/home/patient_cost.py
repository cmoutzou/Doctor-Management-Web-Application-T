def insert_patient(ins):
    return "hello sissy" + ins



    '''
    name,age,amka=name_age_amka_patient()
    asfaleia=asfalistiki()
    energeia=activity()
    per_patient=personal_patient()
    
    new_patient=patient(name,age,amka,asfaleia,energeia)
            
    mycursor = mydb.cursor()
    
    if energeia=='ΝΟΣΗΛΕΙΑ':
        dayin,dayout,duration,cost=noshleia(asfaleia)
        
        sql = "INSERT INTO patient_hosp(amka,name,age,asfaleia,energeia,datein,dateout,personal_patient,cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (new_patient.amka, new_patient.name,new_patient.age,new_patient.asfaleia,new_patient.energeia,dayin,dayout,per_patient,cost)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    else:
        day_exam,cost=exetasi()
        sql = "INSERT INTO patient_exam(amka,name,age,asfaleia,energeia,date_exam,cost) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (new_patient.amka, new_patient.name,new_patient.age,new_patient.asfaleia,new_patient.energeia,day_exam,cost)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        