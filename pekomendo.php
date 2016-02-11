<!DOCTYPE html>
<html>
<head>
    <title>ペコメンド</title>
    <meta charset="utf-8">
    <meta name="description" content=""/>
    <meta name="keywords" content=""/>
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
</head>

<body>
    <div class="wapper">
        <header id="header">
            <div class="inner clearfix">
            </div>
        </header>
        <div class="inner">
            <nav class="global_Nav">
                <ul>
                    <li class="nav_item">HOME<br/>-ホーム-</li>
                    <li class="nav_item">NEWS<br/>-更新情報-</li>
                    <li class="nav_item">FOOD<br/>-お店情報-</li>
                    <li class="nav_item none">ABOUT US<br/>-運営者-</li>
                    <a href="form.php"><li class="nav_item last">お店を登録</li>
                    </a>                
                </ul>
            </nav>
        </div>
        <!--メインビジュアル-->
        <section id="main_visual">
            <div class="inner">
                <div class="main">
                    <img src="image/top.jpeg" alt="サンプル" width="960" height="auto">
                    </div>
            </div>
        </section>
        <?php
        include("menu.php")    
        ?>
        
    </div>
</body>
</html>



