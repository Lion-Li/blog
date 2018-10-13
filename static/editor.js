var E = window.wangEditor;
var editor = new E('#div1', '#div2');  // 两个参数也可以传入 elem 对象，class 选择器
var csrftoken = Cookies.get('csrftoken');  // 从Cookie中取到csrftoken

// var $text1 = $('#text1');
// editor.customConfig.onchange = function (html) {
//     // 监控变化，同步更新到 textarea
//     $text1.val(html)
// };

// 配置服务器端地址
//使用相对路经导致发布后的文章再编辑图片上传路经不正确，这里改成绝对路径。
editor.customConfig.uploadImgServer = 'http://127.0.0.1:8000/article/editor/image';

// 设定图片传输的key值
editor.customConfig.uploadFileName = 'Image';

// 调试模式
editor.customConfig.debug = false;

// 头部添加csrftoken
editor.customConfig.uploadImgHeaders = {
    'X-CSRFToken': csrftoken,
};

// 配置工具栏
editor.customConfig.menus = [
     'head',  // 标题
    'bold',  // 粗体
    'fontSize',  // 字号
    'fontName',  // 字体
    'italic',  // 斜体
    'underline',  // 下划线
    'strikeThrough',  // 删除线
    'foreColor',  // 文字颜色
    'backColor',  // 背景颜色
    'link',  // 插入链接
    'list',  // 列表
    'justify',  // 对齐方式
    'quote',  // 引用
    'image',  // 插入图片
    'table',  // 表格
    'code',  // 插入代码
    'undo',  // 撤销
    'redo'  // 重复
];

editor.create();

// 初始化 textarea 的值
// $text1.val(editor.txt.html());
