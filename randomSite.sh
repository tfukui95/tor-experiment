# This script file generates a random number from 1 to 5, and then depending on what number is generated, the user visits a specific site
# on the webserver.

siteNumber=$(awk -v min=1 -v max=5 'BEGIN{srand(); print int(min+rand()*(max-mi n+1))}')

if [ echo $siteNumber == 1 ] then
  proxychains wget -p http://192.168.2.200/engineering.nyu.edu/
elif [ echo $siteNumber == 2 ]; then
  proxychains wget -p http://192.168.2.200/facebook.com/
elif [ echo $siteNumber == 3 ]; then
  proxychains wget -p http://192.168.2.200/youtube.com/
elif [ echo $siteNumber == 4 ]; then
  proxychains wget -p http://192.168.2.200/reddit.com/
elif [ echo $siteNumber == 5 ]; then
  proxychains wget -p http://192.168.2.200/www.mlb.com/mets
fi

