PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    token TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);
CREATE TABLE users (
    uuid TEXT PRIMARY KEY,
    id TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);
INSERT INTO users VALUES('67950057-2cbb-4e9f-b18d-35161abaa7e6','gi6791991','1f9c4b588be99fe1f505b545e7e8ef0ac3e157b80a516f6d3d9582dff60b718d','11c4cb4d9c796218','이건희','2025-08-28 01:07:23');
INSERT INTO users VALUES('96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','gi67919912','dd20311383221ea63e25c2a1ca591a1bf8d3ee8eaf55ae16af88e965649225e6','44eacd808977a994','dlrjsgml','2025-08-28 01:28:58');
INSERT INTO users VALUES('6fd50e6e-4390-4b3d-85b9-7066511b6ca7','gaon0619','3ba120e1759324d738cb4cb22b154bb1108ea6de6af68672fcb2e6ea3c1dbd7a','1b8b2e1ac6118372','최가온','2025-08-28 08:51:51');
INSERT INTO users VALUES('e833b589-8670-4f22-9083-f9f2149163f4','aewol09','77dca4d50d55b035c802cb9188adeb4132fd138c403a61baf86886faaea0cf78','26396eefd7efc283','송명근','2025-08-28 11:12:20');
INSERT INTO users VALUES('17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','yoonga07','532f4b70950ea1f6ec662060abd3f9f40b982ca8f4868261d84788f2dc19a0ca','dbc589bf18d86e64','이가윤','2025-08-28 15:27:39');
INSERT INTO users VALUES('cb261a65-c2d4-40e3-b79f-b807fa177158','donghun07','90409a9f435b5228930fa2504d0407eb102edd5ca16499e7d3d67f25a1eff714','503e4d166697d8e6','이동훈','2025-08-28 16:50:55');
INSERT INTO users VALUES('158fe3ba-4d61-46c1-86ae-3c1908ac91c7','kmssuper','3e93536e353b34c2f4008e482c00c687190bc95856302e56e21c5a0c55c0a949','27d2d6ec3e321724','김민수','2025-08-28 17:01:36');
INSERT INTO users VALUES('bd8571d6-6593-492d-9750-db9dd395b282','gwyou1127','820da5c218799c783720ff7520a7094de3cadf8797c0146116a7e83b4ac8f2a0','2a615fcdc0545d25','유건우','2025-08-28 17:09:24');
CREATE TABLE user_verify (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);
INSERT INTO user_verify VALUES(1,'67950057-2cbb-4e9f-b18d-35161abaa7e6','verified',NULL,'2025-08-28 01:07:23');
INSERT INTO user_verify VALUES(2,'96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','verified',NULL,'2025-08-28 01:28:58');
INSERT INTO user_verify VALUES(3,'6fd50e6e-4390-4b3d-85b9-7066511b6ca7','verified',NULL,'2025-08-28 08:51:51');
INSERT INTO user_verify VALUES(4,'e833b589-8670-4f22-9083-f9f2149163f4','blocked','두찜이 맛이 없다고?','2025-08-28 11:12:20');
INSERT INTO user_verify VALUES(5,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','verified',NULL,'2025-08-28 15:27:39');
INSERT INTO user_verify VALUES(6,'cb261a65-c2d4-40e3-b79f-b807fa177158','verified',NULL,'2025-08-28 16:50:55');
INSERT INTO user_verify VALUES(7,'158fe3ba-4d61-46c1-86ae-3c1908ac91c7','verified',NULL,'2025-08-28 17:01:36');
INSERT INTO user_verify VALUES(8,'bd8571d6-6593-492d-9750-db9dd395b282','verified',NULL,'2025-08-28 17:09:24');
CREATE TABLE user_admin (
    user_uuid TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);
INSERT INTO user_admin VALUES('67950057-2cbb-4e9f-b18d-35161abaa7e6','2025-08-28 01:33:08');
INSERT INTO user_admin VALUES('158fe3ba-4d61-46c1-86ae-3c1908ac91c7','2025-08-28 17:05:41');
CREATE TABLE user_teacher (
    user_uuid TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);
CREATE TABLE user_class_tracking (
    user_uuid TEXT NOT NULL,
    year INTEGER NOT NULL,
    grade INTEGER CHECK (grade >= 1 AND grade <= 3),
    class INTEGER CHECK (class >= 1 AND class <= 10),
    number INTEGER CHECK (number >= 1 AND number <= 30),
    is_graduated BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_uuid) REFERENCES users (uuid),
    PRIMARY KEY (user_uuid, year),
    UNIQUE(year, grade, class, number)
);
INSERT INTO user_class_tracking VALUES('67950057-2cbb-4e9f-b18d-35161abaa7e6',2025,3,9,15,0);
INSERT INTO user_class_tracking VALUES('6fd50e6e-4390-4b3d-85b9-7066511b6ca7',2025,3,9,20,0);
INSERT INTO user_class_tracking VALUES('e833b589-8670-4f22-9083-f9f2149163f4',2025,3,10,10,0);
INSERT INTO user_class_tracking VALUES('17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f',2025,3,9,14,0);
INSERT INTO user_class_tracking VALUES('cb261a65-c2d4-40e3-b79f-b807fa177158',2025,3,8,12,0);
INSERT INTO user_class_tracking VALUES('158fe3ba-4d61-46c1-86ae-3c1908ac91c7',2025,3,10,3,0);
INSERT INTO user_class_tracking VALUES('bd8571d6-6593-492d-9750-db9dd395b282',2025,3,9,13,0);
CREATE TABLE user_sessions (
    id TEXT PRIMARY KEY,
    user_uuid TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);
