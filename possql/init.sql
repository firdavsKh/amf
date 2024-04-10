CREATE TABLE tbl_fileupload (
  id SERIAL PRIMARY KEY,
  UID INT UNIQUE,
  Message_ID VARCHAR(255) UNIQUE,
  email_date DATE,
  uploaded_date DATE,
  email_from VARCHAR(255),
  upload_status INT,
  chanel INT,
  file_name VARCHAR(100),
  file_dir VARCHAR(255),
  file_hash VARCHAR(255)
);
