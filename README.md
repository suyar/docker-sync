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
  - `8` `8.2` `8.2.0` `8.2-oracle` `8.2.0-oracle`
  - `8.0` `8.0.35` `8.0-oracle` `8.0.35-oracle` `8.0-debian` `8.0.35-debian`
  - `5` `5.7` `5.7.44` `5-oracle` `5.7-oracle` `5.7.44-oracle`

- redis
  - `latest` `alpine`
  - `7` `7-alpine` `7.2` `7.2-alpine`
  - `7.0` `7.0-alpine` 
  - `6` `6-alpine` `6.2` `6.2-alpine`
  - `6.0` `6.0-alpine`
  - `5` `5-alpine` `5.0` `5.0-alpine`

- php
  - `8.3-cli` `8.3-cli-alpine` `8.3-fpm` `8.3-fpm-alpine`
  - `8.2-cli` `8.2-cli-alpine` `8.2-fpm` `8.2-fpm-alpine`
  - `8.1-cli` `8.1-cli-alpine` `8.1-fpm` `8.1-fpm-alpine`
  - `8.0-cli` `8.0-cli-alpine` `8.0-fpm` `8.0-fpm-alpine`
  - `7.4-cli` `7.4-cli-alpine` `7.4-fpm` `7.4-fpm-alpine`
  - `7.3-cli` `7.3-cli-alpine` `7.3-fpm` `7.3-fpm-alpine`
  - `7.2-cli` `7.2-cli-alpine` `7.2-fpm` `7.2-fpm-alpine`
  - `7.1-cli` `7.1-cli-alpine` `7.1-fpm` `7.1-fpm-alpine`
  - `7.0-cli` `7.0-cli-alpine` `7.0-fpm` `7.0-fpm-alpine` (停止同步，已同步的镜像仍可使用)

- vaultwarden/server
  - `latest` `alpine`
  - `1.29.0` `1.29.0-alpine`
  - `1.29.1` `1.29.1-alpine`
  - `1.29.2` `1.29.2-alpine`
  - `1.30.0` `1.30.0-alpine`
  - `1.30.1` `1.30.1-alpine`

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
