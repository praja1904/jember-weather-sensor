CREATE TABLE IF NOT EXISTS log_sensor (
    id SERIAL PRIMARY KEY,
    nama VARCHAR(100),
    nim VARCHAR(20),
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Memasukkan data Nama dan NIM Anda
INSERT INTO log_sensor (nama, nim) VALUES ('Moh. Raffel Prajadinata', '242410102025');