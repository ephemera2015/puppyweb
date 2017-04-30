function imagePreview(file,pic)
{
    var file = file.files[0];  
    var reader = new FileReader();  
    reader.readAsDataURL(file);  
    reader.onload = function(e)
    {  
        pic.src=this.result;
    }  
};
function preview(file) 
{
    div=document.getElementById('add-entry-img-preview');
    $(file).clone(true).insertAfter(file).hide().attr({name:$('#img_cnt').val()});
    $('#img_cnt').val( (parseInt( $('#img_cnt').val() )+1).toString() );
    if (file.files && file.files[0])
    {
        var reader = new FileReader();
        reader.onload = function(evt) 
        {
            div.innerHTML += '<img src="' + evt.target.result + '" width="100px" height="100px"/>';
        }
        reader.readAsDataURL(file.files[0]);
    } 
}
function showPreview(obj)
{  
    var pic = document.getElementById("avatar_preview");  
    var file = document.getElementById("avatar");  
    imagePreview(file,pic);  
};
  
$(document).ready( function ()
{   
    $('.entry_button').each(function (){
        $(this).html($(this).html()+'('+$(this).parent().children('input').length+')');
    });
    $('.entry').each( function (){
        var r=Math.floor(Math.random()*255)+1;
        var g=Math.floor(Math.random()*255)+1;
        var b=Math.floor(Math.random()*255)+1;
        $(this).css("background-color","rgba("+r.toString()+","+g.toString()+","+b.toString()+",0.6)");
    });
    $('#center_close').click(function(){
        $('.login_enroll').css("display","none");
        $('.add-entry').css("display","none");
        $('#entry_imgs').css("display","none");
        $('#center').hide();
    });
    $('#entry_imgs_next').click(function(){
        var x=$('#entry_imgs').children('p:visible');
        if(x.next('p').length==1)
        {
            x.css("display","none");
            x.next().css("display","block");
        }
       
    });
    $('#entry_imgs_previous').click(function(){
        var x=$('#entry_imgs').children('p:visible');
        if(x.prev('p').length==1)
        {
            x.css("display","none");
            x.prev().css("display","block");
        }
       
    });
    $('.entry_button').click(function(){
    
        $('#center').fadeIn(1000);
        $('#entry_imgs').fadeIn(1000);
        $('#entry_imgs').children('p').remove();
        $(this).parent().children('input').each( function() {
        $('#entry_imgs').append($('<p style="text-align:center;display:none"><img height=300px src="/get/image/'+$(this).val()+'"></p>'));
        });
        $('#entry_imgs').children('p:first').css("display","block");
    });
    $('.enroll').css("display","none");
    $('#login').click(function()
    {
        $('#center').show();
        $('.enroll').hide();
        $('.login').show();
    });
    $('#enroll').click(function()
    {
        $('.enroll').show();
        $('.login').hide();
    });
    $('#microblog').click(function()
    {
        $('#center').fadeIn(1000);
        $('.add-entry').fadeIn(1000);
    });
    $('#add-entry-ok').click(function()
    {
        var form=new FormData(document.getElementById("add-entry-form"));
        $.ajax(
        {
            type:"POST",
            url:"/post/entry",
            async:true,
            data:form,
            cache:false,
            processData:false,
            contentType:false,
            success:function(data,textStatus,jqXHR)
            {
                if(data.status)
                {
                    $('.add-entry').css("display","none");
                    $('#center').hide();
                }
            }
        });
    });
    $('#login_btn').click(function()
    {
        if($('#login_btn').html()=='登录')
        {
            $('#center').fadeIn(1000);
            $('.login_enroll').fadeIn(1000);
        }
        else
        {
            $.ajax(
            {
                type:"POST",
                url:"/post/logout",
                async:true,
                data:{},
                timeout:5000,
                dataType:'json',
                success:function(data,textStatus,jqXHR)
                {
                    if(data.status)
                    {
                        $('#login_btn').html("登录");
                    }
                }
            });
        }
    });
    $('#login_ok').click(function()
    {
        $.ajax(
            {
                type:"POST",
                url:"/post/login",
                async:true,
                data:
                {
                    name:$('#login_name').val(),
                    pwd:$('#login_pwd').val()
                },
                timeout:5000,
                dataType:'json',
                success:function(data,textStatus,jqXHR)
                {
                    if(data.status)
                    {   
                        $('#center').hide();
                        $('.login_enroll').hide();
                        $('#login_btn').html("注销");
                    }
                    else
                    {
                        $('#login_enroll_msg').html("用户名或密码错误");
                    }
                }
            });
    });
    $('#enroll_ok').click(function()
    {
        var form=new FormData(document.getElementById("enroll_form"));
        $.ajax(
        {
            type:"POST",
            url:"/post/enroll",
            async:true,
            data:form,
            cache:false,
            processData:false,
            contentType:false,
            success:function(data,textStatus,jqXHR)
            {
                if(data.status)
                {
                    $('.enroll').hide();
                    $('.login').show();
                    $('#login_enroll_msg').html('注册成功，请登录');
                }
                else
                {
                    $('#login_enroll_msg').html("该用户名已被注册");
                }
            }
        });
    });
});