INSERT INTO user_sessions VALUES('749b912b-af76-4e1c-a600-5e0e456527fe','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:10:52');
INSERT INTO user_sessions VALUES('b8056713-b3fd-4f22-9679-8428234136ee','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:14:04');
INSERT INTO user_sessions VALUES('b4049429-2d1e-4c03-b631-a3fd55eb2b07','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:15:49');
INSERT INTO user_sessions VALUES('df6aff2a-594b-43cc-9926-da536daf2015','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:16:25');
INSERT INTO user_sessions VALUES('3131fdaf-aca3-4600-9fee-51dcc23fd6b4','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:19:10');
INSERT INTO user_sessions VALUES('99a88320-34b1-4253-9479-ed044fa4b17c','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:19:18');
INSERT INTO user_sessions VALUES('65abc92c-6ee7-4d31-b04e-14b2a51d6516','96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:29:08');
INSERT INTO user_sessions VALUES('c03fd309-399b-4fd1-be5b-908dc8593ccb','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:29:21');
INSERT INTO user_sessions VALUES('613d6459-11bd-47cf-b107-2918711773b0','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:36:25');
INSERT INTO user_sessions VALUES('54f7a199-fa54-4279-9f5e-3f85e0b62158','96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:36:37');
INSERT INTO user_sessions VALUES('1596f126-a5d3-4ddc-b0c4-02a72380d2e7','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:41:25');
INSERT INTO user_sessions VALUES('8e9ac89d-fb61-4ca2-ac42-fe2cd647661a','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:42:50');
INSERT INTO user_sessions VALUES('99d72170-bc90-4d95-bec4-5dd4959a09b6','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:43:16');
INSERT INTO user_sessions VALUES('c3a8d4c1-6999-4fd8-b435-a039e2352dc2','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:44:10');
INSERT INTO user_sessions VALUES('c1a36ac9-6a62-4921-b9bd-46dd3669530b','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 01:44:24');
INSERT INTO user_sessions VALUES('cfa9263e-9595-41d4-a0df-f37bfa64a977','96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 02:08:00');
INSERT INTO user_sessions VALUES('3e2cfea1-42e0-45c4-bcda-0517601441e4','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 02:09:05');
INSERT INTO user_sessions VALUES('c8a27a1e-36de-4bd5-9c05-0c8adae1846f','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 02:11:11');
INSERT INTO user_sessions VALUES('65b98e6c-1698-40b0-a525-d9137920f619','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 02:32:01');
INSERT INTO user_sessions VALUES('21bd2e8a-271f-452b-8508-ffa2ec8c32e8','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 02:32:11');
INSERT INTO user_sessions VALUES('ef5c5fb9-6784-45fb-9ce6-80edcd5b4204','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 02:34:23');
INSERT INTO user_sessions VALUES('a23df2ad-4ec2-459e-989a-8d01b29f80cb','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 08:35:34');
INSERT INTO user_sessions VALUES('9e3d4ad3-28c7-4366-b836-c10abbfa50a0','6fd50e6e-4390-4b3d-85b9-7066511b6ca7','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 08:55:36');
INSERT INTO user_sessions VALUES('47335e3d-15f4-4cd5-bb33-50a115304401','6fd50e6e-4390-4b3d-85b9-7066511b6ca7','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',1,'2025-08-28 08:59:25');
INSERT INTO user_sessions VALUES('a3a224cb-be87-4ea1-9bc5-cb1ec5954b5c','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 09:15:54');
INSERT INTO user_sessions VALUES('d08f725e-1908-4631-a63a-ab2a48d69bd5','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 09:41:02');
INSERT INTO user_sessions VALUES('ac20c549-fd03-4b5a-892c-240e44f8a865','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',0,'2025-08-28 10:02:57');
INSERT INTO user_sessions VALUES('7b41dc47-3069-446a-8c68-28368241b286','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 11:12:34');
INSERT INTO user_sessions VALUES('2b5dd976-dd3a-48e1-8afb-59324ad92632','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 11:13:26');
INSERT INTO user_sessions VALUES('6a75bfe6-cbba-4f3a-98b0-9fdbce9d53cf','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 11:17:35');
INSERT INTO user_sessions VALUES('0e27b2f6-1b97-4389-a0e5-fd41941319d7','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 11:17:48');
INSERT INTO user_sessions VALUES('aacb6ed0-9393-4847-abd0-7b1767d860d9','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 11:34:30');
INSERT INTO user_sessions VALUES('7303f9ef-c9cd-4f84-a8f5-1c0ccc1530eb','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',0,'2025-08-28 12:10:04');
INSERT INTO user_sessions VALUES('235159be-c920-4930-b363-b47835eb034a','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 12:14:20');
INSERT INTO user_sessions VALUES('d08d1e17-f9d9-4495-b8d6-0775930a3b86','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (iPhone; CPU iPhone OS 26_0_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/139.0.7258.76 Mobile/15E148 Safari/604.1',0,'2025-08-28 13:31:33');
INSERT INTO user_sessions VALUES('9c2a8563-46f7-43db-84c8-b530c199a089','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 13:42:27');
INSERT INTO user_sessions VALUES('5e3eefb1-bd33-423b-b684-491e36b7c272','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Android 15; Mobile; rv:142.0) Gecko/142.0 Firefox/142.0',0,'2025-08-28 14:34:18');
INSERT INTO user_sessions VALUES('947b8d83-52b7-4b13-af81-ecd9b94fc8fc','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',0,'2025-08-28 14:40:04');
INSERT INTO user_sessions VALUES('3b9f59e5-ae1b-491e-8e7c-f7bc0ed71394','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Android 15; Mobile; rv:142.0) Gecko/142.0 Firefox/142.0',0,'2025-08-28 15:01:56');
INSERT INTO user_sessions VALUES('8de96235-d5d6-46a0-b73d-bf3364953673','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:02:30');
INSERT INTO user_sessions VALUES('40653bde-2ca1-48ef-8483-c623dbb39285','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:28:14');
INSERT INTO user_sessions VALUES('7edc294f-e9cf-4d97-b189-de5a0c04ea10','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:29:24');
INSERT INTO user_sessions VALUES('7606b0d8-4d9d-4a2e-a151-81d0f9f356f5','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:29:25');
INSERT INTO user_sessions VALUES('c0999ff0-8a85-4a74-ba6b-d29aa9cf8916','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:29:25');
INSERT INTO user_sessions VALUES('bb8b56f0-42a4-4402-bd6e-be87eea117ad','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:29:25');
INSERT INTO user_sessions VALUES('9c4224ea-f856-48c9-8652-761186e94338','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:29:25');
INSERT INTO user_sessions VALUES('b4d53ed9-9d17-4c30-b060-35e7512931cd','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:35:22');
INSERT INTO user_sessions VALUES('c5b216d7-1c31-4643-a75f-a71cec282a39','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:36:35');
INSERT INTO user_sessions VALUES('1341ae15-01b3-4b83-b60c-9e81f74cb119','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:42:16');
INSERT INTO user_sessions VALUES('8735c6a8-b0c8-4cad-9447-d285d36eb323','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:46:59');
INSERT INTO user_sessions VALUES('26aceac8-d055-419d-b754-be2e40723e04','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:50:09');
INSERT INTO user_sessions VALUES('7134c136-6734-46bf-b3a3-f4bb0c120a18','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 15:54:20');
INSERT INTO user_sessions VALUES('2f361233-5f4f-4e0b-8ede-9e7dd140d3d0','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0',0,'2025-08-28 15:54:52');
INSERT INTO user_sessions VALUES('339a28d7-93fd-4a5b-88b8-05352b9bd9d5','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',0,'2025-08-28 16:11:33');
INSERT INTO user_sessions VALUES('eb6f410e-890f-4891-89f6-9b2d0ab4dd48','cb261a65-c2d4-40e3-b79f-b807fa177158','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/28.0 Chrome/130.0.0.0 Mobile Safari/537.36',1,'2025-08-28 16:54:33');
INSERT INTO user_sessions VALUES('03c627e9-85e7-45b4-a25b-8467d2e1bc7e','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/28.0 Chrome/130.0.0.0 Mobile Safari/537.36',0,'2025-08-28 16:58:14');
INSERT INTO user_sessions VALUES('8d7e58e2-af1f-4674-9a9b-a74a2c3143bc','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',1,'2025-08-28 16:59:26');
INSERT INTO user_sessions VALUES('f7e7ba7f-0e48-4520-8d7d-376a3b87f59d','158fe3ba-4d61-46c1-86ae-3c1908ac91c7','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',1,'2025-08-28 17:04:55');
INSERT INTO user_sessions VALUES('fb6379f2-ace2-4029-bce8-522a1b80210a','6fd50e6e-4390-4b3d-85b9-7066511b6ca7','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',1,'2025-08-28 17:08:24');
INSERT INTO user_sessions VALUES('4915cb45-8794-4104-850c-9eef23567729','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:09:05');
INSERT INTO user_sessions VALUES('934c8441-e617-4287-97fb-05f2e5f169b4','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:09:25');
INSERT INTO user_sessions VALUES('b6cd46a4-5074-47e4-ab90-89fb0168322b','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:09:41');
INSERT INTO user_sessions VALUES('f1a753e2-e170-4260-8df4-48d8ad380177','bd8571d6-6593-492d-9750-db9dd395b282','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:10:12');
INSERT INTO user_sessions VALUES('9bc2f0a5-004c-45fe-bbc7-b1764b06ba2c','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:10:21');
INSERT INTO user_sessions VALUES('393509f5-0c29-48ba-9d5e-cf7d477e6497','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:10:42');
INSERT INTO user_sessions VALUES('2d06e328-3969-4c63-85df-bd539377b538','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:11:09');
INSERT INTO user_sessions VALUES('84fce6a2-79be-4b54-a0c6-50ef8d1c04f2','bd8571d6-6593-492d-9750-db9dd395b282','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:11:25');
INSERT INTO user_sessions VALUES('4c6f311c-f1e6-4133-a57e-3f7dcd9d3bcd','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:12:05');
INSERT INTO user_sessions VALUES('d782be2a-b6c9-4a24-a0a6-d4167858f38e','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',1,'2025-08-28 17:13:23');
INSERT INTO user_sessions VALUES('8867aca6-6a85-416b-ac37-1d72873bae58','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',0,'2025-08-28 17:20:41');
INSERT INTO user_sessions VALUES('264185fc-f727-4cb5-a1ce-9c234820d8e6','17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',1,'2025-08-28 17:21:46');
INSERT INTO user_sessions VALUES('d9846434-fe6b-49e6-9d73-4a93d9773c2a','e833b589-8670-4f22-9083-f9f2149163f4','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/28.0 Chrome/130.0.0.0 Mobile Safari/537.36',1,'2025-08-28 17:30:45');
INSERT INTO user_sessions VALUES('aed0e513-4a53-4b31-adb1-19af9884c753','67950057-2cbb-4e9f-b18d-35161abaa7e6','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',1,'2025-08-28 17:35:55');
INSERT INTO user_sessions VALUES('a3f1b8c5-cdf5-4006-bcc1-a4b1ed7807d0','158fe3ba-4d61-46c1-86ae-3c1908ac91c7','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',1,'2025-08-31 01:41:12');
CREATE TABLE auth_qr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NOT NULL,
    auth_code TEXT NOT NULL,
    use_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid)
);
INSERT INTO auth_qr VALUES(1,'67950057-2cbb-4e9f-b18d-35161abaa7e6','4e487ed4e0b98da3',0,'2025-08-28 01:13:54');
INSERT INTO auth_qr VALUES(2,'67950057-2cbb-4e9f-b18d-35161abaa7e6','756063d11e030a62',0,'2025-08-28 01:16:21');
INSERT INTO auth_qr VALUES(3,'67950057-2cbb-4e9f-b18d-35161abaa7e6','5365ff9ba27d2e8f',0,'2025-08-28 01:19:15');
INSERT INTO auth_qr VALUES(4,'67950057-2cbb-4e9f-b18d-35161abaa7e6','325b2cf2d9f6b0fa',0,'2025-08-28 01:21:13');
INSERT INTO auth_qr VALUES(5,'67950057-2cbb-4e9f-b18d-35161abaa7e6','0a2bd115fb0da116',0,'2025-08-28 01:23:06');
INSERT INTO auth_qr VALUES(6,'67950057-2cbb-4e9f-b18d-35161abaa7e6','64d8e4f327fdeb81',0,'2025-08-28 01:24:46');
INSERT INTO auth_qr VALUES(7,'96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','f92a58976b8be21a',0,'2025-08-28 01:39:25');
INSERT INTO auth_qr VALUES(8,'96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','9ef6e351fb0dda42',0,'2025-08-28 01:40:29');
INSERT INTO auth_qr VALUES(9,'67950057-2cbb-4e9f-b18d-35161abaa7e6','9b6b50a973d72d84',0,'2025-08-28 02:24:18');
INSERT INTO auth_qr VALUES(10,'67950057-2cbb-4e9f-b18d-35161abaa7e6','b8112fd03b777eac',0,'2025-08-28 02:28:58');
INSERT INTO auth_qr VALUES(11,'67950057-2cbb-4e9f-b18d-35161abaa7e6','25f30ce870d44616',0,'2025-08-28 02:29:58');
INSERT INTO auth_qr VALUES(12,'67950057-2cbb-4e9f-b18d-35161abaa7e6','64b34b301af4cd32',1,'2025-08-28 08:35:37');
INSERT INTO auth_qr VALUES(13,'6fd50e6e-4390-4b3d-85b9-7066511b6ca7','26087bc80a9c2a5f',0,'2025-08-28 08:59:28');
INSERT INTO auth_qr VALUES(14,'67950057-2cbb-4e9f-b18d-35161abaa7e6','07528640820ecfa2',0,'2025-08-28 09:50:59');
INSERT INTO auth_qr VALUES(15,'67950057-2cbb-4e9f-b18d-35161abaa7e6','5c2f38cd9db647ae',0,'2025-08-28 10:04:40');
INSERT INTO auth_qr VALUES(16,'67950057-2cbb-4e9f-b18d-35161abaa7e6','5dffece10a3f95ed',0,'2025-08-28 10:15:43');
INSERT INTO auth_qr VALUES(17,'e833b589-8670-4f22-9083-f9f2149163f4','b4adb47a5ecae0b5',0,'2025-08-28 11:13:29');
INSERT INTO auth_qr VALUES(18,'e833b589-8670-4f22-9083-f9f2149163f4','91e853fcf4735442',0,'2025-08-28 11:14:36');
INSERT INTO auth_qr VALUES(19,'e833b589-8670-4f22-9083-f9f2149163f4','4824ec53bf969729',0,'2025-08-28 11:16:23');
INSERT INTO auth_qr VALUES(20,'e833b589-8670-4f22-9083-f9f2149163f4','d6d32b9483d45ee1',0,'2025-08-28 11:17:41');
INSERT INTO auth_qr VALUES(21,'67950057-2cbb-4e9f-b18d-35161abaa7e6','86ca409988875f4a',1,'2025-08-28 11:34:33');
INSERT INTO auth_qr VALUES(22,'67950057-2cbb-4e9f-b18d-35161abaa7e6','a3087e71449bc7f1',0,'2025-08-28 11:36:47');
INSERT INTO auth_qr VALUES(23,'67950057-2cbb-4e9f-b18d-35161abaa7e6','64fc0e9f9b80e7b9',3,'2025-08-28 11:38:40');
INSERT INTO auth_qr VALUES(24,'67950057-2cbb-4e9f-b18d-35161abaa7e6','6ffdcc88eb060417',1,'2025-08-28 11:50:07');
INSERT INTO auth_qr VALUES(25,'67950057-2cbb-4e9f-b18d-35161abaa7e6','212a212d5ffbd4b1',0,'2025-08-28 12:10:11');
INSERT INTO auth_qr VALUES(26,'67950057-2cbb-4e9f-b18d-35161abaa7e6','6700e9515e858d13',2,'2025-08-28 12:14:21');
INSERT INTO auth_qr VALUES(27,'67950057-2cbb-4e9f-b18d-35161abaa7e6','2abc3b9930164cb1',1,'2025-08-28 12:20:50');
INSERT INTO auth_qr VALUES(28,'67950057-2cbb-4e9f-b18d-35161abaa7e6','3eed9ed3b9044481',0,'2025-08-28 12:23:35');
INSERT INTO auth_qr VALUES(29,'67950057-2cbb-4e9f-b18d-35161abaa7e6','56a1866c0a63e552',2,'2025-08-28 12:26:30');
INSERT INTO auth_qr VALUES(30,'67950057-2cbb-4e9f-b18d-35161abaa7e6','ecfa9dc27309ed18',2,'2025-08-28 12:30:47');
INSERT INTO auth_qr VALUES(31,'67950057-2cbb-4e9f-b18d-35161abaa7e6','e14dbf59658803b0',1,'2025-08-28 12:33:27');
INSERT INTO auth_qr VALUES(32,'67950057-2cbb-4e9f-b18d-35161abaa7e6','920ba34a827bab4f',2,'2025-08-28 12:42:58');
INSERT INTO auth_qr VALUES(33,'67950057-2cbb-4e9f-b18d-35161abaa7e6','a240d2be451557b5',2,'2025-08-28 12:44:10');
INSERT INTO auth_qr VALUES(34,'67950057-2cbb-4e9f-b18d-35161abaa7e6','66d010193f1b1198',0,'2025-08-28 14:40:54');
INSERT INTO auth_qr VALUES(35,'e833b589-8670-4f22-9083-f9f2149163f4','82315b89702e384f',2,'2025-08-28 15:02:35');
INSERT INTO auth_qr VALUES(36,'e833b589-8670-4f22-9083-f9f2149163f4','d55245af043c9f10',0,'2025-08-28 15:03:55');
INSERT INTO auth_qr VALUES(37,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','9755ec83cdf24e8c',0,'2025-08-28 15:29:31');
INSERT INTO auth_qr VALUES(38,'67950057-2cbb-4e9f-b18d-35161abaa7e6','95e6fc285281676c',0,'2025-08-28 15:36:16');
INSERT INTO auth_qr VALUES(39,'67950057-2cbb-4e9f-b18d-35161abaa7e6','c1eceb4a75385306',0,'2025-08-28 15:49:24');
INSERT INTO auth_qr VALUES(40,'67950057-2cbb-4e9f-b18d-35161abaa7e6','5687832eeb6befa0',0,'2025-08-28 15:53:48');
INSERT INTO auth_qr VALUES(41,'cb261a65-c2d4-40e3-b79f-b807fa177158','094619c8bd80f291',0,'2025-08-28 16:55:28');
INSERT INTO auth_qr VALUES(42,'e833b589-8670-4f22-9083-f9f2149163f4','c05a60106754ae80',3,'2025-08-28 16:58:16');
INSERT INTO auth_qr VALUES(43,'cb261a65-c2d4-40e3-b79f-b807fa177158','3224e3b248e82ab5',1,'2025-08-28 16:58:46');
INSERT INTO auth_qr VALUES(44,'67950057-2cbb-4e9f-b18d-35161abaa7e6','f9e30c43bc163398',1,'2025-08-28 16:59:27');
INSERT INTO auth_qr VALUES(45,'e833b589-8670-4f22-9083-f9f2149163f4','bac29a7fa65cdc9e',0,'2025-08-28 17:09:09');
INSERT INTO auth_qr VALUES(46,'e833b589-8670-4f22-9083-f9f2149163f4','604828a86580efcd',0,'2025-08-28 17:10:23');
INSERT INTO auth_qr VALUES(47,'bd8571d6-6593-492d-9750-db9dd395b282','041fbd17ced9fa70',0,'2025-08-28 17:11:28');
INSERT INTO auth_qr VALUES(48,'e833b589-8670-4f22-9083-f9f2149163f4','869aed18e86c01a9',0,'2025-08-28 17:12:14');
INSERT INTO auth_qr VALUES(49,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','4692fc54f3b7612c',0,'2025-08-28 17:20:43');
INSERT INTO auth_qr VALUES(50,'e833b589-8670-4f22-9083-f9f2149163f4','fc22814314f89d4c',2,'2025-08-28 17:21:14');
INSERT INTO auth_qr VALUES(51,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','147acc43e1e6ef22',3,'2025-08-28 17:21:47');
INSERT INTO auth_qr VALUES(52,'e833b589-8670-4f22-9083-f9f2149163f4','776e2cf056eb2137',2,'2025-08-28 17:22:26');
INSERT INTO auth_qr VALUES(53,'e833b589-8670-4f22-9083-f9f2149163f4','a4867106a7f2a752',0,'2025-08-28 17:23:28');
INSERT INTO auth_qr VALUES(54,'e833b589-8670-4f22-9083-f9f2149163f4','89bedec9d1515674',1,'2025-08-28 17:25:01');
INSERT INTO auth_qr VALUES(55,'cb261a65-c2d4-40e3-b79f-b807fa177158','1b2038d91fcb798d',1,'2025-08-28 17:25:35');
INSERT INTO auth_qr VALUES(56,'e833b589-8670-4f22-9083-f9f2149163f4','de32720cc3692e81',1,'2025-08-28 17:26:19');
INSERT INTO auth_qr VALUES(57,'e833b589-8670-4f22-9083-f9f2149163f4','8da5a65a6161c805',1,'2025-08-28 17:27:21');
INSERT INTO auth_qr VALUES(58,'e833b589-8670-4f22-9083-f9f2149163f4','878034b42b6f6e3f',0,'2025-08-28 17:29:02');
INSERT INTO auth_qr VALUES(59,'e833b589-8670-4f22-9083-f9f2149163f4','4831682f36f786f7',0,'2025-08-28 17:30:47');
INSERT INTO auth_qr VALUES(60,'e833b589-8670-4f22-9083-f9f2149163f4','d3a46e1290602691',0,'2025-08-28 17:32:24');
CREATE TABLE auth_nfc (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    nfc_hash BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    regi_uuid TEXT NOT NULL,
    owner_uuid TEXT NOT NULL,
    pin_hash TEXT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (regi_uuid) REFERENCES users (uuid),
    FOREIGN KEY (owner_uuid) REFERENCES users (uuid)
);
CREATE TABLE door_status (
    auth_code BOOLEAN NOT NULL,
    button BOOLEAN NOT NULL,
    nfc BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    remote_open BOOLEAN NOT NULL,
    remote_open_by_uuid TEXT NOT NULL,
    remote_open_used BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (auth_code) REFERENCES auth_qr (auth_code)
);
CREATE TABLE kakaowork_bot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    app_key TEXT NOT NULL UNIQUE,
    kw_space_id TEXT NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);
INSERT INTO kakaowork_bot VALUES(1,'DY@25Make - MAKE AMS Bot','87d4fca2.bd7624ded45a4b38a2aadcca72ec732f','255534',1,'2025-08-28 01:34:26');
CREATE TABLE user_link_kakaowork (
    user_uuid TEXT PRIMARY KEY,
    bot_id INTEGER NOT NULL,
    kw_id TEXT NOT NULL UNIQUE,
    kw_name TEXT NOT NULL,
    kw_email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid),
    FOREIGN KEY (bot_id) REFERENCES kakaowork_bot (id)
);
INSERT INTO user_link_kakaowork VALUES('6fd50e6e-4390-4b3d-85b9-7066511b6ca7',1,'11022704','최가온','munggu1107@gmail.com','2025-08-28 08:57:51');
INSERT INTO user_link_kakaowork VALUES('67950057-2cbb-4e9f-b18d-35161abaa7e6',1,'10980848','이건희','gi6791991@gmail.com','2025-08-28 09:50:41');
INSERT INTO user_link_kakaowork VALUES('e833b589-8670-4f22-9083-f9f2149163f4',1,'11022739','송명근','gepoliu2468@gmail.com','2025-08-28 11:13:07');
INSERT INTO user_link_kakaowork VALUES('17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f',1,'10983603','이가윤','diseuji@gmail.com','2025-08-28 15:28:35');
INSERT INTO user_link_kakaowork VALUES('cb261a65-c2d4-40e3-b79f-b807fa177158',1,'11144576','이동훈','ppqq9266@gmail.com','2025-08-28 16:54:55');
INSERT INTO user_link_kakaowork VALUES('bd8571d6-6593-492d-9750-db9dd395b282',1,'10983552','유건우','gwyou1127@gmail.com','2025-08-28 17:10:27');
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NOT NULL,
    setting_key TEXT NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type TEXT NOT NULL DEFAULT 'string',
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    updated_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (user_uuid) REFERENCES users (uuid),
    UNIQUE(user_uuid, setting_key)
);
INSERT INTO user_settings VALUES(3,'67950057-2cbb-4e9f-b18d-35161abaa7e6','first_login','false','boolean','2025-08-28 01:12:36','2025-08-28 01:12:36');
INSERT INTO user_settings VALUES(5,'96ee3969-1c8e-4ab0-a9d2-d5c1e336396b','first_login','false','boolean','2025-08-28 01:29:08','2025-08-28 01:29:08');
INSERT INTO user_settings VALUES(43,'6fd50e6e-4390-4b3d-85b9-7066511b6ca7','first_login','false','boolean','2025-08-28 08:55:36','2025-08-28 08:55:36');
INSERT INTO user_settings VALUES(44,'6fd50e6e-4390-4b3d-85b9-7066511b6ca7','notification_login','true','boolean','2025-08-28 08:57:39','2025-08-28 08:57:39');
INSERT INTO user_settings VALUES(57,'67950057-2cbb-4e9f-b18d-35161abaa7e6','notification_door_access','1','boolean','2025-08-28 09:50:41','2025-08-28 09:50:41');
INSERT INTO user_settings VALUES(62,'e833b589-8670-4f22-9083-f9f2149163f4','first_login','0','boolean','2025-08-28 11:12:34','2025-08-28 11:12:34');
INSERT INTO user_settings VALUES(66,'e833b589-8670-4f22-9083-f9f2149163f4','notification_login','1','boolean','2025-08-28 11:18:00','2025-08-28 11:18:00');
INSERT INTO user_settings VALUES(67,'e833b589-8670-4f22-9083-f9f2149163f4','notification_door_access','0','boolean','2025-08-28 11:18:01','2025-08-28 11:18:01');
INSERT INTO user_settings VALUES(69,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','first_login','0','boolean','2025-08-28 15:28:14','2025-08-28 15:28:14');
INSERT INTO user_settings VALUES(70,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','notification_login','1','boolean','2025-08-28 15:28:35','2025-08-28 15:28:35');
INSERT INTO user_settings VALUES(71,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','notification_door_access','1','boolean','2025-08-28 15:28:35','2025-08-28 15:28:35');
INSERT INTO user_settings VALUES(73,'67950057-2cbb-4e9f-b18d-35161abaa7e6','notification_login','1','boolean','2025-08-28 16:11:50','2025-08-28 16:11:50');
INSERT INTO user_settings VALUES(75,'cb261a65-c2d4-40e3-b79f-b807fa177158','first_login','0','boolean','2025-08-28 16:54:33','2025-08-28 16:54:33');
INSERT INTO user_settings VALUES(76,'cb261a65-c2d4-40e3-b79f-b807fa177158','notification_login','1','boolean','2025-08-28 16:54:55','2025-08-28 16:54:55');
INSERT INTO user_settings VALUES(77,'cb261a65-c2d4-40e3-b79f-b807fa177158','notification_door_access','1','boolean','2025-08-28 16:54:55','2025-08-28 16:54:55');
INSERT INTO user_settings VALUES(79,'158fe3ba-4d61-46c1-86ae-3c1908ac91c7','first_login','0','boolean','2025-08-28 17:04:55','2025-08-28 17:04:55');
INSERT INTO user_settings VALUES(81,'bd8571d6-6593-492d-9750-db9dd395b282','first_login','0','boolean','2025-08-28 17:10:12','2025-08-28 17:10:12');
INSERT INTO user_settings VALUES(82,'bd8571d6-6593-492d-9750-db9dd395b282','notification_login','1','boolean','2025-08-28 17:10:27','2025-08-28 17:10:27');
INSERT INTO user_settings VALUES(83,'bd8571d6-6593-492d-9750-db9dd395b282','notification_door_access','1','boolean','2025-08-28 17:10:27','2025-08-28 17:10:27');
CREATE TABLE request_open_door (
    device_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours')),
    FOREIGN KEY (device_id) REFERENCES devices (id)
);
CREATE TABLE log_access (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NULL,
    method TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    reason TEXT,
    timestamp TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);
INSERT INTO log_access VALUES(1,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 08:35:58');
INSERT INTO log_access VALUES(2,NULL,'BUTTON',0,'출입 거부','2025-08-28 08:38:03');
INSERT INTO log_access VALUES(3,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 08:39:17');
INSERT INTO log_access VALUES(4,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 11:33:20');
INSERT INTO log_access VALUES(5,NULL,'QR',0,'존재하지 않는 QR 코드','2025-08-28 11:33:33');
INSERT INTO log_access VALUES(6,NULL,'BUTTON',0,'출입 거부','2025-08-28 11:33:40');
INSERT INTO log_access VALUES(7,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 11:35:02');
INSERT INTO log_access VALUES(8,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 11:38:50');
INSERT INTO log_access VALUES(9,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 11:38:58');
INSERT INTO log_access VALUES(10,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 11:39:08');
INSERT INTO log_access VALUES(11,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 11:39:23');
INSERT INTO log_access VALUES(12,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 11:39:27');
INSERT INTO log_access VALUES(13,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 11:50:14');
INSERT INTO log_access VALUES(14,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:14:08');
INSERT INTO log_access VALUES(15,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:14:27');
INSERT INTO log_access VALUES(16,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:14:38');
INSERT INTO log_access VALUES(17,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:15:13');
INSERT INTO log_access VALUES(18,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:20:41');
INSERT INTO log_access VALUES(19,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:20:58');
INSERT INTO log_access VALUES(20,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:26:33');
INSERT INTO log_access VALUES(21,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:26:49');
INSERT INTO log_access VALUES(22,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:27:49');
INSERT INTO log_access VALUES(23,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:30:50');
INSERT INTO log_access VALUES(24,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:30:54');
INSERT INTO log_access VALUES(25,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:31:13');
INSERT INTO log_access VALUES(26,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:31:23');
INSERT INTO log_access VALUES(27,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:31:54');
INSERT INTO log_access VALUES(28,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:33:30');
INSERT INTO log_access VALUES(29,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:33:37');
INSERT INTO log_access VALUES(30,NULL,'QR',0,'존재하지 않는 QR 코드','2025-08-28 12:38:48');
INSERT INTO log_access VALUES(31,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:43:01');
INSERT INTO log_access VALUES(32,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:43:53');
INSERT INTO log_access VALUES(33,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:44:13');
INSERT INTO log_access VALUES(34,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 12:44:47');
INSERT INTO log_access VALUES(35,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 12:46:07');
INSERT INTO log_access VALUES(36,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 15:02:38');
INSERT INTO log_access VALUES(37,NULL,'BUTTON',0,'출입 거부','2025-08-28 15:02:48');
INSERT INTO log_access VALUES(38,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 15:03:00');
INSERT INTO log_access VALUES(39,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 15:03:09');
INSERT INTO log_access VALUES(40,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 15:03:17');
INSERT INTO log_access VALUES(41,'e833b589-8670-4f22-9083-f9f2149163f4','QR',0,'만료된 QR 코드','2025-08-28 15:03:39');
INSERT INTO log_access VALUES(42,'e833b589-8670-4f22-9083-f9f2149163f4','QR',0,'만료된 QR 코드','2025-08-28 15:04:00');
INSERT INTO log_access VALUES(43,NULL,'BUTTON',0,'출입 거부','2025-08-28 15:04:31');
INSERT INTO log_access VALUES(44,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 16:58:21');
INSERT INTO log_access VALUES(45,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 16:58:34');
INSERT INTO log_access VALUES(46,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 16:58:48');
INSERT INTO log_access VALUES(47,'cb261a65-c2d4-40e3-b79f-b807fa177158','QR',1,'QR 인증 성공','2025-08-28 16:59:01');
INSERT INTO log_access VALUES(48,'67950057-2cbb-4e9f-b18d-35161abaa7e6','QR',1,'QR 인증 성공','2025-08-28 16:59:33');
INSERT INTO log_access VALUES(49,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:21:16');
INSERT INTO log_access VALUES(50,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','QR',1,'QR 인증 성공','2025-08-28 17:21:54');
INSERT INTO log_access VALUES(51,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:22:07');
INSERT INTO log_access VALUES(52,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','QR',1,'QR 인증 성공','2025-08-28 17:22:11');
INSERT INTO log_access VALUES(53,'17fcb5ae-57f3-4d0b-bc3c-bcf74b8de52f','QR',1,'QR 인증 성공','2025-08-28 17:22:19');
INSERT INTO log_access VALUES(54,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:22:28');
INSERT INTO log_access VALUES(55,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:22:45');
INSERT INTO log_access VALUES(56,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 17:23:47');
INSERT INTO log_access VALUES(57,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 17:23:54');
INSERT INTO log_access VALUES(58,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 17:23:59');
INSERT INTO log_access VALUES(59,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 17:24:05');
INSERT INTO log_access VALUES(60,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 17:24:09');
INSERT INTO log_access VALUES(61,NULL,'NFC',0,'등록되지 않은 카드','2025-08-28 17:24:15');
INSERT INTO log_access VALUES(62,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:25:05');
INSERT INTO log_access VALUES(63,'cb261a65-c2d4-40e3-b79f-b807fa177158','QR',1,'QR 인증 성공','2025-08-28 17:25:45');
INSERT INTO log_access VALUES(64,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:26:23');
INSERT INTO log_access VALUES(65,'e833b589-8670-4f22-9083-f9f2149163f4','QR',1,'QR 인증 성공','2025-08-28 17:27:32');
CREATE TABLE log_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_uuid TEXT NOT NULL,
    change_status TEXT NOT NULL,
    auth_code BOOLEAN NOT NULL,
    button BOOLEAN NOT NULL,
    nfc BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    remote_open BOOLEAN NOT NULL,
    remote_open_by_uuid TEXT NOT NULL,
    remote_open_used BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+9 hours'))
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user_verify',8);
INSERT INTO sqlite_sequence VALUES('user_settings',83);
INSERT INTO sqlite_sequence VALUES('auth_qr',60);
INSERT INTO sqlite_sequence VALUES('kakaowork_bot',1);
INSERT INTO sqlite_sequence VALUES('log_access',65);
COMMIT;
