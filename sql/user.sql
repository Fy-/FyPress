CREATE TABLE `fypress_user` (
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `user_login` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_nicename` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_firstname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_lastname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_url` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_registered` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `user_activation_key` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_status` int(11) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `fypress_user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_login` (`user_login`),
  ADD KEY `user_email_2` (`user_email`),
  ADD KEY `user_login_2` (`user_login`);

ALTER TABLE `fypress_user`
  MODIFY `user_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

CREATE TABLE `fypress_user_meta` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_meta_id_user` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `user_meta_key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_meta_value` longtext COLLATE utf8mb4_unicode_ci
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_user_meta`
  ADD PRIMARY KEY (`user_meta_id_user`,`user_meta_key`),
  ADD UNIQUE KEY `id` (`id`);


ALTER TABLE `fypress_user_meta`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;