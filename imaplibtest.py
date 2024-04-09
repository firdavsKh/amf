import email.utils
import email, getpass, imaplib, os
# import win32com.client
import email, json
from datetime import date, datetime
from pathlib import Path
from  modules.postgres_connect import pgconnec
import psycopg2
import base64

class email_robot():
    def __init__(self, conf:json=None):
        if (conf is None): 
            print ("###>User@StatDep: Failed to create EmailRobot: valid config \ is not privided")
        self.email_host = conf["email_host"]
        self.login = conf["login"]
        self.password = conf["password"]
        self.start_date = conf["start_date"] 
        self.allowed_file_formats = conf["allowed_file_formats"] 
        print ("###>User@StatDep: EmailRobot in screated.") 

    def get_uid_for_recent_emails (self, start_date:date=None):
    # the function get emails received after start_date and return list of IUDs 
        print ("###>User@StatDep: get_for_recent_emails is started...")
        with imaplib.IMAP4_SSL(host=self.email_host,timeout=30000) as mail:
            mail.login(self.login, self.password) 
            #mail.select is required to change from stat AUTH to state SELECT
            mail.select("INBOX", readonly=True)
        
            if start_date is None:
                extration_start_date = date.fromisoformat(self.start_date)
            else: extration_start_date = start_date 
        
            result, data = mail.uid('search', "SINCE", extration_start_date.strftime(r'%d-%b-%Y'))
            ids = data[0]
            id_list = ids.split()
            iud_list = [uid.decode('utf-8') for uid in id_list] 
            ("###>User@StatDep: get_for_recent_emails is successful.") 
            return iud_list
        # TODO: proper exception 
        return None
 
    def send_notifications(self):
        print ("###>User@StatDep: EmailRobot in screated.")

    def get_proper_attachements(self, email_object): 
    # return list of allowed attachments of given email as a list
        if email_object.is_multipart(): 
            email_attachments = [part for part in email_object.walk() \
                                 if part.get_content_type() in self.allowed_file_formats]
        else: return None
        if not email_attachments: return None
        else: return email_attachments

    def fetch_emails_with_allowed_attachements (self, iud_list:list=None):
    # It takes list of IUDs as parameter that are used to grab matched emails
    # from email server. 
    # Then it check the attachemetns of each multipart email again list of 
    # file types provided by email_config.json. Returns emails as a list 
    # where each element represent a nested list with following elements:
    #   {'Message-ID': value},
    #   {'Date': value},
    #   {'From': value},
    #   {'Attachments': [(file_name, email.message.Message oject), ...]}         
        # print('!!!!!!!!!!!!!')
        # print(iud_list)
        # print('!!!!!!!!!!!!!')
        print ("###>User@StatDep: get_multipart_emails started...")
        with imaplib.IMAP4_SSL(host=self.email_host,timeout=30000) as mail:
            mail.login(self.login, self.password)
            #mail.select is required to change from stat AUTH to stateSELECT 
            mail.select("INBOX", readonly=True)
            #TODO: need a proper exception handling mechanism
            if iud_list is None:return None
            # result, data = mail.uid('fetch', iud_list[0], '(RFC822)')
            emails_list = []
            found_emails = [] 
            for uid in iud_list:
                em = email.message_from_bytes(mail.uid('fetch', uid, '(RFC822)')[1][0][1])
                found_emails.append(em) 
                if(em.is_multipart()):
                    raw_attachments = self.get_proper_attachements(em) 
                    # if raw_attachments: 
                    #     emails_list.append({
                    #         'Message-ID':{'Message-ID': em['Message-ID']},
                    #         'Date':{'Date': email.utils.parsedate_tz(em["Date"])},
                    #         'From':{'From': email.utils.parseaddr(em["From"])[1]},
                    #         'Attachements':{'Attachements': raw_attachments},                       
                    #         'UID':{'UID': uid},                       
                    #     }) 
                    # print(len(em['Message-ID']))


            for part in em.walk(): 
                if part.get_content_disposition() == 'attachment':
                    emails_list.append({
                            'Message-ID':{'Message-ID': em['Message-ID']},
                            'Date':{'Date': email.utils.parsedate_tz(em["Date"])},
                            'From':{'From': email.utils.parseaddr(em["From"])[1]},
                            # 'Attachements':{'Attachements': raw_attachments},                       
                            'UID':{'UID': uid},                       
                            'file_name':part.get_filename(),
                            'file_hash':f'{uid}{part.keys()}'
                        })
                    file_name = part.get_filename()
                    def decode_mime_words(s): 
                        return u''.join(
                            word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
                            for word, encoding in email.header.decode_header(s))
                    file_name = decode_mime_words(file_name)
                    file_data = part.get_payload(decode=True) 
                    with open(file_name, 'wb') as f:
                        f.write(file_data)                   
            

            print ("###>User@StatDep: get_multipart_emails is successful.")
            return emails_list

path = Path(__file__).parent
email_conf = json.load (open(path / ("config/email_conf.json")))
robot = email_robot(email_conf)
iud_list = robot.get_uid_for_recent_emails()
# print (robot.fetch_emails_with_allowed_attachements (iud_list)[1]['From']['From'])
print (robot.fetch_emails_with_allowed_attachements (iud_list))
# print (robot.fetch_emails_with_allowed_attachements (iud_list)[0]['Attachements'])
# robot.fetch_emails_with_allowed_attachements (iud_list)



# for i in robot.fetch_emails_with_allowed_attachements (iud_list):
#     print(i['From'])


connection = pgconnec()
cursor = connection.cursor()

try:
    for i in range(10):

        postgres_insert_query = """ INSERT INTO tbl_fileupload (UID, Message_ID, email_date,uploaded_date,email_from,status,chanel,file_name,file_dir,file_hash) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (521,'A11111111','11-11-2023','11-11-2023','22222',1,1,'132123','213131312','2332414')
        cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into mobile table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")