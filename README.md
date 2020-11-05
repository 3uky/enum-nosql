# enum-nosql
MongoDB noSQL injection example from "Hack the Box" for password guessing.

noSQL injection autentication bypass:
If parameter values are directly taken from autentization form as follow:
$query = array("username" => $_POST["username"], "password" => $_POST["password"]);

It's possible to use PHP's associative array processing to inject query that return always true and bypass autentication process.
username[$ne]=1&password[$ne]=1

PHP process malformed input as follow and 
$query = array("username" => array("$ne" => 1), "password" => array("$ne" => 1));

noSQL username and password enumeration:
It's possible to use also regular expressions in query and try to guess username letters one by one.
username="{found username}"&password[$regex]="^{letter from wordlist}"

If we have username for example alice we start with letter with following query
username="{found username}"&password[$regex]="^a"
querry returns true so we know that there is username who starts with letter a. If query returns false we continue with next letter from wordlist. In this way is possible to expose whole username. It's necessary to go through all wordlist even if query returns true because there could be more usernames with same username prefix (in script is possible to solve it with recursions).

after usernames are enumerate it's possible to expose also passwords with following querry
username="{found username}"&password[$regex]="^{letter from wordlist}"

Usage
enum-nosql -u {target_ip}
