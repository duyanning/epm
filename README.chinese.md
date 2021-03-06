献给那些还挣扎在Makefile泥潭中痛不欲生的C++程序员。

epm: (E)asy (P)roject (M)anager

在linux下编写C++程序，除了自己的C++代码外，你还需要准备一个（或者一大堆）Makefile文件，这个（些）Makefile文件就构成了所谓的build system，用来build你的project。

但是，用不了多久你便会发现，这个build system似乎比你自己的project还要大，而且更难于维护。

原因是什么呢？

Makefile中不外乎两类东西：*依赖关系*和*动作*

前者用make自己的语言表达，后者用shell脚本语言表达。

如果把Makefile看作一个程序、一段代码，那么（理想中）这段代码的逻辑应“全部”由依赖关系所决定，依赖关系就好比是“骨”，而执行的动作仅仅是“肉”。

但是，很快你就会发现程序的逻辑并不仅限于这些依赖关系，这个时侯Makefile就遇到麻烦了: 

* make自己的语言就是被设计用来表达依赖关系的，超出这个范围，他无能为力。为了表达这些依赖关系之外的逻辑，你只有求助于make那些头痛医头、脚痛医脚的扩充功能，不但不系统而且很难用。

* 而shell脚本语言，虽然比make自己的语言更通用，但其设计目的（方便交互使用）就已经决定了它无法跟其他以方便程序设计为目的的编程语言相比，而且，它对于make来说，是一种外来的异物，所以跟make自己的语言之间总是存在配合问题。

总而言之，make+shell脚本的方案在表达复杂逻辑时捉襟见肘，而这种能力却正是大型的build system所必须的。

最后的结果就是，make处在一种高不成、低不就的尴尬境地。这也是大量make替代品层出不穷的原因。

epm的解决之道：

* 用python脚本代替shell脚本来编写build system，python语言结构丰富、表达力强大，足以满足各种需求。
* 而对于内建在make语言中的依赖关系指定和更新动作按需执行等功能，则通过一个组等价的类来实现。

有了这组类和强大的python语言，再复杂的build system也能轻松搞定。

不过话说回来，对于日常的绝大多数使用，并不需要一个高度定制的build system，有过visual c++编程经验的朋友想必对于visual c++那简单易用的工程管理很是怀念。而这正是epm所要带给大家的。epm本身用python编写，利用前面说过的那些类，呈现给大家一个简单易用的工程管理工具。

相比高不成、低不就的make，epm的目标是上的去、下的来。

注意：本文仅说明epm作为一个命令行工具如何使用（epm之“下的来”），并不探讨如何在利用epm提供的类和python来编写自己的build system（epm之“上的去”）。

# 获取epm

svn co https://epm.svn.sourceforge.net/svnroot/epm/trunk epm 目前只能通过svn方式获取，epm不过一个python脚本而已，获取之后就立即能用。

使用之前你需要把epm所在的目录添加到PATH中。 在~/.profile的最后添加下面这行就行了： PATH="~/epm:$PATH" （假设你把epm放在了~/epm下） 

# 常用命令

epm new hello

或者更完整一点

epm new hello -t exe （在没有明确指出projec类型的情况下，默认就是-t exe）

    创建一个名为hello.epmprj的project。build之后会得到一个名为hello的exe文件。 

epm new foo -t dll

    创建一个名为foo.epmprj的project。build之后得到一个名为foo.so的动态链接库。 

epm new bar -t lib

    创建一个名为bar.epmprj的project。build之后得到一个名为bar.a的静态库。 

epm add *.cpp

    把目录下所有的cpp文件添加到project中。 

epm add '*.cpp' （强烈推荐这种用法！而非上一种）

    把目录下所有的cpp文件添加到project中。注意*.cpp是被单引号括住的（这防止了shell对*.cpp进行扩展），这样，即使将来再有新的cpp文件，也不用再手动add了。 

epm remove main.cpp

    从project中删除main.cpp。 

epm build 或 epm b

    build就是build。 

epm compile hello.cpp 或 epm c hello.cpp

    只编译hello.cpp 

# 不常用命令

epm addconfig release

    添加一个名为release的configuration。 

epm setactiveconfig release

    把release设置成当前configuration，缺省的是debug。 

epm gui

    打开epm的主窗口。目前只是一个空窗口，打算是有些配置应该能通过GUI方式修改。 

# 使用举例
## 例子1：建立project

mkdir hello #建立一个目录

cd hello

epm new hello #新建一个名为hello的工程

然后准备你的cpp文件，无论什么名字，无论多少

epm add '*.cpp' #把所有cpp文件加到工程中

epm build #编译

以后只要运行epm build就行了。

如果只编译工程中的某个文件，比如hello.cpp

