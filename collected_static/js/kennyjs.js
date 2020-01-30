// 安全删除文章
function confirm_safe_delete() {
    layer.open({
        title: "确认删除",
        content: "你确认删除这篇文章吗？",
        yes: function (index, layero) {
            $('form#safe_delete button').click();
            layer.close(index);
        },
    })
}

//富文本编辑器移除自带样式，以可适应窗口大小
$(".django-ckeditor-widget").removeAttr('style')

//sidebar，目录栏，使用的abouolia/sticky-sidebar
$('#sidebar').stickySidebar({
    topSpacing: 20,
    bottomSpacing: 20,
})

//唤醒二级回复的modal
function load_modal(article_id, comment_id) {
    let modal_body = '#modal_body_' + comment_id;
    let modal_id = '#comment_' + comment_id;
    if ($(modal_body).children().length === 0) {
        let content = '<iframe src="/comment/post-comment/' +
            article_id + '/'
            + comment_id + '"'
            + 'frameborder="0" style="width:100%;height:100%;id="iframe_'
            + comment_id + '"></iframe>';
        $(modal_body).append(content);
    }
    $(modal_id).modal('show');
}

//二级回复modal点击确定后，进行锚点定位
function post_reply_and_show_it(url, new_comment_id) {
    // let next_url = "{% url 'article:article_detail' "+ article_id+" %}";
    let next_url = url;
    //去除url最后的‘/’
    next_url = next_url.charAt(next_url.length - 1) === '/' ? next_url.slice(0, -1) : next_url;
    window.location.replace(next_url + "#comment_elem_" + new_comment_id);
}


// 点赞

// 点赞主函数
function validate_is_like(url, id, likes) {
    // {#   取出LocalStorage中的数据#}
    let storage = window.localStorage;
    const storage_str_data = storage.getItem('my_blog_data');
    let storage_json_data = JSON.parse(storage_str_data)
    // {#    若数据不存在，则创建空字典#}
    if (!storage_json_data) {
        storage_json_data = {}
    }
    ;
    // {#    检查当前文章是否已点赞，是则status=True#}
    const status = check_status(storage_json_data, id);
    if (status) {
        // {#点过赞则立即退出函数#}
        layer.msg('已经点过赞了呦~');
        // {#点过赞立即退出函数#}
        return;
    } else {
        // {#用JQuery找到点赞数量，并加1#}
        $('span#likes_number').text(likes + 1).css('color', '#dc3545')
    }
    // {#    用ajax向后端发送post请求#}
    $.post(
        url,
        //post只是为了做csrf校检，因此数据为空
        {},
        function (result) {
            if (result === 'success') {
                // {#尝试修改点赞数据#}
                try {
                    storage_json_data[id] = true;
                } catch (e) {
                    window.localStorage.clear();
                }
                // {#   将字典转换为字符串，以便存储到LocalStorage#}
                const d = JSON.stringify(storage_json_data)
                try {
                    storage.setItem('my_blog_data', d);
                } catch (e) {
                    // {#    code 22错误表示LocalStorage已经满了#}
                    if (e.code === 22) {
                        window.localStorage.clear();
                        storage.setItem('my_blog_data', d);
                    }
                }
            } else {
                layer.msg('与服务器通信失败..过一会再试试呗~')
            }
        }
    );
}

//检查状态，检查某个文章是否已点赞
function check_status(data, id) {
    try {
        if (id in data && data[id]) {
            return true;
        } else {
            return false;
        }
    } catch (e) {
        window.localStorage.clear();
        return false;
    }
}


//回到顶部
$(function () {
    $('#BackTop').click(function () {
        $('html,body').animate({scrollTop: 0}, 500);
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('#BackTop').fadeIn(300);
        } else {
            $('#BackTop').stop().fadeOut(300);
        }
    }).scroll();
});


