SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;

CREATE TABLE IF NOT EXISTS `fypress_comment` (
  `comment_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `comment_user_id` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `comment_post_id` bigint(20) NOT NULL,
  `comment_parent` bigint(20) NOT NULL,
  `comment_created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `comment_content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment_status` set('published','pending','spam') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `comment_user_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `comment_user_uri` varchar(155) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `comment_user_email` varchar(155) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `comment_user_ip` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`comment_id`),
  KEY `comment_user_id` (`comment_user_id`),
  KEY `comment_created` (`comment_created`),
  KEY `comment_status` (`comment_status`),
  KEY `comment_post_id` (`comment_post_id`),
  KEY `comment_parent` (`comment_parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `fypress_folder` (
  `folder_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `folder_parent` bigint(20) NOT NULL DEFAULT '0',
  `folder_depth` tinyint(4) NOT NULL DEFAULT '0',
  `folder_left` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `folder_right` bigint(20) NOT NULL DEFAULT '0',
  `folder_slug` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_guid` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `folder_posts` int(11) NOT NULL DEFAULT '0',
  `folder_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_seo_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `folder_created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`folder_id`),
  KEY `folder_modified` (`folder_modified`),
  KEY `folder_left` (`folder_left`),
  KEY `folder_right` (`folder_right`),
  KEY `folder_parent` (`folder_parent`),
  KEY `folder_deth` (`folder_depth`),
  KEY `folder_guid` (`folder_guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `fypress_media` (
  `media_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `media_hash` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_modified` datetime NOT NULL,
  `media_type` set('file','image','resize','local','oembed') COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_guid` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_name` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `media_data` text COLLATE utf8mb4_unicode_ci,
  `media_icon` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_html` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`media_id`),
  UNIQUE KEY `media_guid` (`media_guid`),
  UNIQUE KEY `media_hash` (`media_hash`),
  KEY `media_type` (`media_type`),
  KEY `media_modified` (`media_modified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `fypress_option` (
  `option_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `option_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `option_value` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_load` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`option_id`),
  UNIQUE KEY `option_name` (`option_name`),
  KEY `autoload` (`option_load`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `fypress_post` (
  `post_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `post_user_id` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `post_folder_id` bigint(20) UNSIGNED NOT NULL,
  `post_created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `post_content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_title` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_excerpt` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_status` set('published','draft','pending','trash','revision') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'draft',
  `post_comment_status` set('open','closed') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'open',
  `post_slug` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `post_modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `post_parent` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `post_guid` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `post_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'post',
  `post_comment_count` bigint(20) NOT NULL DEFAULT '0',
  `post_image_id` bigint(20) DEFAULT NULL,
  `post_views` bigint(20) NOT NULL DEFAULT '0',
  `post_nav` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `post_user_id` (`post_user_id`),
  KEY `post_date` (`post_created`),
  KEY `post_guid` (`post_guid`),
  KEY `post_status` (`post_status`),
  KEY `post_folder_id` (`post_folder_id`),
  KEY `post_image_id` (`post_image_id`),
  KEY `posts_views` (`post_views`),
  KEY `post_nav` (`post_nav`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `fypress_user` (
  `user_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_login` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_nicename` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_firstname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_lastname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_url` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_registered` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `user_activation_key` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_status` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_email` (`user_email`),
  UNIQUE KEY `user_login` (`user_login`),
  KEY `user_email_2` (`user_email`),
  KEY `user_login_2` (`user_login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `fypress_usermeta` (
  `usermeta_id_user` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `usermeta_key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usermeta_value` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`usermeta_id_user`,`usermeta_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
COMMIT;
