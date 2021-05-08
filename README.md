
#### ~~大佬勿喷~~

# 原理

大概就是让hpp将文件提交到这个仓库，然后在推送到语雀上

然后再用语雀的webhook更新actions然后生成部署（好麻烦啊）

# 使用

fork，修改`_config.yml`中的配置，在secrets中添加YUQUE_TOKEN

然后将hpp的doc_repo改为本仓库即可

在yuque的webhook中加入按照[#1](https://github.com/lbr77/hpp-yuque/issues/1)方法部署的workers链接（或用[这个vercelj脚本](https://github.com/lbr77/webhook_to_github_actions)）
