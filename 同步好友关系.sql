--     NORMAL = 0
--     LIKED = 1
--     LIKE = 2
--     FRIEND = 3
--     STRANGER_BLOCKED = 4
--     FRD_BLOCKED = 7
--     STRANGER_BLOCK = 8
--     FRD_BLOCK = 11
--     STRANGER_INTER_BLOCK = 12
--     FRD_INTER_BLOCK = 15

--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-数据准备-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
----------------------**************拉黑关系表*************------------------------
-- pw_block
----------------------**************拉黑关系表*************------------------------

----------------------**************好友关系表*************------------------------
-- 创建contact总表 每个shard的数据需提前导入到目的db中
-- DROP TABLE if EXISTS pw_contact_all;
-- CREATE TABLE pw_contact_all (
--     contact_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     state           smallint NOT NULL DEFAULT 0,
--     sync_id         bigint NOT NULL DEFAULT 0,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );

-- 依次插入每个shard的contact信息
-- INSERT INTO pw_contact_all (uid,tuid,state,sync_id,update_time,create_time)
-- 	select uid,tuid,state,sync_id,create_time,create_time from pw_contact_shard1;
-- INSERT INTO pw_contact_all (uid,tuid,state,sync_id,update_time,create_time)
-- 	select uid,tuid,state,sync_id,create_time,create_time from pw_contact_shard2;
-- INSERT INTO pw_contact_all (uid,tuid,state,sync_id,update_time,create_time)
-- 	select uid,tuid,state,sync_id,create_time,create_time from pw_contact_shard3;
-- select count(*) from pw_contact_all;

-- 清除无效数据
-- select *  from pw_contact_all where uid=tuid;
-- select * from  (select uid,tuid,count(*) as num from pw_contact_all where state=0 group by uid,tuid) as tmp where tmp.num>1;

----------------------**************好友关系表*************------------------------

