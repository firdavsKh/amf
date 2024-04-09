import email
import imaplib
import email.header

# Login to your email account
mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login('3d_0001@mail.ru', 'RuskXtAkGEPHMXjhQbV4')
mail.select('inbox')
 
result, data = mail.uid('search', None, "FROM",'jv2323@imf.org')
latest_email_uid = data[0].split()[-1]
 
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]
 
email_message = email.message_from_bytes(raw_email)
 
for part in email_message.walk(): 
    if part.get_content_disposition() == 'attachment':
        file_name = part.get_filename()
        def decode_mime_words(s):
            
            return u''.join(
                word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
                for word, encoding in email.header.decode_header(s))
        file_name = decode_mime_words(file_name)
        file_data = part.get_payload(decode=True) 
        with open(file_name, 'wb') as f:
            f.write(file_data)