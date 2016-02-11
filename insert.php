<body>

<?php
    $dsn ='mysql:dbname=peco_table;host=localhost';
$user='root';
$password='';
$dbh=new PDO($dsn,$user,$password);
$dbh->query('SET NAMES utf8');
    
    $name=$_POST['name'];
    $address=$_POST['address'];

    print 'タイトル';;
    print $name;
    print "詳細";
    print $address;

        
    $sql='INSERT INTO test-table(name,address)VALUES("'.$name.'","'.$address.'")';
$stmt=$dbh->prepare($sql);
$stmt->execute();

$dbh=null;    
        
?>

</body>