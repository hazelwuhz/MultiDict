CREATE TABLE `students` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT '姓名',
    `english` decimal(6,2) NOT NULL DEFAULT '0.00' COMMENT '英语成绩',
    `chinese` decimal(6,2) NOT NULL DEFAULT '0.00' COMMENT '语文成绩',
    `math` decimal(6,2) NOT NULL DEFAULT '0.00' COMMENT '数学成绩',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COMMENT = '学生表'

CREATE TABLE `teachers` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT '账号',
    `password` varchar(64) NOT NULL DEFAULT '' COMMENT '密码',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COMMENT = '教师账号表'


INSERT INTO `students` (`name`, `english`, `chinese`, `math`) VALUES('小王', 76, 60, 80);
INSERT INTO `students` (`name`, `english`, `chinese`) VALUES('小张', 90, 70);
INSERT INTO `students` (`name`, `chinese`, `math`) VALUES('小李', 88, 70);

SELECT * FROM `students` WHERE `name` = '小王';
SELECT `name`, `english` FROM `students` WHERE `english` > 60;
SELECT * FROM `students` WHERE `english` >=40 AND `chinese` >= 60;
SELECT * FROM `students` WHERE `english` >=40 OR `chinese` >= 60;

UPDATE `students` SET `english` = 78 WHERE `name` = '小王';
UPDATE `students` SET `english` = 76 WHERE `chinese` > 80;
UPDATE `students` SET `name` = '小王' WHERE `id`=3;
UPDATE `students` SET `name` = '大李' WHERE `id` = 3;

SELECT * FROM `students` WHERE `english` > 76 AND `chinese` > 50 AND `math` >0;

DELETE FROM `students` WHERE `name` = '小王';
DELETE FROM `students` WHERE `id` = 3;
DELETE FROM `students` WHERE `english` >=90;