则输入epm compile hello.cpp。
## 例子2：使用某个库

如果你的程序要链接某个库

编辑一个名为generallink-any.options的文本文件，在其中写你要链接的库的名字。

可以直接写库的名字，也可以写-lfoo这种形式，总而言之，链接时这些东西将会出现在命令行上。
## 例子3：使用gtkmm或fltk

如果你的程序要使用gtkmm或fltk

编辑一个名为generalcxx-any.options的文本文件，其中写

`pkg-config gtkmm-2.4 --cflags` 或 `fltk-config --cxxflags`

再编辑一个名为generallink-any.options 的文本文件，其中写

`pkg-config gtkmm-2.4 --libs` 或 `fltk-config --ldflags`


前一个文件是gtkmm/fltk所需的编译选项，后一个是gtkmm/fltk所需的链接选项。

注意：在options文件中可以使用环境变量，跟在shell下一样。
## 例子4：包含多个project的solution

如果你有多个相关的project。

那就建立一个solution把这些project都管理起来。

epm newsln hello # 新建一个名为hello的solution

epm addprj foo/foo.epmprj # 把foo.epmprj添加进solution

epm addprj bar/bar.epmprj # 把bar.epmprj添加进solution

epm buildsln # build solution，会导致foo和bar两个project都被build

如果foo和bar之间有依赖关系，你可以编辑PROJECTFILES文件，调整里面的次序。
## 例子5：预编译头文件

使用预编译头文件

用编辑器打开文件PRECOMPILEDHEADERS，把你想要预编译的头文件的名字，如std.h，写在里面，保存就行了。

如果你有多个预编译头文件，而他们之间有相互依赖关系，你可以在该文件中调整其次序。
## 例子6：支持C++11与gdb调试

编辑文件generalcxx-debug.options，写如下内容保存

-std\=c++0x

-ggdb 

# 重要文件

<project name>.epmprj

    这是epm的project文件 

SOURCEFILES

    源文件列表 

PRECOMPILEDHEADS

    需要被预编译的头文件列表 

# 参数文件

一个project，不光包括.cpp和.h这些源文件。还包括了与这些文件紧密相关的参数文件。 通过参数文件，你可以进一步控制编译和链接的过程。因为这些文件的内容会被添加到传递给编译器或者链接器的命令行参数之后。

epm参数文件的命名遵循以下方案：

<文件名><工具名>-<配置名>.options

其中：

<文件名>既可以是特定的源文件名，比如main.cpp，也可以是表示对所有源文件都适用的general。

<配置名>既可以是特定的配置名，比如debug或release，也可以是表示对所有配置都适用的any。

<工具名>表示build过程中用到的相关工具，cxx表示C++编译器，c表示C编译器，link表示链接器。

比如 main.cppcxx-debug.options

    该文件指定在debug配置下编译main.cpp所用的命令行选项。 
    其中main.cpp是文件名，cxx是工具名，代表c++编译器，debug是配置名。 

epm在build的过程中，按照从“特定”到“通用”再到“默认”的顺序来查找相关的参数文件。 即：有“特定”的就不用“通用”的，有“通用”的就不用“默认”的。

比如，如果存在两个参数文件main.cppcxx-debug.options和generalcxx-debug.options， 那么当epm编译main.cpp这个文件时，它会使用main.cppcxx-debug.options，而不是generalcxx-debug.options。 假如对于foo.cpp，不存在foo.cppcxx-debug.options，那么就会使用generalcxx-debug.options。 如果既没有“特定”的配置文件，也不存在“通用”的配置文件，那么epm就会使用自带的“默认”的配置文件。这些默认的配置文件都在epm自己的目录下，你不要更改。


# Emacs支持

可以在emacs中使用epm。epm提供了一个名为epmacs.el的emacs插件，给emacs装上就行了。同时还提供了一个.emacs的样例

f7

    编译工程，执行epm build，相当于在VC中按F7 

f5

    调试运行，相当于VC中按F5 

C-f7

    只编译当前文件，相当于VC中按Ctrl+F7 

M-x epm-set-gdb-args

    设置被调试程序的命令行参数 

M-x epm-set-gdb-dir

设置被调试程序的当前目录


# 遇到问题

因为还在不断开发之中，很有可能原来的project现在没法打开了。

如果出现这种情况，把以前的文件删除了，重新建立project就行了。

或者，你干脆就用某个特定版本的epm，不要更新。

或者，访问讨论组

http://groups.google.com/group/easy-project-manager


# 需要安装的第三方软件

python，因为epm就是用python编写的。

g++，epm假设你使用的是g++

如果你还打算使用epm的emacs插件epmacs.el，你需要先安装pymacs这个东西，因为epmacs.el用到它。 
