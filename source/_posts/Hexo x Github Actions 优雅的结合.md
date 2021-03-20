---
title: Hexo x Github Actions 优雅的结合
tag: c++
layout: posts
cover: 'https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209195357.jpeg'
categories:
  - 学习
  - Github Actions
abbrlink: 167d
date: 2021-02-09 15:41:21
---
用过Hexo的同学应该都知道，Hexo的最大缺点就是--------麻烦。

重装系统之后，要重新`npm install hexo-cli -g`、然后重新`hexo deploy`...

事情太多了。。

怎么办呢？直到某一天，我在Github 上看到了这样一个东西:

![Github Actions](https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209154627.png)

Github Actions  github 推出的CI/CD 服务（Continuous Integration /Continuous Delivery(CD) ）

相当于免费给你提供一个服务器然后。。。为所欲为![](https://cdn.jsdelivr.net/npm/chenyfan-oss@1.1.8/5896e9710dfd5.jpg)

<!-- more -->
### 1.上传源代码
(本文将博客目录一律改为`[blog-root]`)
用git 把你**博客**的源代码上传到一个新的仓库（最好是私有的）（不是`hexo d`!）

```bash
cd [blog-root]
git init 
git commit -m "Inital Commit" -a
git checkout -b main
git remote add origin <github_repo_url>
git push -u origin main
```
### 2. 获得token

### 3.新建actions
点击

![](https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209155303.png)

就可以直接新建一个Actions

![](https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209155710.png)

进入这个页面以后

![](https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209155735.png)

复制我的脚本

```yaml
name: Hexo Deploy

on:
  push:
    paths-ignore:
      - 'scaffolds/**'
      - 'source/_drafts/**'
      
jobs:
  build:
    runs-on: ubuntu-18.04
    if: github.event.repository.owner.id == github.event.sender.id

    steps:
      - name: 检查分支
        uses: actions/checkout@v2
        with:
          ref: main

      - name: 安装Node.js
        uses: actions/setup-node@v1
        with:
          node-version: '12.x'
      - name: 改变时区
        run: |
          cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
          echo "Now Date: "
          date -R
      - name: 安装Hexo
        run: |
          git config --global user.email "liborui0609@foxmail.com"
          git config --global user.name "lbr77"
          npm install hexo-cli -g
      - name: 缓存Hexo
        uses: actions/cache@v1
        id: cache
        with:
          path: node_modules
          key: ${{runner.OS}}-${{hashFiles('**/package-lock.json')}}
      - name: 安装依赖
        if: steps.cache.outputs.cache-hit != 'true'
        run: |
          npm i gulp-cli -g
          npm i --save
      - name: 生成静态文件并压缩
        run: |
          hexo clean
          hexo bangumi -u
          hexo generate
      - name: 从Github下载配置
        run: |
          git clone https://github.com/lbr77/lbr77.github.io.git ./.tmp/
          cp -r ./.tmp/.git/ ./public/.git/
          rm -rf  ./.tmp/
      - name: 部署到Github Pages
        run: |
          cd ./public
          git add *
          ls
          git commit -m "Update by Github Actions"
          git remote set-url origin https://[username]:[gh-token]@github.com/lbr77/lbr77.github.io
          git push -u origin main
      
```
粘贴后保存

### 3.配置SSH

然后（打开本地）的~/.ssh/id_rsa文件，复制并在你的repo中创建一个Secret Key

![](https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209160221.png)

名为HEXO_DEPLOY_KEY

并且新建一个repo，用来存储你的博客网址-----然后在新的repo中新建deploy_key,复制~/.ssh/id_rsa.pub文件

![](https://cdn.jsdelivr.net/gh/lbr77/picbed@main/img/20210209161553.png)


然后修改一个文件试试！！


每次你就可以直接将源代码推送到Github，然后等待他自行渲染，自动上传啦！！！

### 后记

参考资料：[GitHub Actions 来自动部署 Hexo](https://zhuanlan.zhihu.com/p/170563000)

下一篇，我们可以使用[Hexo Plus Plus](https://github.com/HexoPlusPlus/HexoPlusPlus)来使用全网页的Hexo博客！！（再也不需要每次安装Nodejs啦！！）
