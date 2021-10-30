<?php
$GPSData = 'GPSData000001.txt';				// Путь и имя исходного файла с регистратора
$time_correct = 60*60*(8+6);				// Поправка на часовой пояс, в секундах
$folder_done = "./";					// Папка для готовых gpx файлов, "./" - текущая дериктория

//Значения по умолчанию
$header_autor = 'Author';
$header_time = '2011-09-22T18:56:51Z';
$header_name = 'Name';
$header_desc = 'Description';
$header_trk_name = 'Track Name';

function footer($header_autor, $header_time, $header_name, $header_desc, $header_trk_name)
{
	if (empty($header_autor)){$header_autor = 'Autor';}
	if (empty($header_time)){$header_time = '2011-09-22T18:56:51Z';}
	if (empty($header_name)){$header_name = 'Name';}
	if (empty($header_desc)){$header_desc = 'Description';}
	if (empty($header_trk_name)){$header_trk_name = 'Track Name';}
	
return $header = '<?xml version="1.0" encoding="UTF-8"?>
	<gpx
	xmlns="http://www.topografix.com/GPX/1/1"
	version="1.1"
	creator="Sc0rpion"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
	  <time>'.$header_time.'</time>
	  <metadata>
	    <name>'.$header_name.'</name>
	    <desc>'.$header_desc.'</desc>
	    <author>
	     <name>'.$header_autor.'</name>
	    </author>
	  </metadata>
	  <trk>
	    <name>'.$header_trk_name.'</name>
		<trkseg>';
}

$footer = '
	</trkseg>
  </trk>
</gpx>';

$handle = @fopen($GPSData, "r");
if ($handle) {
    while (($buffer = fgets($handle, 4096)) !== false) {
	    if (strpos($buffer, '$V02') !== false) {
			$flag = 1;
	    } else {
			$pieces = explode(",", $buffer);
			$iso8601 = date('Y-m-d\TH:i:s\Z', $pieces[0]+$time_correct);
			$stroka = '
	        <trkpt lat="'.$pieces[2].'" lon="'.$pieces[3].'">
	          <time>'.$iso8601.'</time>
	        </trkpt>';
			
			if ($flag == 1){
				if (isset($fp)) {
					fwrite($fp, $footer);
					fclose($fp);
				}
				$file_name = $folder_done.$iso8601.'.gpx';
				$fp = fopen($file_name, 'a');
				fwrite($fp, footer($header_autor, $iso8601, $iso8601, $header_desc, $iso8601));
				$flag = 0;
			}
			fwrite($fp, $stroka);
	    }
		
    }
    if (!feof($handle)) {
        echo "Ошибка: fgets() неожиданно потерпел неудачу\n";
    }
	fclose($handle);
}
fclose($fp);
?>
