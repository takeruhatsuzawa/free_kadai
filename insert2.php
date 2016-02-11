<body>

<?php
    $dsn ='mysql:dbname=peco_table;host=localhost';
$user='root';
$password='';
$dbh=new PDO($dsn,$user,$password);
$dbh->query('SET NAMES utf8');
    
    $title=$_POST['title'];
    $detail=$_POST['detail'];

    print 'タイトル';;
    print $title;
    print "詳細";
    print $detail;

        
    $sql='INSERT INTO peco_an_table(title,detail)VALUES("'.$title.'","'.$detail.'")';
$stmt=$dbh->prepare($sql);
$stmt->execute();

$dbh=null;    
        
?>

</body>