# Docker Sync

## 仓库概述

同步 DockerHub 镜像到阿里云私有仓库。

> 基于 `GitHub Actions` 每日自动同步

### 官方仓库同步

- nginx
  - `latest` `alpine` `1.25` `1.25-alpine`
  - `stable` `stable-alpine` `1.24` `1.24-alpine`

- mysql
  - `latest`
  - `8` `8.0` `8.0.33`
  - `5` `5.7` `5.7.42`

- redis
  - `latest`
  - `7` `7.0`
  - `6` `6.0` `6.2`
  - `5` `5.0`

- php
  - `8.2-cli` `8.2-cli-alpine` `8.2-fpm` `8.2-fpm-alpine`
  - `8.1-cli` `8.1-cli-alpine` `8.1-fpm` `8.1-fpm-alpine`
  - `8.0-cli` `8.0-cli-alpine` `8.0-fpm` `8.0-fpm-alpine`
  - `7.4-cli` `7.4-cli-alpine` `7.4-fpm` `7.4-fpm-alpine`
  - `7.3-cli` `7.3-cli-alpine` `7.3-fpm` `7.3-fpm-alpine`
  - `7.2-cli` `7.2-cli-alpine` `7.2-fpm` `7.2-fpm-alpine`
  - `7.1-cli` `7.1-cli-alpine` `7.1-fpm` `7.1-fpm-alpine`
  - `7.0-cli` `7.0-cli-alpine` `7.0-fpm` `7.0-fpm-alpine` (停止同步，已同步的镜像仍可使用)

- vaultwarden/server
  - `latest`
  - `1.29.0`

### suyar 仓库同步

- suyar/php
  - `8.2-cli` `8.2-cli-alpine` `8.2-fpm` `8.2-fpm-alpine`
  - `8.2-cli-supervisor` `8.2-cli-alpine-supervisor` `8.2-cli-cron` `8.2-cli-alpine-cron`
  - `8.2-integration` `8.2-alpine-integration`
  - `8.1-cli` `8.1-cli-alpine` `8.1-fpm` `8.1-fpm-alpine`
  - `8.1-cli-supervisor` `8.1-cli-alpine-supervisor` `8.1-cli-cron` `8.1-cli-alpine-cron`
  - `8.1-integration` `8.1-alpine-integration`
  - `8.0-cli` `8.0-cli-alpine` `8.0-fpm` `8.0-fpm-alpine`
  - `8.0-cli-supervisor` `8.0-cli-alpine-supervisor` `8.0-cli-cron` `8.0-cli-alpine-cron`
  - `8.0-integration` `8.0-alpine-integration`
  - `7.4-cli` `7.4-cli-alpine` `7.4-fpm` `7.4-fpm-alpine`
  - `7.4-cli-supervisor` `7.4-cli-alpine-supervisor` `7.4-cli-cron` `7.4-cli-alpine-cron`
  - `7.4-integration` `7.4-alpine-integration`
  - `7.3-cli` `7.3-cli-alpine` `7.3-fpm` `7.3-fpm-alpine`
  - `7.3-cli-supervisor` `7.3-cli-alpine-supervisor` `7.3-cli-cron` `7.3-cli-alpine-cron`
  - `7.3-integration` `7.3-alpine-integration`
  - `7.2-cli` `7.2-cli-alpine` `7.2-fpm` `7.2-fpm-alpine`
  - `7.2-cli-supervisor` `7.2-cli-alpine-supervisor` `7.2-cli-cron` `7.2-cli-alpine-cron`
  - `7.2-integration` `7.2-alpine-integration`
  - `7.1-cli` `7.1-cli-alpine` `7.1-fpm` `7.1-fpm-alpine`
  - `7.1-cli-supervisor` `7.1-cli-alpine-supervisor` `7.1-cli-cron` `7.1-cli-alpine-cron`
  - `7.1-integration` `7.1-alpine-integration`
  - `7.0-cli` `7.0-cli-alpine` `7.0-fpm` `7.0-fpm-alpine`
  - `7.0-cli-supervisor` `7.0-cli-alpine-supervisor` `7.0-cli-cron` `7.0-cli-alpine-cron`
  - `7.0-integration` `7.0-alpine-integration`
