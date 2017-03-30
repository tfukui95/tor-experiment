sudo apt-get update
sudo apt-get -y install apache2 php5 libapache2-mod-php5

sudo rm /var/www/html/index.html
echo '<?php' | sudo tee -a /var/www/html/index.php
echo 'echo "Remote address: " . $_SERVER['REMOTE_ADDR'] . "\n";' | sudo tee -a /var/www/html/index.php
echo 'echo "Forwarded for:  " . $_SERVER['HTTP_X_FORWARDED_FOR'] . "\n";' | sudo tee -a /var/www/html/index.php
echo '?>' | sudo tee -a /var/www/html/index.php

sudo /etc/init.d/apache2 restart
