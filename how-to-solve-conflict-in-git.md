# how to solve conflict in git

## 提交时的错误信息
error: Your local changes to the following files would be overwritten by merge:
        readme.md
Please, commit your changes or stash them before you can merge.

## 如果需要保留自己的修改，操作如下：

```bash
git stash
git pull
git stash pop
```

### 查看并修改差异
```bash
git diff -w +文件名 
```

## 如果要完全覆盖本地修改的文件. 方法如下:
```bash
git reset --hard
git pull
```
其中git reset是针对整个工程，

### 如果想针对文件回退本地修改,使用如下：
```bash
git checkout HEAD file/to/restore
```
