import ibm_db
from datetime import datetime

# Replace these values with your database configuration
dbname = 'bludb'
hostname = 'b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud'
port = '32716'
protocol = 'TCPIP' 
uid = 'byn13214'
password = 'YINqMSZ8hBrq82UX'

# Build the DSN string
dsn = f"DATABASE={dbname};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={uid};PWD={password};Security=SSL"

def insert_event():
    try:
        conn = ibm_db.connect(dsn, "", "")
        sample_data = "INSERT INTO AFN(Prospect_name,Prospect_Phone,CSR_Name,last_interaction_date,next_followup_date,status) VALUES('Srinivas','+14154759607','John','2023-09-10','2023-09-11','No');"
        stmt = ibm_db.exec_immediate(conn, sample_data)
        ibm_db.close(conn)
        return {"result": "Data inserted successfully"}
    except Exception as e:
        return {"dberror": str(e)}

# prospect_phone = "whatsapp:+917013151060"
# new_status = "No"
# prospect_name = "Vijay Kumar"


def update_status(prospect_phone,new_status):
# def update_status():
    today = datetime.now().date()
    try:
        conn = ibm_db.connect(dsn, "", "")
        update_query = f"UPDATE AFN SET status = '{new_status}', last_interaction_date = '{today}' WHERE Prospect_Phone = '{prospect_phone}';"
        # update_query = f"UPDATE AFN SET next_followup_date = '2023-09-12' WHERE PROSPECT_NAME = 'Sruthi Narala';"
        stmt = ibm_db.exec_immediate(conn, update_query)
        ibm_db.close(conn)
        return {"result": "Status updated successfully"}
    except Exception as e:
        return {"dberror": str(e)}

def update_status_no(prospect_phone,new_status,next_date):
    today = datetime.now().date()
    try:
        conn = ibm_db.connect(dsn, "", "")
        update_query = f"UPDATE AFN SET status = '{new_status}', last_interaction_date = '{today}',next_followup_date = '{next_date}' WHERE Prospect_Phone = '{prospect_phone}';"
        # update_query = f"UPDATE AFN SET CASE_DESCRIPTION = 'Paid all EMI, yet to receive loan clearance certificate' WHERE PROSPECT_NAME = 'Srinivas';"
        stmt = ibm_db.exec_immediate(conn, update_query)
        ibm_db.close(conn)
        return {"result": "Status updated successfully"}
    except Exception as e:
        return {"dberror": str(e)}


def delete_rows():
    try:
        conn = ibm_db.connect(dsn, "", "")
        if conn:
            sql = "DELETE FROM AFN WHERE PROSPECT_PHONE LIKE 'whatsapp:%'"
            
            # Prepare and execute the SQL query
            stmt = ibm_db.prepare(conn, sql)
            if ibm_db.execute(stmt):
                ibm_db.commit(conn)
                return {"message": "Rows deleted successfully"}
            else:
                return {"error": "Failed to execute SQL query"}
        else:
            return {"error": "Failed to connect to the database"}
    except Exception as e:
        return {"dberror": str(e)}
    finally:
        if conn:
            ibm_db.close(conn)

def db2_instance():

    try:
        conn = ibm_db.connect(dsn, "", "")
        stmt = ibm_db.exec_immediate(conn, "select PROSPECT_NAME,PROSPECT_PHONE,CSR_NAME,LAST_INTERACTION_DATE,NEXT_FOLLOWUP_DATE,CASE_DESCRIPTION from AFN")
        data = []
        
        while ibm_db.fetch_row(stmt):
            name = ibm_db.result(stmt, 0)  # PROSPECT_NAME
            phone = ibm_db.result(stmt, 1)  # PROSPECT_PHONE
            csr_name = ibm_db.result(stmt,2)
            last_date = ibm_db.result(stmt,3)
            follow_up_date = ibm_db.result(stmt,4) #NEXT_FOLLOWUP_DATE
            case_desc = ibm_db.result(stmt,5)
            data.append({"PROSPECT_NAME": name, "PROSPECT_PHONE": phone, "CSR_NAME":csr_name,"LAST_INTERACTION_DATE":last_date,
            "NEXT_FOLLOWUP_DATE":follow_up_date,"CASE_DESCRIPTION":case_desc})

        ibm_db.close(conn)
        return {"data": data}
    except Exception as e:
        return {"dberror": str(e)}

def get_name(sender_id):
    try:
        conn = ibm_db.connect(dsn, "", "")
        stmt = ibm_db.exec_immediate(conn, "select PROSPECT_NAME from AFN where PROSPECT_PHONE='{sender_id}'")
        data = []

        while ibm_db.fetch_row(stmt):
            name = ibm_db.result(stmt, 0)
            data.append({"PROSPECT_NAME": name})
        ibm_db.close(conn)
        return {"data": data}
    except Exception as e:
        return {"dberror": str(e)}
# get_name(sender_id)

# # Call the main function to test it
if __name__ == "__main__":
# #     inserted = insert_event()
# #     print(inserted)
# # # #     # db2_instance()
# # # #     # delete_rows()
# # #     # result = db2_instance()
# # #     # print(result)
# # # #     print("User", result["data"][0]["PROSPECT_PHONE"])
    up = update_status()
    print(up)





