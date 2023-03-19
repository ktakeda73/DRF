INSERT INTO public.api_dispatch
(created_dt, updated_dt, corporation)
VALUES(now(), now(), 'ＸＸＸＸ');
INSERT INTO public.api_userinfo
(created_dt, updated_dt, username, email, default_password, default_salt, "password", salt, dispatch_id)
VALUES(now(), now(), 'ＸＸ　ＸＸ', 'xxxxx@xx.xx', '7d8a0838ce8e19b26e45fdd0b72954aac7e712a8d8f0cd7bedca3281217b5c76', 'XXXX', '7d8a0838ce8e19b26e45fdd0b72954aac7e712a8d8f0cd7bedca3281217b5c76', 'XXXX', 1);
INSERT INTO public.api_workplace
(created_dt, updated_dt, workplace, dispatch_id)
VALUES(now(), now(), '小川町', 1),
(now(), now(), '豊洲', 1);
