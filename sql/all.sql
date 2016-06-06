--
-- Structure de la table `fypress_folder`
--

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fypress_media`
--

CREATE TABLE `fypress_media` (
  `media_id` bigint(20) UNSIGNED NOT NULL,
  `media_hash` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_modified` datetime NOT NULL,
  `media_type` set('file','image','resize','local','oembed') COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_guid` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_name` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `media_data` text COLLATE utf8mb4_unicode_ci,
  `media_icon` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_html` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fypress_option`
--

CREATE TABLE `fypress_option` (
  `option_id` bigint(20) UNSIGNED NOT NULL,
  `option_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `option_value` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_load` tinyint(4) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fypress_post`
--

CREATE TABLE `fypress_post` (
  `post_id` bigint(20) UNSIGNED NOT NULL,
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
  `post_nav` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fypress_post_meta`
--

CREATE TABLE `fypress_post_meta` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `post_meta_id_post` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `post_meta_key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_meta_value` longtext COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fypress_user`
--

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fypress_user_meta`
--

CREATE TABLE `fypress_user_meta` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_meta_id_user` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
  `user_meta_key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_meta_value` longtext COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `fypress_folder`
--
ALTER TABLE `fypress_folder`
  ADD PRIMARY KEY (`folder_id`),
  ADD KEY `folder_modified` (`folder_modified`),
  ADD KEY `folder_id_parent` (`folder_left`),
  ADD KEY `folder_left` (`folder_left`),
  ADD KEY `folder_right` (`folder_right`),
  ADD KEY `folder_parent` (`folder_parent`),
  ADD KEY `folder_deth` (`folder_depth`),
  ADD KEY `folder_guid` (`folder_guid`);

--
-- Index pour la table `fypress_media`
--
ALTER TABLE `fypress_media`
  ADD PRIMARY KEY (`media_id`),
  ADD UNIQUE KEY `media_guid` (`media_guid`),
  ADD UNIQUE KEY `media_hash` (`media_hash`),
  ADD KEY `media_type` (`media_type`),
  ADD KEY `media_modified` (`media_modified`);

--
-- Index pour la table `fypress_option`
--
ALTER TABLE `fypress_option`
  ADD PRIMARY KEY (`option_id`),
  ADD UNIQUE KEY `option_name` (`option_name`),
  ADD KEY `autoload` (`option_load`);

--
-- Index pour la table `fypress_post`
--
ALTER TABLE `fypress_post`
  ADD PRIMARY KEY (`post_id`),
  ADD KEY `post_user_id` (`post_user_id`),
  ADD KEY `post_date` (`post_created`),
  ADD KEY `post_guid` (`post_guid`),
  ADD KEY `post_status` (`post_status`),
  ADD KEY `post_folder_id` (`post_folder_id`),
  ADD KEY `post_image_id` (`post_image_id`),
  ADD KEY `posts_views` (`post_views`),
  ADD KEY `post_nav` (`post_nav`);

--
-- Index pour la table `fypress_post_meta`
--
ALTER TABLE `fypress_post_meta`
  ADD PRIMARY KEY (`post_meta_id_post`,`post_meta_key`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Index pour la table `fypress_user`
--
ALTER TABLE `fypress_user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_login` (`user_login`),
  ADD KEY `user_email_2` (`user_email`),
  ADD KEY `user_login_2` (`user_login`);

--
-- Index pour la table `fypress_user_meta`
--
ALTER TABLE `fypress_user_meta`
  ADD PRIMARY KEY (`user_meta_id_user`,`user_meta_key`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `fypress_folder`
--
ALTER TABLE `fypress_folder`
  MODIFY `folder_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `fypress_media`
--
ALTER TABLE `fypress_media`
  MODIFY `media_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `fypress_option`
--
ALTER TABLE `fypress_option`
  MODIFY `option_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `fypress_post`
--
ALTER TABLE `fypress_post`
  MODIFY `post_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `fypress_post_meta`
--
ALTER TABLE `fypress_post_meta`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `fypress_user`
--
ALTER TABLE `fypress_user`
  MODIFY `user_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `fypress_user_meta`
--
ALTER TABLE `fypress_user_meta`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;