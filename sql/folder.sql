CREATE TABLE `fypress_folder` (
  `folder_id` bigint(20) UNSIGNED NOT NULL,
  `folder_parent` bigint(20) NOT NULL DEFAULT '0',
  `folder_depth` tinyint(4) NOT NULL DEFAULT '0',
  `folder_left` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `folder_right` bigint(20) NOT NULL DEFAULT '0',
  `folder_slug` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_guid` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `folder_posts` int(11) NOT NULL DEFAULT '0',
  `folder_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_seo_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `folder_modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `folder_created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_folder`
  ADD PRIMARY KEY (`folder_id`),
  ADD KEY `folder_modified` (`folder_modified`),
  ADD KEY `folder_id_parent` (`folder_left`),
  ADD KEY `folder_left` (`folder_left`),
  ADD KEY `folder_right` (`folder_right`),
  ADD KEY `folder_parent` (`folder_parent`),
  ADD KEY `folder_deth` (`folder_depth`),
  ADD KEY `folder_guid` (`folder_guid`);


ALTER TABLE `fypress_folder`
  MODIFY `folder_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

# INSERT INTO `fypress_folder` (`folder_id`, `folder_parent`, `folder_depth`, `folder_left`, `folder_right`, `folder_slug`, `folder_posts`, `folder_name`, `folder_content`, `folder_seo_content`, `folder_modified`, `folder_created`) VALUES (1, 0, 0, 0, 0, '', 0, 'Default category (/)', 'Default category (/)', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00');
