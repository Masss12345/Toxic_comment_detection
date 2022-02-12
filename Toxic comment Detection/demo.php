<?php
	$command = escapeshellcmd('flask.py');
		$output = shell_exec($command);
		echo $output;
		echo "here";
		?>
		<html>
		<head>
		</head>
		<body>
		<h1> here</h1>
		</body>
		</html>