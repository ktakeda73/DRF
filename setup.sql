INSERT INTO public."W01_Dispatch"
(created_dt, updated_dt, corporation)
VALUES(now(), now(), 'ＸＸＸＸ');

INSERT INTO public."A01_Auth"
(created_dt, updated_dt, auth_name, auth_group, "user", attendance, leave, absence, holiday_work, expenses)
VALUES(now(), now(), '[1,1,1,1]', '[1,1,1,1]', '[1,1,1,1]', '[1,1,1,1]', '[1,1,1,1]', '[1,1,1,1]', '[1,1,1,1]', '[1,1,1,1]');

INSERT INTO public."W03_Department"
(created_dt, updated_dt, department)
VALUES(now(), now(), 'ＸＸＸＸＸＸＸＸ');

INSERT INTO public."F01_User"
(created_dt, updated_dt, userid, username, email, default_password, default_salt, "password", salt, is_active, is_superuser, auth_name_id, dispatch_id, department_id)
VALUES(now(), now(), 'RESC000001', 'ＸＸ　ＸＸ', 'xxxxx@xx.xx', '7d8a0838ce8e19b26e45fdd0b72954aac7e712a8d8f0cd7bedca3281217b5c76', 'xxxx', '7d8a0838ce8e19b26e45fdd0b72954aac7e712a8d8f0cd7bedca3281217b5c76', 'xxxx', true, true, 1, 1, 1);

INSERT INTO public."W02_Workplace"
(created_dt, updated_dt, workplace, dispatch_id)
VALUES(now(), now(), '小川町', 1),
(now(), now(), '豊洲', 1);

INSERT INTO public."F04.02_Absence_Division"
(created_dt, updated_dt, division)
VALUES(now(), now(), '遅刻'),
(now(), now(), '欠勤'),
(now(), now(), '半休（午前）'),
(now(), now(), '半休（午後）'),
(now(), now(), '有給');

INSERT INTO public."F04.01_Absence_Reason"
(created_dt, updated_dt, reson)
VALUES(now(), now(), '体調不良'),
(now(), now(), '電車遅延'),
(now(), now(), '寝坊'),
(now(), now(), '予定休');
