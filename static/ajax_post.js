 $(function(){
        $('#jsStayBtn').on('click', function(){
            var title = $("#example-text-input").val();
            var options = $("select[name='options']").val();
            var content = editor.txt.html();
            var url = window.location.href;  // 取得当前完整域名
            var csrftoken = Cookies.get('csrftoken');  // 从Cookie中取到csrftoken

            $.ajax({
                cache: false,
                type: "POST",
                url: url,
                data: {'title': title, 'options': options, 'content': content},
                dateType: "json",
                async: true,
                beforeSend:function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
                success: function(data) {
                    if(data.status == 'success'){
                        alert("保存成功");
                         // window.location.reload();//刷新当前页面.
                    }else if(data.status == 'fail'){
                        // $('#jsCompanyTips').html(data.msg);
                        alert("保存失败");
                    }
                },
            });
        });
    });

// 提交评论
 $(function(){
     $('#comment_submit').on('click', function(){
         var comment = $("#comment").val();
         var url = window.location.href;  // 取得当前完整域名
         var csrftoken = Cookies.get('csrftoken');  // 从Cookie中取到csrftoken
         var article_id =  url.split("/");

         $.ajax({
             cache: false,
             type: "POST",
             // url: url + 'comment',
             url: 'http://127.0.0.1:8000/article/comment/submit/' + article_id[5] + '/',  // url: '127.0.0.1:8000/article/comment/submit/article_id'
             data: {'comment': comment},
             dateType: "json",
             async: true,
             beforeSend:function(xhr, settings){
                 xhr.setRequestHeader("X-CSRFToken", csrftoken);
             },
             success: function(data) {
                 if(data.status == '0'){
                     alert("保存成功");
                     window.location.reload();//刷新当前页面.
                 }else if(data.status == '1'){
                     // $('#jsCompanyTips').html(data.msg);
                     alert("保存失败");
                 }
             },
         });
     });
 });

// 删除评论
$(function (){
    $('#comment_delete').on('click', function() {
        var comment_id = this.value;
        var csrftoken = Cookies.get('csrftoken');
        // var url = window.location.href;
        // var article_id =  url.split("/")[5];

        $.ajax({
            cache: false,
            type: 'POST',
            url: 'http://127.0.0.1:8000/article/comment/delete/',
            // url: url,
            data: {'comment_id': comment_id, /*'article_id': article_id*/},
            dataType: "json",
            async: true,
            beforeSend: function (xhr, setting) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                if (data.status == 0){
                    // alter('提交成功');
                    window.location.reload();//刷新当前页面.
                }
                else if (data.status == 1){
                    alter('删除失败');
                }
            },
        });
    });
});


