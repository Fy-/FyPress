CREATE TABLE `fypress_option` (
  `option_id` bigint(20) UNSIGNED NOT NULL,
  `option_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `option_value` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_load` tinyint(4) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `fypress_option`
  ADD PRIMARY KEY (`option_id`),
  ADD UNIQUE KEY `option_name` (`option_name`),
  ADD KEY `autoload` (`option_load`);


ALTER TABLE `fypress_option`
  MODIFY `option_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;