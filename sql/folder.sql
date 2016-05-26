CREATE TABLE `fypress_folder` (
  `folder_id` bigint(20) UNSIGNED NOT NULL,
  `folder_parent` bigint(20) DEFAULT NULL,
  `folder_depth` tinyint(4) DEFAULT NULL,
  `folder_left` bigint(20) UNSIGNED DEFAULT NULL,
  `folder_right` bigint(20) DEFAULT NULL,
  `folder_slug` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_seo_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `folder_created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_folder`
  ADD PRIMARY KEY (`folder_id`),
  ADD UNIQUE KEY `folder_slug` (`folder_slug`),
  ADD UNIQUE KEY `folder_name` (`folder_slug`),
  ADD KEY `folder_modified` (`folder_modified`),
  ADD KEY `folder_id_parent` (`folder_left`),
  ADD KEY `folder_left` (`folder_left`),
  ADD KEY `folder_right` (`folder_right`),
  ADD KEY `folder_parent` (`folder_parent`),
  ADD KEY `folder_deth` (`folder_depth`);


ALTER TABLE `fypress_folder`
  MODIFY `folder_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;