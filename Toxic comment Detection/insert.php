<?php
$name=$_REQUEST["name"];
$email=$_REQUEST["email"];
$message=$_REQUEST["message"];
$id=0;
$conn=mysqli_connect("localhost","root","","toxic_comment");
if($conn)
{
	$q="insert into comments values('$id','$name','$email','$message')";
	$r=mysqli_query($conn,$q);
	if($r)
	{
		header("location:demo.php");
	}
	else
	{
		echo "<script>alert('Email id already in use')</script>";
	}
}

?>