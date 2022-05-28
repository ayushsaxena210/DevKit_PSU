<?php

try{
  //establishing connection
  $db = new PDO('sqite:user_PDO.sqlite');

  //creating table
  $db->exec("CREATE TABLE user(id INTEGER PRIMARY KEY, username VARCHAR, password VARCHAR, loggedin DATETIME)");
  
  $id=$username=$password=$loggedin="";

  //inserting into table
  $db->exec("INSERT INTO user(id,username,password,loggedin) VALUES($id, $username, $password, $loggedin)");
  
  //printing the database table
  print"<table border=1>";

  print"<tr><td>ID</td><td>Username</td><td>password</td><td>loggedin</td></tr>";
  
  $result=$db->query('SELECT * FROM user');

  foreach($result as $row){
    print "<tr><td>".$row['id']."</td>";
    print "<tr><td>".$row['username']."</td>";
    print "<tr><td>".$row['password']."</td>";
    print "<tr><td>".$row['loggedin']."</td>";
  }

print "</table>";

}
catch(PDOException $e){
  echo $e->getMessage();
}

?>