#!/bin/bash
# 设置安装目录
install_dir="$PWD/tooldelta"
# 设置应用程序名称
app_name="ToolDelta"
# 设置快捷指令
shortcut_command="td"
# 设置 GitHub release URL
github_release_url="https://mirror.ghproxy.com/https://github.com/ToolDelta/ToolDelta/releases/download/0.3.8/ToolDelta-linux"

function EXIT_FAILURE(){
    exit -1
}



function download_exec(){
# 权限
mkdir -p "$install_dir"
chown -R $(whoami):$(whoami) "$install_dir"

# 切换到安装目录
pushd "$install_dir" || exit

# 下载
if curl -o "$app_name" -L "$github_release_url"; then
    echo "下载完成。"
else
    echo "下载失败。请检查网络连接或稍后再试。"
    exit 1
fi

# 权限
chmod +x "$app_name"
# 创建符号链接
if ln -s "$install_dir/start.sh" "/usr/local/bin/$shortcut_command"; then
    echo "快捷指令 '$shortcut_command' 创建成功。"
else
    echo "创建快捷指令 '$shortcut_command' 失败。请检查权限或手动创建快捷指令。"
fi

# 生成start.sh脚本
echo "pushd $install_dir && ./$app_name && popd " >  "$install_dir/start.sh"
chmod +x "$install_dir/start.sh"

popd
}

if [[ $(uname) == "Darwin" ]]; then
    PLANTFORM="Macos_x86_64"
elif [[ $(uname -o) == "GNU/Linux" ]] || [[ $(uname -o) == "GNU/Linux" ]]; then
    PLANTFORM="Linux_x86_64"
    if [[ $(uname -m) != "x86_64" ]]; then
        echo "不支持非64位的Linux系统"
        EXIT_FAILURE
    fi
elif [[ $(uname -o) == "Android" ]]; then
    PLANTFORM="Andorid_armv8"
    if [[ $(uname -m) == "armv7" ]]; then
        echo "不支持armv7的Andorid系统"
        EXIT_FAILURE
    fi
    echo "检测文件权限中..."
    if [ ! -x "/sdcard/Download" ]; then
        echo "请给予 termux 文件权限 ~"
        sleep 2
        termux-setup-storage
    fi
    if [ -x "/sdcard/Download" ]; then
        echo -e ""
        # green_line "太好了，omega将被保存到downloads文件夹下，你可以从任何文件管理器中找到它了"
        # working_dir="/sdcard/Download"
        # executable="/sdcard/Download/fastbuilder"
    else
        red_line "不行啊，没给权限"
        EXIT_FAILURE
    fi
else
    echo "不支持该系统，你的系统是"
    uname -a
fi




download_exec
echo "安装完成啦，您现在可以在命令行中输入 '$shortcut_command' 来启动 $app_name。"