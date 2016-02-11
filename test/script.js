jQuery(function($){
	//送信ボタンの非表示
	$('#submit').hide();
	
	
	//フォームの内容が変更されたとき
	$('#img').change(function() {
	    var preview = $('#preview');
		
	    //現在表示されているものを消す。
	    preview.find("img").fadeOut(300);
 
	    //アップロード
	    $(this).upload(
			'upload.php',
			$("form").serialize(),
			function(html){
			//サムネイルの表示
	        	preview.html(html).animate({"height":preview.find("img").height()+"px"},300,function(){
	            	preview.find("img").hide().fadeIn(300);
	        	});
	    	},'html');
	});

	//離れるときに画像を削除
	$(window).bind("beforeunload",function(){
		var unlinkFile = $("#postPhotoName").val();
		$.ajax({
			async: false,
			cache: false,
			type:	"POST",
			url:	"upload.php",
			data:	"postPhotoName="+unlinkFile

		});

	});

});