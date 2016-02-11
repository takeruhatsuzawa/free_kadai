<!DOCTYPE html>
<html>
<head>
    <title>ペコメンド</title>
    <meta charset="utf-8">
    <meta name="description" content=""/>
    <meta name="keywords" content=""/>
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
    <script type="text/javascript"
src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">
</script>
</head>

<body>
    <div class="wapper">
        <header id="header">
            <div class="inner clearfix">
                <h1>
                </h1>
            </div>
        </header>
        <div class="inner">
            <nav class="global_Nav">
                <ul>
                    <li class="nav_item">HOME<br/>-ホーム-</li>
                    <li class="nav_item">NEWS<br/>-更新情報-</li>
                    <li class="nav_item">FOOD<br/>-お店情報-</li>
                    <li class="nav_item none">ABOUT US<br/>-運営者-</li>
                    <li class="nav_item last">お店を登録</li>
                </ul>
            </nav>
        </div>
        <!--メインビジュアル-->
        <section id="main_visual">
            <div class="">
                <div class="contents-box">
                    <div class="form-heading">
                        <div>
                            <h2 class="section-title">FORM</h2>
                            <p>お店登録</p>     
                        </div>
                    </div>
                </div>
                
            </div>
        </section>
        <section>
            <html>
<head>
<meta charset="utf-8">
<title></title>
</head>
<body>
    
<form action="insert.php" method="post">
    
    <table class="form-table inner">
        <tr class="form-table-tr">
            <th>店舗名</th>
            <td><input type="text" name="name" value="" style="width:300px; padding:7px; font-size:16px;"></td>
        </tr>
        <tr class="form-table-tr">
            <th>住所</th>
            <td><input type="text" name="address" value="" style="width:300px; padding:7px;font-size:16px;"></td>
        </tr>
        <tr class="form-table-tr">
            <th>メニュー名</th>
            <td><input type="text" name="menu" value="" style="width:300px; padding:7px; font-size:16px;"></td>
        </tr>
        <tr class="form-table-tr">
            <th>アレルギー</th>
            <td><input type="checkbox" name="allergy[]" value="mugi">麦 
                <input type="checkbox" name="allergy[]" value="egg">たまご 
                <input type="checkbox" name="allergy[]" value="crab">かに 
                <input type="checkbox" name="allergy[]" value="shrimp">えび 
                <input type="checkbox" name="allergy[]" value="peanuts">ピーナッツ 
                <input type="checkbox" name="allergy" value="soba">そば 
            </td>
        </tr>
        <tr>
            <th>写真</th>
            <td><input type="file" name="pic"></td>
        </tr>
    </table>

    
    <div class="btn inner">
        <input id="submit_button" type="submit" value="送信" onClick="location.href='input_finish.php'">

    </div>
    
    
    
</form>

</body>
</html>
            
        </section>
        
        
    </div>
    
</body>
</html>
