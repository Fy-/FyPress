CREATE TABLE `fypress_media` (
  `media_id` bigint(20) UNSIGNED NOT NULL,
  `media_hash` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_modified` datetime NOT NULL,
  `media_type` set('file','image','resize','local','oembed') COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_guid` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_name` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `media_data` text COLLATE utf8mb4_unicode_ci,
  `media_icon` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_html` text COLLATE utf8mb4_unicode_ci
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_media`
  ADD PRIMARY KEY (`media_id`),
  ADD UNIQUE KEY `media_guid` (`media_guid`),
  ADD UNIQUE KEY `media_hash` (`media_hash`),
  ADD KEY `media_type` (`media_type`),
  ADD KEY `media_modified` (`media_modified`);


ALTER TABLE `fypress_media`
  MODIFY `media_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;