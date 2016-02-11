
<section id="news" class="contents-box">
    <div class="contents-heading">
        <h2 class="section-title">NEWS</h2>
        <p>お知らせ・更新情報</p>
    </div>
        <div class="inner">
            <dl class="news-list clearfix">
                
    <?php
    $dsn='mysql:dbname=peco_table;host=localhost';
    $user='root';
    $password='';
    $dbh= new PDO($dsn, $user, $password);
    $dbh->query('SET NAMES utf8');
    
    $sql='SELECT*FROM peco_an_table WHERE1';
    $stmt = $dbh->prepare($sql);
    $stmt->execute();
    
    for($i = 0; $i < 3; $i++)
    {
        $rec=$stmt->fetch(PDO::FETCH_ASSOC);
        if($rec==false)
        {
            break;
        }
            print $rec['id'];
        print '<a href="http://google.co.jp">'.$rec['title'].'</a>';
        print $rec['detail'];
        print '<br />';
        
    }  
        
        
    $dbh=null;
    ?>
                
            </dl>
        </div>
    
    
    
</section>
        