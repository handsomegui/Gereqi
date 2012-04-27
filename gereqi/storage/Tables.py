class Sqlite:
    tables = ['''CREATE TABLE IF NOT EXISTS media (
                file_name    TEXT ,
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
                year   SMALLINT(4),
                genre  VARCHAR(20),
                track UNSIGNED TINYINT(2),
                length  VARCHAR(5),
                bitrate SMALLINT(4),
                added UNSIGNED INT(10),
                rating TINYINT(1),
                PRIMARY KEY (file_name) )''', 
            '''CREATE TABLE IF NOT EXISTS playlist (
                name TEXT,
                file_name TEXT)''',
            '''CREATE TABLE IF NOT EXISTS playcount (
                id INT(10) PRIMARY KEY,
                file_name    TEXT,
                count INT(10) )''',
            '''CREATE TABLE IF NOT EXISTS last_playlist (
                id INT(3) PRIMARY KEY,
                file_name TEXT)''']
