# This script file generates a random number from 1 to 5, and then depending on what number is generated, the user visits a specific site
# on the webserver.

siteNumber=$(awk -v min=1 -v max=5 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')

if [ $siteNumber == 1 ] 
then
  proxychains wget -q -p http://192.168.2.200/engineering.nyu.edu/
elif [ $siteNumber == 2 ] 
then
  proxychains wget -q -p http://192.168.2.200/facebook.com/
elif [ $siteNumber == 3 ]
then
  proxychains wget -q -p http://192.168.2.200/youtube.com/
elif [ $siteNumber == 4 ]
then
  proxychains wget -q -p http://192.168.2.200/reddit.com/
elif [ $siteNumber == 5 ]
then
  proxychains wget -q -p http://192.168.2.200/www.mlb.com/mets
fi

echo -n "Press enter to see which site the client visited:"
if read -t 100 response; then
  if [ $siteNumber == 1 ] 
then
  echo "The client visited NYU's Engineering homepage"
elif [ $siteNumber == 2 ] 
then
  echo "The client visited Facebook"
elif [ $siteNumber == 3 ]
then
  echo "The client visited Youtube"
elif [ $siteNumber == 4 ]
then
  echo "The client visited Reddit"
elif [ $siteNumber == 5 ]
then
  echo "The client visited the New York Mets homepage"
else
    echo "Sorry, you are too slow!"
fi
