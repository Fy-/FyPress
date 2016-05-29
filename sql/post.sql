CREATE TABLE `fypress_post` (
  `post_id` bigint(20) UNSIGNED NOT NULL,
  `post_user_id` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `post_created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `post_content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_title` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_excerpt` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_status` set('publish','draft','pending','trash','inherit') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'publish',
  `post_comment_status` set('open','closed') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'open',
  `post_slug` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `post_modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `post_parent` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `post_guid` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `post_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'post',
  `post_comment_count` bigint(20) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_post`
  ADD PRIMARY KEY (`post_id`),
  ADD KEY `post_user_id` (`post_user_id`),
  ADD KEY `post_date` (`post_created`),
  ADD KEY `post_guid` (`post_guid`),
  ADD KEY `post_status` (`post_status`);


ALTER TABLE `fypress_post`
  MODIFY `post_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

CREATE TABLE `fypress_post_meta` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `post_meta_id_post` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `post_meta_key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_meta_value` longtext COLLATE utf8mb4_unicode_ci
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_post_meta`
  ADD PRIMARY KEY (`post_meta_id_post`,`post_meta_key`),
  ADD UNIQUE KEY `id` (`id`);


ALTER TABLE `fypress_post_meta`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;