----------------------**************喜欢请求关系表*************------------------------
-- 创建contact_request_all总表 每个shard的数据需提前导入到目的db中
-- DROP TABLE if EXISTS pw_contact_request_all;
-- CREATE TABLE pw_contact_request_all (
--    contact_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     state           smallint NOT NULL DEFAULT 0,
--     sync_id         bigint NOT NULL DEFAULT 0,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
-- INSERT INTO pw_contact_request_all (uid,tuid,state,sync_id,update_time,create_time)
-- 	select uid,tuid,state,sync_id,update_time,update_time from pw_contact_request_shard1;
-- INSERT INTO pw_contact_request_all (uid,tuid,state,sync_id,update_time,create_time)
-- 	select uid,tuid,state,sync_id,update_time,update_time from pw_contact_request_shard2;
-- INSERT INTO pw_contact_request_all (uid,tuid,state,sync_id,update_time,create_time)
-- 	select uid,tuid,state,sync_id,update_time,update_time from pw_contact_request_shard3;
-- 清除无效数据
-- delete from pw_contact_request_all where uid=tuid;
-- select * from
-- 	(select uid,tuid,count(*) as num from pw_contact_request_all where state=0 group by uid,tuid) as tmp where tmp.num>1;


----------------------**************喜欢请求关系表*************------------------------

----------------------**************用户昵称表*************------------------------
-- DROP TABLE if EXISTS pw_user_name;
-- CREATE TABLE pw_user_name (
-- 		contact_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
-- 		name 									varchar
-- );
-- create index pw_user_name_uid on pw_user_name(uid);
-- insert into pw_user_name (uid,name)
-- 	select uid,name from pw_user;
-- insert into pw_user_name (uid,name)
-- 	select uid,name from pw_user_shard2;
-- insert into pw_user_name (uid,name)
-- 	select uid,name from pw_user_shard3;

-- select * from  (select uid,count(*) as num from pw_user_name group by uid) as tmp where tmp.num>=2;

----------------------**************用户昵称表*************------------------------

----------------------**************好友备注表*************------------------------
-- DROP TABLE IF EXISTS contact_note_all;
-- CREATE TABLE contact_note_all (
-- 		id BIGSERIAL PRIMARY KEY,
--     uid integer NOT NULL,
--     tuid integer NOT NULL,
--     note character varying
-- );
-- CREATE index contact_note_all_uids on contact_note_all(uid,tuid);
-- create index contact_note_all_tuid on contact_note_all(tuid);
-- insert into contact_note_all(uid,tuid,note)
-- 	select uid,tuid,note from pw_contact_note;
-- insert into contact_note_all(uid,tuid,note)
-- 	select uid,tuid,note from pw_contact_note_shard2;
-- insert into contact_note_all(uid,tuid,note)
-- 	select uid,tuid,note from pw_contact_note_shard3;

-- select * from  (select uid,count(*) as num from contact_note_all_uids group by uid) as tmp where tmp.num>=2;

----------------------**************好友备注表*************------------------------

--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-数据准备-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*



----------------**************************  request 整理开始  *************************----------------------------

---------------pw_contact_request_tmp:喜欢请求排除存在好友关系的表  创建语句------------------------
-- pw_contact_request_tmp中数据为在request,但不在contact表中的数据

-- DROP TABLE IF EXISTS pw_contact_request_tmp;
-- create table pw_contact_request_tmp  as
-- 	SELECT pc.contact_id as contact_id, pc.uid, pc.tuid,pc.state, pc.create_time, pc.update_time
-- 		FROM pw_contact_request_all pc left join pw_contact_all pa
-- 			on (pc.uid = pa.uid and pc.tuid=pa.tuid)
-- 				where pc.state = 0 and (pa.state=1 or pa.contact_id is null);

-- select * from pw_contact_request_tmp;
---------------pw_contact_request_tmp:喜欢请求排除存在好友关系的表  创建语句------------------------

---------------------------pw_contact_request_mutual_tmp-----------------------------
-- 此表为存在互相喜欢 但是好友表不存在的数据 目标关系为互为好友

-- DROP TABLE if EXISTS pw_contact_request_mutual_tmp;
-- create table pw_contact_request_mutual_tmp as
--    select pc.contact_id, pc.uid, pc.tuid, pc.state,pc.create_time, pc.update_time
-- 			from pw_contact_request_tmp pc inner join pw_contact_request_tmp pt
-- 				on (pc.uid=pt.tuid and pc.tuid=pt.uid);

-- select * from pw_contact_request_mutual_tmp;
---------------------------pw_contact_request_mutual_tmp-----------------------------

----------------------relation_like----------------------
-- 此表存储已处理好的喜欢数据

-- DROP TABLE IF EXISTS relation_like;
-- CREATE TABLE relation_like (
--     relation_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     hide                    smallint NOT NULL DEFAULT 0,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );

-- 插入喜欢数据
-- INSERT INTO relation_like (uid,tuid,relation_type,update_time,create_time)
-- 	select pt.uid,pt.tuid,2,pt.update_time, pt.update_time
-- 		from pw_contact_request_tmp pt left join pw_contact_request_mutual_tmp pm
-- 			on pt.uid=pm.uid and pt.tuid=pm.tuid  where pm.uid is null;

-- 插入被喜欢数据
-- INSERT INTO relation_like (uid,tuid,relation_type,update_time,create_time)
-- 	select tuid,uid,1,update_time,update_time from relation_like where relation_type=2

-- 查看是否存在重复数据
-- select * from  (select uid,tuid,count(*) as num from relation_like group by uid,tuid) as tmp where tmp.num>=2;
----------------------relation_like----------------------

----------------**************************  request 整理完毕  *************************----------------------------


----------------**************************  contact 整理开始  *************************----------------------------
----------------------relation_frd----------------------
-- 此表存储已处理好的喜欢数据
-- DROP TABLE IF EXISTS relation_frd;
-- CREATE TABLE relation_frd (
--     relation_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     hide                    smallint NOT NULL DEFAULT 0,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
----------------查询好友关系 但是只存在单条数据---------------
-- SELECT count(*) FROM pw_contact_all pc left join pw_contact_all pa
-- 	on (pc.uid=pa.tuid and pc.tuid=pa.uid)
-- 		where pc.state = 0 and pa.contact_id is null;
----------------查询好友关系 但是只存在单条数据---------------


-------------------pw_contact_complete_tmp--------------------------
-- 好友关系表中的好友加入到临时表 此表中的数据都为互为好友 处理单条垃圾数据的情况
-- create table pw_contact_complete_tmp as
-- select pc.contact_id, pc.uid, pc.tuid,  pc.state, pc.create_time
-- from pw_contact_all pc where pc.state=0
-- union all
-- SELECT pc.contact_id, pc.tuid as uid, pc.uid as tuid,  pc.state, pc.create_time
-- FROM pw_contact_all pc left join pw_contact_all pa on (pc.uid=pa.tuid and pc.tuid=pa.uid)
-- where pc.state = 0 and pa.contact_id is null -- 存在问题！！！！！！！
-------------------pw_contact_complete_tmp--------------------------

-------------------插入好友数据到relation_frd--------------------------
-- 插入好友数据到relation_frd
--
-- select count(*) from pw_contact_all where state=0; -- 237820
-- select count(*) from pw_contact_all pc inner join pw_contact_all pc1
-- 	on pc.uid=pc1.tuid and pc.tuid=pc1.uid and pc.state=pc1.state where pc.state=0; -- 230370
-- select count(*) from pw_contact_all pc left join pw_contact_all pa
-- 	on (pc.uid=pa.tuid and pc.tuid=pa.uid)
-- 		where pc.state = 0 and (pa.state!=0 or pa.uid is null);

-- insert into relation_frd (uid,tuid,relation_type,update_time,create_time)
-- 		select  pc.uid,pc.tuid,3,pc.create_time,pc.create_time
-- 			from pw_contact_all pc where pc.state=0
-- 	union all
-- 		SELECT pc.tuid as uid, pc.uid as tuid, 3, pc.create_time, pc.create_time
-- 			FROM pw_contact_all pc left join pw_contact_all pa
-- 				on (pc.uid=pa.tuid and pc.tuid=pa.uid)
-- 					where pc.state = 0 and (pa.state!=0 or pa.contact_id is null);

-- 插入互相喜欢的数据到relation_frd
-- insert into relation_frd (uid,tuid,relation_type,update_time,create_time)
-- 	select  uid,tuid,3,update_time,update_time from pw_contact_request_mutual_tmp;

-- 删除自己和自己互为好友
-- select * from relation_frd where uid=tuid;

-- 查看是否存在重复数据  存在删除
-- select * from  (select uid,tuid,count(*) as num from relation_frd group by uid,tuid) as tmp where tmp.num>=2;
-- delete from relation_frd where uid=2485888 and tuid=993 and update_time <> (select max(update_time) from relation_frd where uid=2485888 and tuid=993 group by uid,tuid);

-------------------插入好友数据到relation_frd--------------------------
----------------**************************  contact 整理完毕  *************************----------------------------


----------------*************************  block 整理开始  ************************---------------------------
-- DROP TABLE if EXISTS relation_block;
-- CREATE TABLE relation_block (
--     id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
--
-- 获取双向拉黑
-- SELECT pb.uid,pb.tuid,pb.update_time FROM pw_block pb INNER JOIN pw_block pc ON pb.uid=pc.tuid AND pb.tuid=pc.uid;

-- 创建双向拉黑数据临时表 pw_inter_block_tmp
-- DROP TABLE IF EXISTS pw_inter_block_tmp;
-- create table pw_inter_block_tmp as
-- 	SELECT pb.uid,pb.tuid,pb.update_time
-- 		FROM pw_block pb INNER JOIN pw_block pc
-- 			ON pb.uid=pc.tuid AND pb.tuid=pc.uid;
-- select * from pw_inter_block_tmp;

-- 获取单向拉黑
-- SELECT pb.uid,pb.tuid,pb.update_time FROM pw_block pb left join pw_block pb1 on pb.uid=pb1.tuid and pb.tuid=pb1.uid where pb1.uid is null;
-- 创建单向拉黑数据临时表 pw_signle_block_tmp
-- DROP TABLE IF EXISTS pw_single_block_tmp;
-- CREATE TABLE pw_single_block_tmp AS
-- 		SELECT pb.uid,pb.tuid,pb.update_time
-- 			FROM pw_block pb left join pw_block pb1
-- 				on pb.uid=pb1.tuid and pb.tuid=pb1.uid
-- 					where pb1.uid is null;
-- select * from pw_single_block_tmp;

-- 插入双向拉黑数据 好友互相拉黑+陌生人互相拉黑
-- 插入好友互相拉黑
-- INSERT INTO relation_block (uid,tuid,relation_type,update_time,create_time)
-- 	SELECT pb.uid,pb.tuid,15,pb.update_time,pb.update_time FROM pw_inter_block_tmp pb INNER JOIN pw_contact_all pc
-- 		ON pb.uid=pc.uid AND pb.tuid=pc.tuid
-- 			where pc.state!=1;
-- select * from relation_block;
-- 插入陌生人互相拉黑
-- INSERT INTO relation_block (uid,tuid,relation_type,update_time,create_time)
-- 	SELECT pb.uid,pb.tuid,12,pb.update_time,pb.update_time FROM pw_inter_block_tmp pb LEFT JOIN relation_block rb
-- 		ON pb.uid=rb.uid AND pb.tuid=rb.tuid
-- 			where rb.uid is NULL;

-- 插入单向拉黑数据 好友单向拉黑+陌生人单向拉黑
-- 插入好友单向拉黑
-- INSERT INTO relation_block (uid,tuid,relation_type,update_time,create_time)
-- 	SELECT pb.uid,pb.tuid,11,pb.update_time,pb.update_time FROM pw_single_block_tmp pb INNER JOIN pw_contact_all pc
-- 		ON pb.uid=pc.uid AND pb.tuid=pc.tuid
-- 			where pc.state!=1;
-- 插入好友单向被拉黑
-- INSERT INTO relation_block (uid,tuid,relation_type,update_time,create_time)
-- 	SELECT tuid,uid,7,update_time,create_time from relation_block
-- 		where relation_type=11;

-- 插入陌生人单向拉黑
-- INSERT INTO relation_block (uid,tuid,relation_type,update_time,create_time)
-- 	SELECT pb.uid,pb.tuid,8,pb.update_time,pb.update_time FROM pw_single_block_tmp pb LEFT JOIN relation_block rb
-- 		ON pb.uid=rb.uid AND pb.tuid=rb.tuid
-- 			where rb.uid is NULL;
--
-- 插入陌生人单向被拉黑
-- INSERT INTO relation_block (uid,tuid,relation_type,update_time,create_time)
-- 	SELECT tuid,uid,4,update_time,create_time from relation_block
-- 		where relation_type=8;

----------------*************************  block 整理完毕  ************************---------------------------


----------------*************************  用户关系总表整理开始  ************************---------------------------
-- 创建用户关系临时表
-- drop table if EXISTS relationship_temp;
-- CREATE TABLE relationship_temp (
--     relation_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     hide                    smallint NOT NULL DEFAULT 0,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
-- create UNIQUE index relationship_temp_uids on relationship_temp(uid,tuid);
-- create index relationship_temp_tuid on relationship_temp(tuid);

-- 插入拉黑关系
-- insert into relationship_temp (uid,tuid,relation_type,update_time,create_time)
-- 	select uid,tuid,relation_type,update_time,create_time from relation_block;
-- 插入好友关系
-- insert into relationship_temp (uid,tuid,relation_type,update_time,create_time)
-- 	select frd.uid,frd.tuid,frd.relation_type,frd.update_time,frd.create_time
-- 		from relation_frd frd LEFT JOIN relation_block rb
-- 			on frd.uid=rb.uid and frd.tuid=rb.tuid
-- 				where rb.id is null;
-- 插入单向喜欢关系
-- insert into relationship_temp (uid,tuid,relation_type,update_time,create_time)
-- 	select rl.uid,rl.tuid,rl.relation_type,rl.update_time,rl.create_time
-- 		from relation_like rl LEFT JOIN relationship_temp rp
-- 			on rl.uid=rp.uid and rl.tuid=rp.tuid
-- 				where rp.relation_id is null;
----------------*************************  用户关系总表整理开始  ************************---------------------------


----------------*************************  用户关系shard表整理开始  ************************---------------------------

---------------清理shard中不存在的用户------------------
-- -- 创建用户关系shard临时表
-- drop table if EXISTS relationship_shard_tmp;
-- create table relationship_shard_tmp as
-- 	select us.shard_id as shard_id,rt.uid as uid,rt.tuid as tuid,rt.relation_type as relation_type,
-- 		un.name as tuser_name,cn.note as tuser_note,rt.update_time as update_time,rt.create_time as create_time
-- 			FROM relationship_temp rt
-- 				left join pw_user_shard us on rt.uid = us.shard_key
-- 				left join pw_user_name un on rt.tuid=un.uid
-- 				left join contact_note_all cn on rt.uid=cn.uid and rt.tuid=cn.tuid;
-- select * from relationship_shard_tmp where shard_id is null;
-- -- 删除不存在shard的用户关系
-- delete from relationship_shard_tmp
-- 	where uid in (select DISTINCT(uid) from relationship_shard_tmp where shard_id is NULL)
-- 		or tuid in (select DISTINCT(uid) from relationship_shard_tmp where shard_id is NULL);


---------------清理shard中不存在的用户------------------


-- --初始化shard1表
-- 创建用户关系shard1表
-- drop table if EXISTS pw_relationship_shard1;
-- drop SEQUENCE if EXISTS pw_relationship_shard1_sync_id;
-- CREATE SEQUENCE pw_relationship_shard1_sync_id
--     START WITH 10000000
--     INCREMENT BY 1
--     NO MINVALUE
--     NO MAXVALUE
--     CACHE 1;
--
-- CREATE TABLE pw_relationship_shard1 (
--     relation_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     hide                    smallint NOT NULL DEFAULT 0,
--     sync_id                 integer DEFAULT nextval('pw_relationship_shard1_sync_id'::regclass) NOT NULL,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
-- -- 插入到shard1中
-- INSERT INTO pw_relationship_shard1(uid,tuid,relation_type,update_time,create_time)
-- 	select uid,tuid,relation_type,update_time,create_time
-- 		FROM relationship_shard_tmp where shard_id=1;
-- --初始化shard2表
-- drop table if EXISTS pw_relationship_shard2;
-- drop SEQUENCE if EXISTS pw_relationship_shard2_sync_id;
-- CREATE SEQUENCE pw_relationship_shard2_sync_id
--     START WITH 10000000
--     INCREMENT BY 1
--     NO MINVALUE
--     NO MAXVALUE
--     CACHE 1;
--
-- CREATE TABLE pw_relationship_shard2 (
--     relation_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     hide                    smallint NOT NULL DEFAULT 0,
--     sync_id                 integer DEFAULT nextval('pw_relationship_shard2_sync_id'::regclass) NOT NULL,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
--
-- -- 插入到shard2中
-- INSERT INTO pw_relationship_shard2(uid,tuid,relation_type,update_time,create_time)
-- 	select uid,tuid,relation_type,update_time,create_time
-- 		FROM relationship_shard_tmp where shard_id=1;

-- --初始化shard3表
-- drop table if EXISTS pw_relationship_shard3;
-- drop SEQUENCE if EXISTS pw_relationship_shard3_sync_id;
-- CREATE SEQUENCE pw_relationship_shard3_sync_id
--     START WITH 10000000
--     INCREMENT BY 1
--     NO MINVALUE
--     NO MAXVALUE
--     CACHE 1;
--
-- CREATE TABLE pw_relationship_shard3 (
--     relation_id             BIGSERIAL PRIMARY KEY,
--     uid                     integer NOT NULL,
--     tuid                    integer NOT NULL,
--     relation_type           smallint NOT NULL DEFAULT 0,
--     hide                    smallint NOT NULL DEFAULT 0,
--     sync_id                 integer DEFAULT nextval('pw_relationship_shard3_sync_id'::regclass) NOT NULL,
--     update_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time             TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
-- 插入到shard3中
-- INSERT INTO pw_relationship_shard3(uid,tuid,relation_type,update_time,create_time)
-- 	select uid,tuid,relation_type,update_time,create_time
-- 		FROM relationship_shard_tmp where shard_id=1;

----------------*************************  用户关系shard表整理开始  ************************---------------------------



----------------************************* 同步新表用户关系到shard表 ***************************---------------------------------

-- INSERT INTO pw_relationship_shard1 (uid,tuid,relation_type,update_time,create_time)
-- 	select pn.uid,pn.tuid,pn.relation_type,pn.update_time,pn.create_time
-- 		from pw_relation_new pn left join pw_relationship_shard1 rs1
-- 			on pn.uid=rs1.uid and pn.tuid=rs1.tuid
-- 				where rs1.relation_id is null;


-- INSERT INTO pw_relationship_shard1 (uid,tuid,relation_type,update_time,create_time)
-- 	select pn.uid,pn.tuid,pn.relation_type,pn.update_time,pn.create_time
-- 		from pw_relation_new pn inner join pw_relationship_shard1 rs1
-- 			on pn.uid=rs1.uid and pn.tuid=rs1.tuid;
----------------************************* 同步新表用户关系到shard表 ***************************---------------------------------


----------------************************* 同步好友搜索用户关系到shard表 ***************************---------------------------------
-- DROP TABLE IF EXISTS user_relation_shard1;
-- CREATE TABLE user_relation_shard1 (
--     id            BIGSERIAL PRIMARY KEY,
--     uid           integer NOT NULL,
--     tuid          integer NOT NULL,
--     tuser_name    varchar,
--     relation_type smallint NOT NULL,
--     tuser_note    varchar,
--     update_time   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
--
-- CREATE UNIQUE INDEX user_relation_shard1_uids ON user_relation_shard1(uid,tuid);
-- CREATE INDEX user_relation_shard1_tuid ON user_relation_shard1(tuid);
--
-- insert into user_relation_shard1 (uid,tuid,tuser_name,tuser_note,relation_type,update_time,create_time)
-- 	SELECT uid,tuid,tuser_name,tuser_note,relation_type,update_time,create_time FROM relationship_shard_tmp
-- 		where shard_id=1;

-- DROP TABLE IF EXISTS user_relation_shard2;
-- CREATE TABLE user_relation_shard2 (
--     id            BIGSERIAL PRIMARY KEY,
--     uid           integer NOT NULL,
--     tuid          integer NOT NULL,
--     tuser_name    varchar,
--     relation_type smallint NOT NULL,
--     tuser_note    varchar,
--     update_time   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
--
-- CREATE UNIQUE INDEX user_relation_shard2_uids ON user_relation_shard2(uid,tuid);
-- CREATE INDEX user_relation_shard2_tuid ON user_relation_shard2(tuid);
--
-- insert into user_relation_shard2 (uid,tuid,tuser_name,tuser_note,relation_type,update_time,create_time)
-- 	SELECT uid,tuid,tuser_name,tuser_note,relation_type,update_time,create_time FROM relationship_shard_tmp
-- 		where shard_id=2;
--

-- DROP TABLE IF EXISTS user_relation_shard3;
-- CREATE TABLE user_relation_shard3 (
--     id            BIGSERIAL PRIMARY KEY,
--     uid           integer NOT NULL,
--     tuid          integer NOT NULL,
--     tuser_name    varchar,
--     relation_type smallint NOT NULL,
--     tuser_note    varchar,
--     update_time   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     create_time   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
-- );
--
-- CREATE UNIQUE INDEX user_relation_shard3_uids ON user_relation_shard3(uid,tuid);
-- CREATE INDEX user_relation_shard3_tuid ON user_relation_shard3(tuid);
--
-- insert into user_relation_shard3 (uid,tuid,tuser_name,tuser_note,relation_type,update_time,create_time)
-- 	SELECT uid,tuid,tuser_name,tuser_note,relation_type,update_time,create_time FROM relationship_shard_tmp
-- 		where shard_id=3;
